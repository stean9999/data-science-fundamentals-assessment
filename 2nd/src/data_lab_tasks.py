"""
Hands-On Data Lab Implementation — Practical Tasks Pipeline
Assignment 2: Build a working data analysis environment and complete practical exercises
Track: Data Science Internship Core
Author: Data Science Intern
"""

import os
import sys
import warnings
import matplotlib
matplotlib.use('Agg')  # Headless backend to prevent interactive popups and blocking
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns
import sklearn
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split

# Configure UTF-8 encoding on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Global seed and warnings
np.random.seed(42)
warnings.filterwarnings('ignore')

# Set working directory to 2nd folder
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.abspath(os.path.join(script_dir, ".."))
os.chdir(base_dir)

data_dir = os.path.join(base_dir, "data")
fig_dir = os.path.join(base_dir, "figures")
os.makedirs(data_dir, exist_ok=True)
os.makedirs(fig_dir, exist_ok=True)

# Plot styling
STYLE = 'seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'seaborn-whitegrid'
plt.style.use(STYLE)
sns.set_palette('deep')

# =============================================================================
# 1. ENVIRONMENT SETUP & VERSION AUDIT
# =============================================================================
print("=" * 65)
print("  DATA SCIENCE ENVIRONMENT — VERSION REPORT")
print("=" * 65)
print(f"  Python        : {sys.version.split()[0]}")
print(f"  NumPy         : {np.__version__}")
print(f"  Pandas        : {pd.__version__}")
print(f"  Matplotlib    : {matplotlib.__version__}")
print(f"  Seaborn       : {sns.__version__}")
print(f"  Scikit-learn  : {sklearn.__version__}")
print("=" * 65)
print("  All libraries verified successfully.")
print("=" * 65)

# =============================================================================
# 2. WORK WITH DATA USING PANDAS & NUMPY — SYNTHESIS & INGESTION
# =============================================================================
print("\n[SECTION 2] Synthesizing Multi-Modal Retail Dataset...")
n = 500
categories    = ['Electronics', 'Clothing', 'Groceries', 'Furniture', 'Sports']
regions       = ['North', 'South', 'East', 'West', 'Central']
payment_modes = ['Credit Card', 'Debit Card', 'Cash', 'UPI', 'Net Banking']
genders       = ['Male', 'Female']

order_ids    = [f'ORD-{10000 + i}' for i in range(n)]
dates        = pd.date_range(start='2023-01-01', periods=n, freq='D')
cat          = np.random.choice(categories, n, p=[0.30, 0.20, 0.25, 0.10, 0.15])
region       = np.random.choice(regions, n)
payment      = np.random.choice(payment_modes, n)
gender       = np.random.choice(genders, n)
age          = np.random.randint(18, 70, n)
units_sold   = np.random.randint(1, 20, n)
unit_price   = np.round(np.random.uniform(50, 5000, n), 2)
discount_pct = np.round(np.random.choice([0, 5, 10, 15, 20, 25], n,
                                          p=[0.30, 0.20, 0.20, 0.15, 0.10, 0.05]), 1)
revenue      = np.round(units_sold * unit_price * (1 - discount_pct / 100), 2)
rating       = np.round(np.clip(np.random.normal(3.8, 0.7, n), 1, 5), 1)
returned     = np.where(rating < 2.5, 1, np.random.binomial(1, 0.05, n))

df_raw = pd.DataFrame({
    'OrderID'    : order_ids,
    'Date'       : dates,
    'Category'   : cat,
    'Region'     : region,
    'Gender'     : gender,
    'Age'        : age,
    'PaymentMode': payment,
    'UnitsSold'  : units_sold,
    'UnitPrice'  : unit_price,
    'DiscountPct': discount_pct,
    'Revenue'    : revenue,
    'Rating'     : rating,
    'Returned'   : returned
})

# Inject real-world data flaws for cleaning exercise
np.random.seed(7)
miss_idx = np.random.choice(df_raw.index, size=30, replace=False)
df_raw.loc[miss_idx[:15], 'Rating']    = np.nan
df_raw.loc[miss_idx[15:], 'UnitPrice'] = np.nan

dup_idx = np.random.choice(df_raw.index, size=10, replace=False)
df_raw  = pd.concat([df_raw, df_raw.iloc[dup_idx]], ignore_index=True)

err_idx = np.random.choice(df_raw.index, size=15, replace=False)
df_raw.loc[err_idx, 'Gender'] = df_raw.loc[err_idx, 'Gender'].str.lower()

