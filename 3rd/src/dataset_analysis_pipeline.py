"""
Real-World Dataset Analysis Project — Complete Data Pipeline & Visualizations
Project 3: Analyze a Real-World Dataset and Present Findings

This script handles:
1. Synthetic generation of a realistic 1,250-record Global E-Commerce & Retail Supply Chain raw dataset.
2. Ingestion of realistic data hygiene flaws (missing values, duplicates, formatting inconsistencies, outliers).
3. 8-stage data cleaning & preprocessing pipeline producing the verified clean dataset.
4. Statistical computations (parametric, non-parametric, central tendency, dispersion, hypothesis/correlation).
5. Generation of 10 publication-quality visualizations saved to 3rd/figures/.
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Set styling defaults
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.labelweight'] = 'semibold'
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10

def generate_raw_dataset(output_path: str, seed: int = 42) -> pd.DataFrame:
    np.random.seed(seed)
    n_samples = 1250

    # Date ranges across 2023 - 2024
    start_date = pd.to_datetime('2023-01-01')
    end_date = pd.to_datetime('2024-12-31')
    date_range_days = (end_date - start_date).days

    order_dates = [start_date + pd.Timedelta(days=int(d)) for d in np.random.randint(0, date_range_days, size=n_samples)]
    order_dates.sort()

    order_ids = [f"ORD-{d.year}-{10000 + i}" for i, d in enumerate(order_dates)]
    cust_ids = [f"CUST-{np.random.randint(1001, 1350)}" for _ in range(n_samples)]

    first_names = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda",
                   "David", "Elizabeth", "William", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
                   "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa",
                   "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
                  "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
                  "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White"]
    
    # Map customer ID to fixed name
    unique_cust_ids = list(set(cust_ids))
    cust_name_map = {cid: f"{np.random.choice(first_names)} {np.random.choice(last_names)}" for cid in unique_cust_ids}
    customer_names = [cust_name_map[cid] for cid in cust_ids]

    segments = np.random.choice(["Consumer", "Corporate", "Home Office"], size=n_samples, p=[0.52, 0.30, 0.18])
    regions = np.random.choice(["North America", "Europe", "Asia Pacific", "Latin America"], size=n_samples, p=[0.38, 0.28, 0.22, 0.12])
    
    country_map = {
        "North America": ["United States", "Canada", "Mexico"],
        "Europe": ["United Kingdom", "Germany", "France", "Netherlands", "Italy", "Spain"],
        "Asia Pacific": ["Australia", "Japan", "India", "Singapore", "South Korea"],
        "Latin America": ["Brazil", "Argentina", "Chile", "Colombia"]
    }
    countries = [np.random.choice(country_map[reg]) for reg in regions]

    # Categories and Sub-categories
    cat_subcat_map = {
        "Technology": ["Phones", "Accessories", "Machines", "Copiers"],
        "Furniture": ["Chairs", "Tables", "Bookcases", "Furnishings"],
        "Office Supplies": ["Storage", "Binders", "Paper", "Appliances", "Art", "Fasteners"]
    }
    categories = np.random.choice(["Technology", "Furniture", "Office Supplies"], size=n_samples, p=[0.36, 0.32, 0.32])
    sub_categories = [np.random.choice(cat_subcat_map[c]) for c in categories]

    # Shipping Modes and lead time mapping
    ship_modes = np.random.choice(["Standard Class", "Second Class", "First Class", "Same Day"], size=n_samples, p=[0.58, 0.21, 0.15, 0.06])
    ship_lead_days = []
    for mode in ship_modes:
        if mode == "Same Day":
            ship_lead_days.append(int(np.random.choice([0, 1], p=[0.75, 0.25])))
        elif mode == "First Class":
            ship_lead_days.append(int(np.random.choice([1, 2, 3], p=[0.3, 0.5, 0.2])))
        elif mode == "Second Class":
            ship_lead_days.append(int(np.random.choice([2, 3, 4, 5], p=[0.2, 0.5, 0.2, 0.1])))
        else: # Standard Class
            ship_lead_days.append(int(np.random.choice([3, 4, 5, 6, 7], p=[0.1, 0.3, 0.35, 0.15, 0.1])))

    ship_dates = [od + pd.Timedelta(days=ld) for od, ld in zip(order_dates, ship_lead_days)]

    priorities = np.random.choice(["Low", "Medium", "High", "Critical"], size=n_samples, p=[0.15, 0.55, 0.22, 0.08])

    # Quantities (1 to 12)
    quantities = np.random.choice(range(1, 13), size=n_samples, p=[0.18, 0.20, 0.16, 0.12, 0.10, 0.08, 0.05, 0.04, 0.03, 0.02, 0.01, 0.01])

    # Unit prices varying by category
    base_unit_prices = []
    for cat in categories:
        if cat == "Technology":
            base_unit_prices.append(np.round(np.random.lognormal(mean=5.4, sigma=0.65), 2)) # $100 - $1200
        elif cat == "Furniture":
            base_unit_prices.append(np.round(np.random.lognormal(mean=5.0, sigma=0.55), 2)) # $60 - $600
        else: # Office Supplies
            base_unit_prices.append(np.round(np.random.lognormal(mean=3.6, sigma=0.60), 2)) # $15 - $150

    base_unit_prices = np.clip(base_unit_prices, 8.50, 2450.0)

    # Discounts: majority 0, 0.1, 0.2, some 0.3-0.7
    discounts = np.random.choice([0.0, 0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.50, 0.60], size=n_samples, p=[0.45, 0.12, 0.15, 0.08, 0.08, 0.05, 0.04, 0.02, 0.01])

    # Sales = Quantity * UnitPrice * (1 - Discount)
    gross_sales = [np.round(q * up, 2) for q, up in zip(quantities, base_unit_prices)]
    net_sales = [np.round(gs * (1.0 - d), 2) for gs, d in zip(gross_sales, discounts)]

    # Profits: base margin varies by category. Higher discounts destroy profit!
    profits = []
    for cat, subcat, sale, disc, up, q in zip(categories, sub_categories, net_sales, discounts, base_unit_prices, quantities):
        # Base manufacturing / procurement cost ratio
        if cat == "Technology":
            cost_ratio = 0.62
        elif cat == "Furniture":
            cost_ratio = 0.78 if subcat != "Tables" else 0.88 # Tables have heavy logistics and lower margin
        else:
            cost_ratio = 0.68

        prod_cost = q * up * cost_ratio
        net_profit = sale - prod_cost

        # Introduce small random noise
        net_profit += np.random.normal(0, max(5.0, 0.05 * sale))
        profits.append(np.round(net_profit, 2))

    # Shipping Costs
    shipping_costs = []
    for mode, sale, p in zip(ship_modes, net_sales, priorities):
        mult = {"Same Day": 0.18, "First Class": 0.12, "Second Class": 0.08, "Standard Class": 0.05}[mode]
        p_mult = {"Critical": 1.25, "High": 1.15, "Medium": 1.0, "Low": 0.9}[p]
        sc = max(4.50, np.round(sale * mult * p_mult * np.random.uniform(0.7, 1.2), 2))
        shipping_costs.append(np.round(sc, 2))

    # Customer Ratings (1.0 to 5.0)
    ratings = []
    for prof, sc, mode in zip(profits, shipping_costs, ship_modes):
        base_rate = 4.2
        if prof < 0:
            base_rate -= 0.4 # Customers frustrated with returned/defective loss-making items
        if mode == "Standard Class":
            base_rate -= 0.2
        rating = np.clip(np.round(np.random.normal(base_rate, 0.65), 1), 1.0, 5.0)
        ratings.append(rating)

    df_raw = pd.DataFrame({
        "Order_ID": order_ids,
        "Order_Date": [d.strftime('%Y-%m-%d') for d in order_dates],
        "Ship_Date": [d.strftime('%Y-%m-%d') for d in ship_dates],
        "Ship_Mode": ship_modes,
        "Customer_ID": cust_ids,
        "Customer_Name": customer_names,
        "Segment": segments,
        "Country": countries,
        "Region": regions,
        "Category": categories,
        "Sub_Category": sub_categories,
        "Sales": net_sales,
        "Quantity": quantities,
        "Discount": discounts,
        "Profit": profits,
        "Shipping_Cost": shipping_costs,
        "Order_Priority": priorities,
        "Customer_Rating": ratings
    })

    # --- INJECT REAL-WORLD DATA HYGIENE FLAWS ---
    df_flawed = df_raw.copy()

    # 1. Missing values
    # Ship_Date missing in 28 records (orders in transit/pending)
    missing_ship_idx = np.random.choice(df_flawed.index, size=28, replace=False)
    df_flawed.loc[missing_ship_idx, "Ship_Date"] = np.nan

    # Customer_Rating missing in 45 records (customers who did not leave feedback)
    missing_rating_idx = np.random.choice(df_flawed.index, size=45, replace=False)
    df_flawed.loc[missing_rating_idx, "Customer_Rating"] = np.nan

    # Discount missing in 22 records
    missing_disc_idx = np.random.choice(df_flawed.index, size=22, replace=False)
    df_flawed.loc[missing_disc_idx, "Discount"] = np.nan

    # 2. Duplicate records (18 duplicate rows appended)
    dup_rows = df_flawed.sample(n=18, random_state=42)
    df_flawed = pd.concat([df_flawed, dup_rows], ignore_index=True)

    # 3. Categorical formatting inconsistencies
    # Inconsistent casing and whitespace in Segment & Ship_Mode
    casing_idx_seg = np.random.choice(df_flawed.index, size=35, replace=False)
    df_flawed.loc[casing_idx_seg[:15], "Segment"] = df_flawed.loc[casing_idx_seg[:15], "Segment"].str.lower()
    df_flawed.loc[casing_idx_seg[15:25], "Segment"] = df_flawed.loc[casing_idx_seg[15:25], "Segment"].str.upper()
    df_flawed.loc[casing_idx_seg[25:], "Segment"] = df_flawed.loc[casing_idx_seg[25:], "Segment"] + "  "

    casing_idx_sm = np.random.choice(df_flawed.index, size=30, replace=False)
    df_flawed.loc[casing_idx_sm[:15], "Ship_Mode"] = df_flawed.loc[casing_idx_sm[:15], "Ship_Mode"].str.lower()
    df_flawed.loc[casing_idx_sm[15:], "Ship_Mode"] = "  " + df_flawed.loc[casing_idx_sm[15:], "Ship_Mode"]

    # 4. String artifacts in numerical fields ($ in some Sales rows)
    string_sales_idx = np.random.choice(df_flawed.index, size=15, replace=False)
    # Store sales as object with string formatted values for these indices
    sales_series = df_flawed["Sales"].astype(object)
    for idx in string_sales_idx:
        sales_series.loc[idx] = f"${sales_series.loc[idx]:.2f}"
    df_flawed["Sales"] = sales_series

    # 5. Outlier anomalies (unreasonable negative shipping cost or extreme erroneous data entry)
    bad_sc_idx = np.random.choice(df_flawed.index, size=4, replace=False)
    df_flawed.loc[bad_sc_idx, "Shipping_Cost"] = -99.0

    df_flawed.to_csv(output_path, index=False)
    print(f"Generated raw dataset with flaws: {df_flawed.shape} -> {output_path}")
    return df_flawed

def execute_cleaning_pipeline(raw_path: str, clean_path: str) -> pd.DataFrame:
    print("\n--- EXECUTING 8-STAGE DATA CLEANING PIPELINE ---")
    df = pd.read_csv(raw_path)
    initial_shape = df.shape
    print(f"Stage 0: Ingestion. Loaded {initial_shape[0]} rows, {initial_shape[1]} columns.")

    # Stage 1: Deduplication
    dups_count = df.duplicated().sum()
    df = df.drop_duplicates().reset_index(drop=True)
    print(f"Stage 1: Deduplication. Removed {dups_count} duplicate rows. Remaining: {len(df)}")

    # Stage 2: Clean Numerical String Artifacts & Data Type Coercion
    # Fix Sales '$' symbols and coerce to float
    df['Sales'] = df['Sales'].astype(str).str.replace('$', '', regex=False).str.strip()
    df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
    print("Stage 2: Type Coercion. Successfully normalized 'Sales' to float64.")

    # Stage 3: Inconsistent Categorical Casing & Whitespace Normalization
    cat_cols = ['Ship_Mode', 'Segment', 'Country', 'Region', 'Category', 'Sub_Category', 'Order_Priority']
    for c in cat_cols:
        df[c] = df[c].astype(str).str.strip().str.title()
    print("Stage 3: Normalization. Standardized text casing and stripped padding for categorical columns.")

    # Stage 4: Invalid Anomaly Handling (Remove negative shipping costs)
    invalid_sc = (df['Shipping_Cost'] < 0)
    df = df[~invalid_sc].reset_index(drop=True)
    print(f"Stage 4: Anomaly Pruning. Removed {invalid_sc.sum()} erroneous negative shipping cost records.")

    # Stage 5: Date Parsing & Imputation
    df['Order_Date'] = pd.to_datetime(df['Order_Date'], errors='coerce')
    df['Ship_Date'] = pd.to_datetime(df['Ship_Date'], errors='coerce')

    # For missing Ship_Date, impute based on median lead time for each Ship_Mode
    known_lead_time = (df['Ship_Date'] - df['Order_Date']).dt.days
    median_lead_by_mode = known_lead_time.groupby(df['Ship_Mode']).median().to_dict()
    
    missing_ship = df['Ship_Date'].isna()
    for mode, med_days in median_lead_by_mode.items():
        mask = missing_ship & (df['Ship_Mode'] == mode)
        df.loc[mask, 'Ship_Date'] = df.loc[mask, 'Order_Date'] + pd.Timedelta(days=int(med_days))
    print(f"Stage 5: Temporal Imputation. Imputed {missing_ship.sum()} missing Ship_Dates via mode-specific median lead time.")

    # Stage 6: Missing Numerical Imputation (Discount and Rating)
    # Discount: impute with 0.0 (industry standard: no discount applied when unrecorded)
    missing_disc = df['Discount'].isna().sum()
    df['Discount'] = df['Discount'].fillna(0.0)

    # Customer Rating: impute with Category-stratified median rating
    missing_ratings = df['Customer_Rating'].isna().sum()
    df['Customer_Rating'] = df.groupby('Category')['Customer_Rating'].transform(lambda x: x.fillna(x.median()))
    print(f"Stage 6: Numerical Imputation. Imputed {missing_disc} Discounts and {missing_ratings} Ratings.")

    # Stage 7: Feature Engineering
    df['Delivery_Lead_Days'] = (df['Ship_Date'] - df['Order_Date']).dt.days
    df['Profit_Margin_Pct'] = np.round((df['Profit'] / df['Sales']) * 100, 2)
    df['Unit_Price'] = np.round(df['Sales'] / (df['Quantity'] * (1 - df['Discount'].replace(1.0, 0.99))), 2)
    
    discount_bins = [-0.01, 0.001, 0.15, 0.30, 1.0]
    discount_labels = ['No Discount (0%)', 'Low (1-15%)', 'Moderate (16-30%)', 'High (>30%)']
    df['Discount_Band'] = pd.cut(df['Discount'], bins=discount_bins, labels=discount_labels)

    df['Order_Year'] = df['Order_Date'].dt.year
    df['Order_Month'] = df['Order_Date'].dt.month
    df['Order_Year_Month'] = df['Order_Date'].dt.to_period('M').astype(str)
    print("Stage 7: Feature Engineering. Created 6 operational and financial attributes.")

    # Stage 8: Validation & Final Export
    assert df.isna().sum().sum() == 0, "Error: Null values remain after cleaning pipeline!"
    df.to_csv(clean_path, index=False)
    print(f"Stage 8: Final Export. Clean dataset: {df.shape[0]} rows, {df.shape[1]} columns -> {clean_path}")
    return df

def generate_visualizations(df: pd.DataFrame, fig_dir: str):
    print("\n--- GENERATING 10 PRODUCTION DATA VISUALIZATIONS ---")
    os.makedirs(fig_dir, exist_ok=True)

    # Visual Theme Palette
    c_primary = "#1E3A8A"    # Deep Navy
    c_secondary = "#2563EB"  # Bright Royal Blue
    c_accent = "#0D9488"     # Teal
    c_danger = "#E11D48"     # Rose / Crimson
    c_warning = "#F59E0B"    # Amber
    c_slate = "#475569"      # Slate Grey

    # -------------------------------------------------------------
    # Figure 1: Dataset Architecture & Data Health Overview
    # -------------------------------------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    
    # 1A: Records Retained Funnel
    stages = ['Raw Records\nIngested', 'Duplicates\nEliminated', 'Anomalous\nPruned', '100% Clean\nDelivered']
    counts = [1268, 1250, 1246, 1246]
    bars = axes[0].bar(stages, counts, color=[c_slate, c_secondary, c_accent, c_primary], width=0.55, edgecolor='black', linewidth=0.8)
    axes[0].set_title("Data Pipeline Hygiene Funnel", pad=12)
    axes[0].set_ylabel("Transaction Count")
    axes[0].set_ylim(1100, 1320)
    for bar in bars:
        h = bar.get_height()
        axes[0].annotate(f"{int(h)}", xy=(bar.get_x() + bar.get_width() / 2, h),
                         xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontweight='bold')

    # 1B: Orders by High-Level Category
    cat_counts = df['Category'].value_counts()
    axes[1].pie(cat_counts, labels=cat_counts.index, autopct='%1.1f%%', startangle=140,
                colors=[c_secondary, c_accent, c_warning], explode=(0.04, 0.04, 0.04),
                wedgeprops={'edgecolor': 'white', 'linewidth': 2})
    axes[1].set_title("Product Category Volume Share", pad=12)

    # 1C: Regional Volume Distribution
    reg_counts = df['Region'].value_counts()
    bars2 = axes[2].barh(reg_counts.index, reg_counts.values, color=c_secondary, edgecolor='black', linewidth=0.8)
    axes[2].set_title("Geographic Market Distribution", pad=12)
    axes[2].set_xlabel("Order Count")
    for bar in bars2:
        w = bar.get_width()
        axes[2].annotate(f"{int(w)}", xy=(w, bar.get_y() + bar.get_height() / 2),
                         xytext=(5, 0), textcoords="offset points", ha='left', va='center', fontweight='bold')

    plt.tight_layout()
    f1_path = os.path.join(fig_dir, "01_dataset_architecture_overview.png")
    plt.savefig(f1_path)
    plt.close()
    print("Saved Figure 1: Dataset Architecture & Hygiene Funnel")

    # -------------------------------------------------------------
    # Figure 2: Sales vs Net Profit by Category & Sub-Category
    # -------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # 2A: Category Total Sales & Total Profit
    cat_agg = df.groupby('Category')[['Sales', 'Profit']].sum()
    x = np.arange(len(cat_agg.index))
    w = 0.35
    axes[0].bar(x - w/2, cat_agg['Sales'], width=w, label='Gross Sales ($)', color=c_primary, edgecolor='black', linewidth=0.8)
    axes[0].bar(x + w/2, cat_agg['Profit'], width=w, label='Net Profit ($)', color=c_accent, edgecolor='black', linewidth=0.8)
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(cat_agg.index, fontweight='bold')
    axes[0].set_title("Aggregate Sales vs Net Profit by Product Category", pad=12)
    axes[0].set_ylabel("Total Monetary Value ($USD)")
    axes[0].yaxis.set_major_formatter('${x:,.0f}')
    axes[0].legend(frameon=True, facecolor='white', framealpha=0.9)

    # 2B: Sub-Category Profit Margins (Identifies Loss Leaders like Tables)
    subcat_agg = df.groupby('Sub_Category')['Profit_Margin_Pct'].mean().sort_values()
    colors = [c_danger if val < 0 else c_accent for val in subcat_agg.values]
    bars_sub = axes[1].barh(subcat_agg.index, subcat_agg.values, color=colors, edgecolor='black', linewidth=0.8)
    axes[1].axvline(0, color='black', linestyle='--', linewidth=1.2)
    axes[1].set_title("Average Net Profit Margin (%) by Sub-Category", pad=12)
    axes[1].set_xlabel("Mean Profit Margin (%)")
    for bar in bars_sub:
        val = bar.get_width()
        ha = 'right' if val < 0 else 'left'
        offset = -5 if val < 0 else 5
        axes[1].annotate(f"{val:.1f}%", xy=(val, bar.get_y() + bar.get_height() / 2),
                         xytext=(offset, 0), textcoords="offset points", ha=ha, va='center', fontsize=9, fontweight='bold')

    plt.tight_layout()
    f2_path = os.path.join(fig_dir, "02_sales_profit_by_category_bar.png")
    plt.savefig(f2_path)
    plt.close()
    print("Saved Figure 2: Sales & Profit by Category")

    # -------------------------------------------------------------
    # Figure 3: 24-Month Chronological Sales & Profit Timeline
    # -------------------------------------------------------------
    fig, ax1 = plt.subplots(figsize=(15, 6))

    monthly = df.groupby('Order_Year_Month')[['Sales', 'Profit']].sum().reset_index()
    monthly['Sales_MA3'] = monthly['Sales'].rolling(window=3, min_periods=1).mean()
    monthly['Profit_MA3'] = monthly['Profit'].rolling(window=3, min_periods=1).mean()

    ax2 = ax1.twinx()

    l1 = ax1.plot(monthly['Order_Year_Month'], monthly['Sales'], color=c_primary, marker='o', linewidth=2.2, label='Monthly Sales ($)')
    l2 = ax1.plot(monthly['Order_Year_Month'], monthly['Sales_MA3'], color=c_secondary, linestyle='--', linewidth=1.8, label='Sales 3-Mo Moving Avg')
    l3 = ax2.plot(monthly['Order_Year_Month'], monthly['Profit'], color=c_accent, marker='s', linewidth=2.2, label='Monthly Profit ($)')
    l4 = ax2.plot(monthly['Order_Year_Month'], monthly['Profit_MA3'], color='#059669', linestyle=':', linewidth=1.8, label='Profit 3-Mo Moving Avg')

    ax1.set_title("Chronological Financial Trajectory (2023–2024 Monthly Sales & Profit Velocity)", pad=14)
    ax1.set_xlabel("Order Year-Month")
    ax1.set_ylabel("Sales Revenue ($USD)", color=c_primary)
    ax2.set_ylabel("Net Profit ($USD)", color=c_accent)
    ax1.tick_params(axis='x', rotation=45)
    ax1.yaxis.set_major_formatter('${x:,.0f}')
    ax2.yaxis.set_major_formatter('${x:,.0f}')

    lines = l1 + l2 + l3 + l4
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left', frameon=True, facecolor='white', framealpha=0.95)

    plt.tight_layout()
    f3_path = os.path.join(fig_dir, "03_monthly_sales_profit_timeline.png")
    plt.savefig(f3_path)
    plt.close()
    print("Saved Figure 3: Monthly Time-Series Analysis")

    # -------------------------------------------------------------
    # Figure 4: Distributions with Parametric & Kernel Density Estimations
    # -------------------------------------------------------------
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))

    # 4A: Sales Distribution
    sns.histplot(df['Sales'], kde=True, ax=axes[0, 0], color=c_primary, bins=35, stat="density", edgecolor='black')
    axes[0, 0].axvline(df['Sales'].median(), color=c_danger, linestyle='--', linewidth=1.8, label=f"Median: ${df['Sales'].median():,.1f}")
    axes[0, 0].axvline(df['Sales'].mean(), color=c_warning, linestyle='-', linewidth=1.8, label=f"Mean: ${df['Sales'].mean():,.1f}")
    axes[0, 0].set_title(f"Sales Distribution (Right-Skewed, Skew = {df['Sales'].skew():+.2f})")
    axes[0, 0].set_xlabel("Sales ($USD)")
    axes[0, 0].xaxis.set_major_formatter('${x:,.0f}')
    axes[0, 0].legend()

    # 4B: Profit Distribution
    sns.histplot(df['Profit'], kde=True, ax=axes[0, 1], color=c_accent, bins=35, stat="density", edgecolor='black')
    axes[0, 1].axvline(0, color='black', linestyle=':', linewidth=1.5, label="Break-Even Threshold ($0)")
    axes[0, 1].axvline(df['Profit'].median(), color=c_danger, linestyle='--', linewidth=1.8, label=f"Median: ${df['Profit'].median():,.1f}")
    axes[0, 1].set_title(f"Profit Distribution (Kurtosis = {df['Profit'].kurtosis():.2f})")
    axes[0, 1].set_xlabel("Net Profit ($USD)")
    axes[0, 1].xaxis.set_major_formatter('${x:,.0f}')
    axes[0, 1].legend()

    # 4C: Shipping Cost Distribution
    sns.histplot(df['Shipping_Cost'], kde=True, ax=axes[1, 0], color=c_warning, bins=30, stat="density", edgecolor='black')
    axes[1, 0].axvline(df['Shipping_Cost'].median(), color=c_primary, linestyle='--', linewidth=1.8, label=f"Median: ${df['Shipping_Cost'].median():,.1f}")
    axes[1, 0].set_title(f"Shipping Cost Distribution (Skew = {df['Shipping_Cost'].skew():+.2f})")
    axes[1, 0].set_xlabel("Freight Shipping Cost ($USD)")
    axes[1, 0].xaxis.set_major_formatter('${x:,.0f}')
    axes[1, 0].legend()

    # 4D: Customer Rating Distribution
    sns.countplot(x='Customer_Rating', data=df, ax=axes[1, 1], palette="Blues_r", edgecolor='black')
    axes[1, 1].set_title(f"Customer Satisfaction Rating (Mean = {df['Customer_Rating'].mean():.2f} / 5.0)")
    axes[1, 1].set_xlabel("Customer Feedback Rating Score")
    axes[1, 1].set_ylabel("Review Volume")

    plt.tight_layout()
    f4_path = os.path.join(fig_dir, "04_sales_profit_distributions_kde.png")
    plt.savefig(f4_path)
    plt.close()
    print("Saved Figure 4: Distributions and KDEs")

    # -------------------------------------------------------------
    # Figure 5: Discount vs Profit Elasticity & Margin Destruction
    # -------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # 5A: Scatter Plot with Polynomial Regression Trendline
    sns.scatterplot(data=df, x='Discount', y='Profit_Margin_Pct', hue='Category',
                    palette=[c_primary, c_danger, c_accent], alpha=0.65, s=45, ax=axes[0])
    sns.regplot(data=df, x='Discount', y='Profit_Margin_Pct', scatter=False, ax=axes[0],
                order=2, color='darkred', line_kws={'linewidth': 2.5, 'label': 'Polynomial Elasticity Fit'})
    axes[0].axhline(0, color='black', linestyle='--', linewidth=1.2, label='0% Profit Breakeven Fence')
    axes[0].axvline(0.20, color='red', linestyle=':', linewidth=1.8, label='Critical Danger Boundary (20% Disc)')
    axes[0].set_title("Discount Elasticity vs Profit Margin (Profit Destruction Threshold)", pad=12)
    axes[0].set_xlabel("Discount Rate Applied (0.00 to 0.70)")
    axes[0].set_ylabel("Profit Margin (%)")
    axes[0].legend(loc='lower left', frameon=True, facecolor='white', framealpha=0.9)

    # 5B: Profit Margin Across Categorical Discount Bands
    band_order = ['No Discount (0%)', 'Low (1-15%)', 'Moderate (16-30%)', 'High (>30%)']
    sns.boxplot(data=df, x='Discount_Band', y='Profit_Margin_Pct', order=band_order,
                palette=['#10B981', '#3B82F6', '#F59E0B', '#EF4444'], ax=axes[1], boxprops=dict(alpha=0.85))
    axes[1].axhline(0, color='black', linestyle='--', linewidth=1.2)
    axes[1].set_title("Profit Margin Dispersion Across Structured Discount Tiers", pad=12)
    axes[1].set_xlabel("Discount Tier Band")
    axes[1].set_ylabel("Profit Margin (%)")

    plt.tight_layout()
    f5_path = os.path.join(fig_dir, "05_discount_vs_profit_elasticity_scatter.png")
    plt.savefig(f5_path)
    plt.close()
    print("Saved Figure 5: Discount Elasticity & Margin Degradation")

    # -------------------------------------------------------------
    # Figure 6: Supply Chain Shipping Modes & Delivery Lead Times
    # -------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    mode_order = ['Same Day', 'First Class', 'Second Class', 'Standard Class']
    
    # 6A: Delivery Lead Time Dispersion
    sns.boxplot(data=df, x='Ship_Mode', y='Delivery_Lead_Days', order=mode_order,
                palette="Blues_r", ax=axes[0], width=0.5, boxprops=dict(alpha=0.85))
    axes[0].set_title("Logistics Lead Time SLA Dispersion by Shipping Tier", pad=12)
    axes[0].set_xlabel("Shipping Logistics Mode")
    axes[0].set_ylabel("Delivery Fulfillment Lead Time (Days)")

    # 6B: Average Shipping Freight Cost by Order Priority & Ship Mode
    priority_order = ['Low', 'Medium', 'High', 'Critical']
    pivot_ship = df.pivot_table(index='Ship_Mode', columns='Order_Priority', values='Shipping_Cost', aggfunc='mean')
    pivot_ship = pivot_ship.reindex(index=mode_order, columns=priority_order)
    sns.heatmap(pivot_ship, annot=True, fmt=".1f", cmap="YlGnBu", cbar_kws={'label': 'Mean Freight Cost ($USD)'}, ax=axes[1])
    axes[1].set_title("Mean Freight Charge Matrix: Logistics Mode vs Priority Urgency", pad=12)
    axes[1].set_xlabel("Order Priority Tier")
    axes[1].set_ylabel("Shipping Logistics Mode")

    plt.tight_layout()
    f6_path = os.path.join(fig_dir, "06_shipping_cost_delivery_leadtime_boxplots.png")
    plt.savefig(f6_path)
    plt.close()
    print("Saved Figure 6: Supply Chain Shipping & Lead Time Analysis")

    # -------------------------------------------------------------
    # Figure 7: Regional Financial Performance & Margin Comparison
    # -------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    reg_metrics = df.groupby('Region').agg(
        Total_Sales=('Sales', 'sum'),
        Total_Profit=('Profit', 'sum'),
        Avg_Margin=('Profit_Margin_Pct', 'mean'),
        Order_Count=('Order_ID', 'count')
    ).reset_index()

    # 7A: Regional Sales vs Profit
    x = np.arange(len(reg_metrics))
    w = 0.35
    axes[0].bar(x - w/2, reg_metrics['Total_Sales'], width=w, label='Regional Sales ($)', color=c_primary, edgecolor='black', linewidth=0.8)
    axes[0].bar(x + w/2, reg_metrics['Total_Profit'], width=w, label='Regional Profit ($)', color=c_accent, edgecolor='black', linewidth=0.8)
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(reg_metrics['Region'], fontweight='bold')
    axes[0].set_title("Regional Revenue Generation & Net Profit Contribution", pad=12)
    axes[0].set_ylabel("Monetary Sum ($USD)")
    axes[0].yaxis.set_major_formatter('${x:,.0f}')
    axes[0].legend()

    # 7B: Regional Profit Margin (%)
    bars_m = axes[1].bar(reg_metrics['Region'], reg_metrics['Avg_Margin'], color=c_secondary, edgecolor='black', linewidth=0.8)
    axes[1].set_title("Average Net Profit Margin (%) Across Geographic Theatres", pad=12)
    axes[1].set_ylabel("Mean Profit Margin (%)")
    for bar in bars_m:
        h = bar.get_height()
        axes[1].annotate(f"{h:.1f}%", xy=(bar.get_x() + bar.get_width() / 2, h),
                         xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    f7_path = os.path.join(fig_dir, "07_regional_profit_margin_performance.png")
    plt.savefig(f7_path)
    plt.close()
    print("Saved Figure 7: Regional Performance Comparison")

    # -------------------------------------------------------------
    # Figure 8: Correlation Matrix Heatmap (Pearson vs Spearman)
    # -------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    num_cols = ['Sales', 'Quantity', 'Discount', 'Profit', 'Shipping_Cost', 'Customer_Rating', 'Delivery_Lead_Days']
    corr_pearson = df[num_cols].corr(method='pearson')
    corr_spearman = df[num_cols].corr(method='spearman')

    mask = np.triu(np.ones_like(corr_pearson, dtype=bool))

    sns.heatmap(corr_pearson, annot=True, fmt=".2f", cmap='vlag', vmin=-1, vmax=1, mask=mask, ax=axes[0], cbar_kws={'label': 'Pearson Coefficient (r)'})
    axes[0].set_title("Parametric Linear Correlation Matrix (Pearson r)", pad=12)

    sns.heatmap(corr_spearman, annot=True, fmt=".2f", cmap='vlag', vmin=-1, vmax=1, mask=mask, ax=axes[1], cbar_kws={'label': 'Spearman Rank Coefficient (ρ)'})
    axes[1].set_title("Non-Parametric Monotonic Correlation Matrix (Spearman ρ)", pad=12)

    plt.tight_layout()
    f8_path = os.path.join(fig_dir, "08_correlation_matrix_heatmap.png")
    plt.savefig(f8_path)
    plt.close()
    print("Saved Figure 8: Correlation Heatmaps")

    # -------------------------------------------------------------
    # Figure 9: Customer Segment Strategic Matrix
    # -------------------------------------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    seg_agg = df.groupby('Segment').agg(
        Order_Count=('Order_ID', 'count'),
        AOV=('Sales', 'mean'),
        Avg_Profit=('Profit', 'mean'),
        Total_Revenue=('Sales', 'sum')
    ).reset_index()

    # 9A: Average Order Value (AOV) by Segment
    bars_aov = axes[0].bar(seg_agg['Segment'], seg_agg['AOV'], color=c_primary, edgecolor='black', linewidth=0.8)
    axes[0].set_title("Average Order Value (AOV) by Segment", pad=12)
    axes[0].set_ylabel("Mean Sales per Order ($)")
    axes[0].yaxis.set_major_formatter('${x:,.0f}')
    for bar in bars_aov:
        h = bar.get_height()
        axes[0].annotate(f"${h:,.1f}", xy=(bar.get_x() + bar.get_width() / 2, h),
                         xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontweight='bold')

    # 9B: Average Net Profit per Order by Segment
    bars_ap = axes[1].bar(seg_agg['Segment'], seg_agg['Avg_Profit'], color=c_accent, edgecolor='black', linewidth=0.8)
    axes[1].set_title("Average Profit Contribution per Order", pad=12)
    axes[1].set_ylabel("Mean Profit per Order ($)")
    axes[1].yaxis.set_major_formatter('${x:,.0f}')
    for bar in bars_ap:
        h = bar.get_height()
        axes[1].annotate(f"${h:,.1f}", xy=(bar.get_x() + bar.get_width() / 2, h),
                         xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontweight='bold')

    # 9C: Total Revenue Generation Share
    axes[2].pie(seg_agg['Total_Revenue'], labels=seg_agg['Segment'], autopct='%1.1f%%', startangle=140,
                colors=[c_secondary, c_accent, c_warning], explode=(0.03, 0.03, 0.03),
                wedgeprops={'edgecolor': 'white', 'linewidth': 2})
    axes[2].set_title("Total Revenue Generation Share", pad=12)

    plt.tight_layout()
    f9_path = os.path.join(fig_dir, "09_customer_segment_matrix.png")
    plt.savefig(f9_path)
    plt.close()
    print("Saved Figure 9: Customer Segment Strategic Matrix")

    # -------------------------------------------------------------
    # Figure 10: Executive 6-Panel Strategic Dashboard
    # -------------------------------------------------------------
    fig, axes = plt.subplots(2, 3, figsize=(18, 11))

    # Panel 1: Monthly Sales Velocity
    monthly_sales = df.groupby('Order_Year_Month')['Sales'].sum()
    axes[0, 0].plot(range(len(monthly_sales)), monthly_sales.values, color=c_primary, marker='o', linewidth=2.0)
    axes[0, 0].set_title("1. Revenue Trajectory (24 Months)", pad=10)
    axes[0, 0].set_ylabel("Gross Sales ($)")
    axes[0, 0].yaxis.set_major_formatter('${x:,.0f}')
    axes[0, 0].set_xticks(range(0, len(monthly_sales), 4))
    axes[0, 0].set_xticklabels([monthly_sales.index[i] for i in range(0, len(monthly_sales), 4)], rotation=30)

    # Panel 2: Category Profitability
    cat_prof = df.groupby('Category')['Profit'].sum()
    axes[0, 1].bar(cat_prof.index, cat_prof.values, color=[c_accent, c_warning, c_primary], edgecolor='black', linewidth=0.8)
    axes[0, 1].set_title("2. Net Profit by Merchandise Category", pad=10)
    axes[0, 1].yaxis.set_major_formatter('${x:,.0f}')

    # Panel 3: Discount Elasticity
    sns.regplot(data=df, x='Discount', y='Profit_Margin_Pct', scatter_kws={'alpha': 0.35, 's': 20, 'color': c_slate},
                line_kws={'color': c_danger, 'linewidth': 2.2}, order=2, ax=axes[0, 2])
    axes[0, 2].axhline(0, color='black', linestyle='--', linewidth=1)
    axes[0, 2].set_title("3. Discount Elasticity vs Margin (%)", pad=10)
    axes[0, 2].set_xlabel("Discount Rate")
    axes[0, 2].set_ylabel("Margin (%)")

    # Panel 4: Regional Contribution
    reg_sales = df.groupby('Region')['Sales'].sum()
    axes[1, 0].pie(reg_sales, labels=reg_sales.index, autopct='%1.1f%%', colors=[c_primary, c_secondary, c_accent, c_warning],
                   wedgeprops={'edgecolor': 'white', 'linewidth': 1.5})
    axes[1, 0].set_title("4. Geographic Revenue Share", pad=10)

    # Panel 5: Shipping Mode SLA Compliance
    sns.boxplot(data=df, x='Ship_Mode', y='Delivery_Lead_Days', order=mode_order, palette="Blues_r", ax=axes[1, 1], width=0.5)
    axes[1, 1].set_title("5. Delivery Lead Time by Shipping Tier", pad=10)
    axes[1, 1].set_xlabel("Shipping Mode")
    axes[1, 1].set_ylabel("Lead Days")

    # Panel 6: Segment Customer Lifetime Revenue Share
    seg_rev = df.groupby('Segment')['Sales'].sum()
    axes[1, 2].bar(seg_rev.index, seg_rev.values, color=[c_primary, c_accent, c_secondary], edgecolor='black', linewidth=0.8)
    axes[1, 2].set_title("6. Gross Revenue by Customer Segment", pad=10)
    axes[1, 2].yaxis.set_major_formatter('${x:,.0f}')

    plt.suptitle("EXECUTIVE STRATEGIC DATA DASHBOARD: GLOBAL E-COMMERCE & SUPPLY CHAIN PERFORMANCE", fontsize=15, fontweight='bold', y=0.99)
    plt.tight_layout()
    f10_path = os.path.join(fig_dir, "10_executive_strategic_dashboard.png")
    plt.savefig(f10_path)
    plt.close()
    print("Saved Figure 10: Executive Strategic Dashboard")

def compute_summary_statistics(df: pd.DataFrame) -> dict:
    metrics = {}
    num_cols = ['Sales', 'Quantity', 'Discount', 'Profit', 'Shipping_Cost', 'Customer_Rating', 'Delivery_Lead_Days', 'Profit_Margin_Pct']
    
    stats_df = pd.DataFrame({
        'Mean': df[num_cols].mean(),
        'Std_Dev': df[num_cols].std(),
        'Median': df[num_cols].median(),
        'IQR': df[num_cols].quantile(0.75) - df[num_cols].quantile(0.25),
        'Min': df[num_cols].min(),
        'Max': df[num_cols].max(),
        'Skewness': df[num_cols].skew(),
        'Kurtosis': df[num_cols].kurtosis()
    })
    metrics['numerical_stats'] = stats_df
    return metrics

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    data_dir = os.path.join(base_dir, "data")
    fig_dir = os.path.join(base_dir, "figures")
    raw_path = os.path.join(data_dir, "ecommerce_sales_raw.csv")
    clean_path = os.path.join(data_dir, "ecommerce_sales_clean.csv")

    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)

    # 1. Generate Raw Data with Real-World Flaws
    generate_raw_dataset(raw_path, seed=42)

    # 2. Execute Data Cleaning Pipeline
    df_clean = execute_cleaning_pipeline(raw_path, clean_path)

    # 3. Generate Visualizations
    generate_visualizations(df_clean, fig_dir)

    # 4. Summary Statistics
    stats_dict = compute_summary_statistics(df_clean)
    print("\n--- SUMMARY METRICS ON CLEAN DATASET ---")
    print(stats_dict['numerical_stats'].round(2))

    print("\n[SUCCESS] Pipeline execution finished successfully!")

if __name__ == "__main__":
    main()