df_raw.loc[df_raw.index[3], 'Revenue'] = -999.0

raw_path = os.path.join(data_dir, 'retail_sales_raw.csv')
df_raw.to_csv(raw_path, index=False)
print(f"  Raw dataset saved -> {raw_path} | Shape: {df_raw.shape}")

# Slicing, filtering & ranking demonstrations
high_elec = df_raw[(df_raw['Category'] == 'Electronics') & (df_raw['Revenue'] > 10_000)]
print(f"  High-value Electronics transactions (> $10k): {len(high_elec)}")

# Relational Join demonstration
tier_lookup = pd.DataFrame({
    'Region'     : ['North', 'South', 'East', 'West', 'Central'],
    'LoyaltyTier': ['Gold', 'Silver', 'Platinum', 'Bronze', 'Silver']
})
df_merged = df_raw.merge(tier_lookup, on='Region', how='left')
print(f"  Relational merge completed. Merged columns: {list(df_merged.columns)}")

# =============================================================================
# 3. DATA CLEANING PIPELINE
# =============================================================================
print("\n[SECTION 3] Executing 8-Stage Data Cleaning Pipeline...")
df_clean = df_raw.copy()

# Step 1: Remove duplicates
init_len = len(df_clean)
df_clean.drop_duplicates(inplace=True)
print(f"  [1] Removed {init_len - len(df_clean)} duplicate rows -> {len(df_clean)} remain.")

# Step 2: Fix casing
df_clean['Gender'] = df_clean['Gender'].str.title()
print(f"  [2] Standardized Gender casing -> {df_clean['Gender'].unique()}")

# Step 3: Remove negative revenue anomaly
df_clean = df_clean[df_clean['Revenue'] > 0]
print(f"  [3] Filtered financial anomalies -> {len(df_clean)} valid rows remain.")

# Step 4: Impute missing Rating with category median
cat_rating_med = df_clean.groupby('Category', observed=False)['Rating'].transform('median')
df_clean['Rating'] = df_clean['Rating'].fillna(cat_rating_med).round(1)
print(f"  [4] Imputed missing Ratings using category medians.")

# Step 5: Impute missing UnitPrice with category mean
cat_price_mean = df_clean.groupby('Category', observed=False)['UnitPrice'].transform('mean')
df_clean['UnitPrice'] = df_clean['UnitPrice'].fillna(cat_price_mean).round(2)
print(f"  [5] Imputed missing UnitPrices using category means.")

# Step 6: Recalculate net revenue
df_clean['Revenue'] = np.round(df_clean['UnitsSold'] * df_clean['UnitPrice'] * (1 - df_clean['DiscountPct'] / 100), 2)
print(f"  [6] Vectorially reconciled Net Revenue.")

# Step 7: Parse datetime
df_clean['Date'] = pd.to_datetime(df_clean['Date'])
df_clean['Month'] = df_clean['Date'].dt.month_name().str[:3]
df_clean['Quarter'] = 'Q' + df_clean['Date'].dt.quarter.astype(str)
print(f"  [7] Parsed Datetime & extracted Month/Quarter features.")

# Step 8: Profit margin feature engineering
df_clean['ProfitMargin'] = np.round((1 - df_clean['DiscountPct'] / 100) * 100, 1)
print(f"  [8] Engineered ProfitMargin feature.")

clean_path = os.path.join(data_dir, 'retail_sales_clean.csv')
df_clean.to_csv(clean_path, index=False)
print(f"  Clean dataset saved -> {clean_path} | Shape: {df_clean.shape} | Nulls: {df_clean.isnull().sum().sum()}")

# =============================================================================
# 4. EXPLORATORY DATA VISUALIZATIONS
# =============================================================================
print("\n[SECTION 4] Generating Production Visualizations...")

COLORS = ['#2563EB', '#7C3AED', '#059669', '#D97706', '#DC2626']

# 4.1 Bar Chart: Revenue by Category
cat_rev = (df_clean.groupby('Category', observed=False)['Revenue']
           .sum().sort_values(ascending=False).reset_index())
fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(cat_rev['Category'], cat_rev['Revenue'] / 1e6,
              color=COLORS, width=0.55, edgecolor='black', alpha=0.85)
for bar in bars:
    y = bar.get_height()
    ax.annotate(f'${y:.2f}M', (bar.get_x() + bar.get_width() / 2, y + 0.04),
                ha='center', va='bottom', fontsize=10, fontweight='bold')
ax.set_title('Total Revenue by Product Category (2023)', fontsize=14, fontweight='bold', pad=12)
ax.set_ylabel('Total Revenue (Million $)', fontsize=11)
ax.set_ylim(0, cat_rev['Revenue'].max() / 1e6 * 1.20)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'bar_revenue_by_category.png'), dpi=150)
plt.close()

# 4.2 Line Chart: Monthly Revenue Trend
monthly = df_clean.set_index('Date').resample('ME')['Revenue'].sum().reset_index()
monthly['MonthLabel'] = monthly['Date'].dt.strftime('%b')
fig, ax = plt.subplots(figsize=(11, 5))
ax.plot(monthly['MonthLabel'], monthly['Revenue'] / 1e3,
        marker='o', color='#2563EB', linewidth=2.5, markersize=7)
ax.fill_between(monthly['MonthLabel'], monthly['Revenue'] / 1e3,
                alpha=0.15, color='#2563EB')
mean_rev = monthly['Revenue'].mean() / 1e3
ax.axhline(mean_rev, color='#DC2626', linestyle='--', linewidth=1.5,
           label=f'Monthly Mean (${mean_rev:.1f}k)')
ax.set_title('Monthly Revenue Trajectory (2023)', fontsize=14, fontweight='bold', pad=12)
ax.set_ylabel('Revenue ($ Thousands)', fontsize=11)
ax.legend(frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'line_monthly_revenue.png'), dpi=150)
plt.close()

# 4.3 Histogram & KDE: Revenue Distribution
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(df_clean['Revenue'], kde=True, bins=30, ax=ax,
             color='#2563EB', edgecolor='white', alpha=0.7)
ax.axvline(df_clean['Revenue'].mean(), color='#DC2626', linestyle='--',
           linewidth=2, label=f"Mean: ${df_clean['Revenue'].mean():,.0f}")
ax.axvline(df_clean['Revenue'].median(), color='#059669', linestyle='-',
           linewidth=2, label=f"Median: ${df_clean['Revenue'].median():,.0f}")
ax.xaxis.set_major_formatter(mticker.StrMethodFormatter('${x:,.0f}'))
ax.set_title('Revenue Distribution (Histogram & KDE)', fontsize=14, fontweight='bold', pad=12)
ax.legend(frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'hist_revenue_distribution.png'), dpi=150)
plt.close()

# 4.4 Scatter Plot: Unit Price vs Revenue
fig, ax = plt.subplots(figsize=(9, 5.5))
sns.scatterplot(data=df_clean, x='UnitPrice', y='Revenue',
                hue='Category', size='UnitsSold', sizes=(30, 200),
                palette=COLORS, alpha=0.75, ax=ax)
m, b = np.polyfit(df_clean['UnitPrice'], df_clean['Revenue'], 1)
x_line = np.linspace(df_clean['UnitPrice'].min(), df_clean['UnitPrice'].max(), 100)
ax.plot(x_line, m * x_line + b, color='#DC2626', linestyle='--', linewidth=2,
        label=f'Trendline (r = {df_clean["UnitPrice"].corr(df_clean["Revenue"]):.2f})')
ax.xaxis.set_major_formatter(mticker.StrMethodFormatter('${x:,.0f}'))
ax.yaxis.set_major_formatter(mticker.StrMethodFormatter('${x:,.0f}'))
ax.set_title('Unit Price vs. Revenue by Category', fontsize=14, fontweight='bold', pad=12)
ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'scatter_price_vs_revenue.png'), dpi=150)
plt.close()

# 4.5 Box Plots: Region & Rating
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
sns.boxplot(data=df_clean, x='Region', y='Revenue', palette='Set2', ax=axes[0])
axes[0].yaxis.set_major_formatter(mticker.StrMethodFormatter('${x:,.0f}'))
axes[0].set_title('Revenue Spread by Region', fontsize=13, fontweight='bold')
sns.boxplot(data=df_clean, x='Category', y='Rating', palette='Pastel1', ax=axes[1])
axes[1].set_title('Customer Rating Spread by Category', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'boxplot_revenue_rating.png'), dpi=150)
plt.close()

# 4.6 Correlation Heatmap
num_cols = ['Age', 'UnitsSold', 'UnitPrice', 'DiscountPct', 'Revenue', 'Rating', 'Returned']
corr_matrix = df_clean[num_cols].corr()
fig, ax = plt.subplots(figsize=(8, 6.5))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='Blues',
            linewidths=0.5, linecolor='gray', vmin=-1, vmax=1, ax=ax)
ax.set_title('Pearson Correlation Matrix (Numerical Features)', fontsize=14, fontweight='bold', pad=12)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'heatmap_correlation.png'), dpi=150)
plt.close()

# 4.7 Pie & Stacked Bar: Payment Mode & Returns
fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))
pm_counts = df_clean['PaymentMode'].value_counts()
axes[0].pie(pm_counts, labels=pm_counts.index, autopct='%1.1f%%',
            colors=COLORS, startangle=140,
            wedgeprops={'edgecolor': 'white', 'linewidth': 2})
axes[0].set_title('Payment Mode Share', fontsize=13, fontweight='bold')

pm_return = (df_clean.groupby(['PaymentMode', 'Returned'], observed=False)
             .size().unstack(fill_value=0))
pm_return.rename(columns={0: 'Kept', 1: 'Returned'}, inplace=True)
pm_return.plot(kind='bar', stacked=True, color=['#059669', '#DC2626'],
               ax=axes[1], edgecolor='black', alpha=0.85)
axes[1].set_title('Order Outcome by Payment Mode', fontsize=13, fontweight='bold')
axes[1].set_ylabel('Number of Orders')
axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=30, ha='right')
axes[1].legend(title='Outcome', frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'pie_stacked_payments_returns.png'), dpi=150)
plt.close()

# 4.8 Multi-Feature KDE
fig, axes = plt.subplots(2, 3, figsize=(14, 8))
axes = axes.flatten()
features_to_plot = ['Age', 'UnitsSold', 'UnitPrice', 'DiscountPct', 'Revenue', 'Rating']
plot_colors = ['#2563EB', '#7C3AED', '#059669', '#D97706', '#DC2626', '#0891B2']
for i, col in enumerate(features_to_plot):
    sns.kdeplot(df_clean[col], ax=axes[i], color=plot_colors[i], fill=True, alpha=0.35, linewidth=2)
    axes[i].set_title(f'KDE — {col}', fontweight='bold', fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'kde_all_features.png'), dpi=150)
plt.close()

# 4.9 Pearson vs Spearman
corr_p = df_clean[num_cols].corr(method='pearson')
corr_s = df_clean[num_cols].corr(method='spearman')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
sns.heatmap(corr_p, annot=True, fmt='.2f', cmap='coolwarm', vmin=-1, vmax=1, ax=ax1, cbar=False)
ax1.set_title('Pearson Correlation (Linear)', fontsize=12, fontweight='bold')
sns.heatmap(corr_s, annot=True, fmt='.2f', cmap='coolwarm', vmin=-1, vmax=1, ax=ax2)
ax2.set_title('Spearman Correlation (Monotonic Rank)', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'heatmap_pearson_vs_spearman.png'), dpi=150)
plt.close()

# 4.10 Comprehensive 6-Panel Dashboard
fig = plt.figure(figsize=(18, 12))
fig.suptitle('Retail Sales — Comprehensive Analysis Dashboard',
             fontsize=16, fontweight='bold', y=1.01)

# Panel 1: Revenue by Category
ax1 = fig.add_subplot(2, 3, 1)
cat_r = df_clean.groupby('Category', observed=False)['Revenue'].sum() / 1e6
ax1.bar(cat_r.index, cat_r.values, color=COLORS, edgecolor='black', alpha=0.85)
ax1.set_title('Total Revenue by Category ($M)', fontweight='bold')
ax1.set_ylabel('Revenue ($M)')
ax1.tick_params(axis='x', rotation=30)

# Panel 2: Monthly Trajectory
ax2 = fig.add_subplot(2, 3, 2)
monthly_k = df_clean.set_index('Date').resample('ME')['Revenue'].sum() / 1e3
ax2.plot(monthly_k.index.strftime('%b'), monthly_k.values,
         marker='o', color='#2563EB', linewidth=2)
ax2.set_title('Monthly Revenue Trend ($K)', fontweight='bold')
ax2.set_ylabel('Revenue ($K)')
ax2.tick_params(axis='x', rotation=45)

# Panel 3: Revenue Histogram + KDE
ax3 = fig.add_subplot(2, 3, 3)
sns.histplot(df_clean['Revenue'], kde=True, bins=25, ax=ax3,
             color='#7C3AED', edgecolor='white', alpha=0.6)
ax3.xaxis.set_major_formatter(mticker.StrMethodFormatter('${x:,.0f}'))
ax3.set_title('Revenue Distribution & KDE', fontweight='bold')
ax3.tick_params(axis='x', rotation=30)

# Panel 4: Unit Price vs. Revenue
ax4 = fig.add_subplot(2, 3, 4)
sns.scatterplot(data=df_clean, x='UnitPrice', y='Revenue', hue='Category',
                palette=COLORS, alpha=0.7, ax=ax4, legend=False)
ax4.set_title('Unit Price vs. Revenue', fontweight='bold')
ax4.xaxis.set_major_formatter(mticker.StrMethodFormatter('${x:,.0f}'))
ax4.yaxis.set_major_formatter(mticker.StrMethodFormatter('${x:,.0f}'))

# Panel 5: Revenue by Region Boxplot
ax5 = fig.add_subplot(2, 3, 5)
sns.boxplot(data=df_clean, x='Region', y='Revenue', palette='Set2', ax=ax5)
ax5.yaxis.set_major_formatter(mticker.StrMethodFormatter('${x:,.0f}'))
ax5.set_title('Revenue Spread by Region', fontweight='bold')

# Panel 6: Payment Mode & Returns
ax6 = fig.add_subplot(2, 3, 6)
pm_ret = (df_clean.groupby('PaymentMode', observed=False)['Returned']
          .mean() * 100).sort_values(ascending=False)
bars6 = ax6.bar(pm_ret.index, pm_ret.values, color='#DC2626', alpha=0.75, edgecolor='black')
for b in bars6:
    ax6.annotate(f'{b.get_height():.1f}%',
                 (b.get_x() + b.get_width() / 2, b.get_height() + 0.3),
                 ha='center', va='bottom', fontsize=9, fontweight='bold')
ax6.set_title('Return Rate by Payment Mode (%)', fontweight='bold')
ax6.set_ylabel('Return Rate (%)')
ax6.tick_params(axis='x', rotation=30)

plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'dashboard_comprehensive.png'), dpi=150, bbox_inches='tight')
plt.close()

print("  All 10 production figures rendered and saved successfully.")

# =============================================================================
# 5. STATISTICAL ANALYSIS & OUTLIER DETECTION
# =============================================================================
print("\n[SECTION 5] Performing Statistical Analysis & Outlier Detection...")
q1 = df_clean['Revenue'].quantile(0.25)
q3 = df_clean['Revenue'].quantile(0.75)
iqr = q3 - q1
upper_fence = q3 + 1.5 * iqr
iqr_outliers = df_clean[df_clean['Revenue'] > upper_fence]
print(f"  Revenue IQR: Q1=${q1:,.2f} | Q3=${q3:,.2f} | IQR=${iqr:,.2f}")
print(f"  Tukey Upper Fence: ${upper_fence:,.2f} | Outliers detected: {len(iqr_outliers)}")

z_scores = np.abs((df_clean['Revenue'] - df_clean['Revenue'].mean()) / df_clean['Revenue'].std())
z_outliers = df_clean[z_scores > 3.0]
print(f"  Z-Score (|Z| > 3.0) outliers detected: {len(z_outliers)}")

# =============================================================================
# 6. MACHINE LEARNING PREPROCESSING & PIPELINE SPLIT
# =============================================================================
print("\n[SECTION 6] Scikit-Learn Feature Engineering & Train-Test Split...")
df_ml = df_clean.copy()
le = LabelEncoder()
for col in ['Category', 'Region', 'Gender', 'PaymentMode']:
    df_ml[col] = le.fit_transform(df_ml[col].astype(str))

features = ['Category', 'Region', 'Gender', 'PaymentMode', 'Age',
            'UnitsSold', 'UnitPrice', 'DiscountPct', 'Revenue']
X = df_ml[features]
y = df_ml['Returned']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

print(f"  Training set size : {X_train.shape[0]} samples (80%)")
print(f"  Test set size     : {X_test.shape[0]} samples (20%)")
print(f"  Train mean after scaling: {np.mean(X_train_scaled):.4f} | Std: {np.std(X_train_scaled):.4f}")

print("\n" + "=" * 65)
print("  DATA LAB TASKS COMPLETED SUCCESSFULLY")
print("=" * 65)
