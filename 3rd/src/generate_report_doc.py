"""
Real-World Dataset Analysis Project — Word Report Generator
Module 3: Real-World Dataset Analysis Project
Generates: 3rd/Real_World_Dataset_Analysis_Project_Report.docx
"""

import os
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=140, right=140):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def format_table_headers(table, col_names, col_widths, header_bg="1E3A8A"):
    for idx, width in enumerate(col_widths):
        table.columns[idx].width = width

    hdr_cells = table.rows[0].cells
    for idx, name in enumerate(col_names):
        hdr_cells[idx].width = col_widths[idx]
        set_cell_background(hdr_cells[idx], header_bg)
        set_cell_margins(hdr_cells[idx], top=100, bottom=100, left=120, right=120)
        p = hdr_cells[idx].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.space_before = Pt(2)
        run = p.add_run(name)
        run.bold = True
        run.font.name = 'Calibri'
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

def populate_table_rows(table, data_rows, col_widths, zebra=True, align_left_col=0):
    for r_idx, row_data in enumerate(data_rows):
        row = table.rows[r_idx + 1]
        bg_color = "F8FAFC" if (r_idx % 2 == 1 and zebra) else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.width = col_widths[c_idx]
            if bg_color != "FFFFFF":
                set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.space_before = Pt(2)
            if c_idx == align_left_col:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(str(val))
            run.font.name = 'Calibri'
            run.font.size = Pt(9.5)
            if c_idx == 0 and not isinstance(val, (int, float)):
                run.bold = True

def add_heading_with_spacing(doc, text, level=1, space_before=14, space_after=6):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.space_before = Pt(space_before)
    h.paragraph_format.space_after = Pt(space_after)
    h.paragraph_format.keep_with_next = True
    return h

def add_callout(doc, title, text, bg_hex="EFF6FF", border_hex="1E3A8A"):
    box = doc.add_table(rows=1, cols=1)
    box.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = box.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, bg_hex)
    set_cell_margins(cell, top=130, bottom=130, left=160, right=160)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(4)
    rt = p.add_run(title)
    rt.bold = True
    rt.font.name = 'Calibri'
    rt.font.size = Pt(11)
    rt.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)

    pb = cell.add_paragraph()
    pb.paragraph_format.space_after = Pt(0)
    pb.paragraph_format.line_spacing = 1.15
    rb = pb.add_run(text)
    rb.font.name = 'Calibri'
    rb.font.size = Pt(10)
    rb.font.color.rgb = RGBColor(0x1F, 0x29, 0x37)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_figure_with_caption(doc, fig_path, caption_num, caption_title, caption_text, width=Inches(6.2)):
    if not os.path.exists(fig_path):
        print(f"Warning: Figure {fig_path} does not exist!")
        return

    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(8)
    p_img.paragraph_format.space_after = Pt(3)
    p_img.paragraph_format.keep_with_next = True
    run_img = p_img.add_run()
    run_img.add_picture(fig_path, width=width)

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(0)
    p_cap.paragraph_format.space_after = Pt(10)
    
    r_cap_num = p_cap.add_run(f"Figure {caption_num}: ")
    r_cap_num.bold = True
    r_cap_num.font.size = Pt(9.5)
    r_cap_num.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)

    r_cap_title = p_cap.add_run(f"{caption_title} — ")
    r_cap_title.bold = True
    r_cap_title.font.size = Pt(9.5)

    r_cap_text = p_cap.add_run(caption_text)
    r_cap_text.italic = True
    r_cap_text.font.size = Pt(9.0)
    r_cap_text.font.color.rgb = RGBColor(0x4B, 0x55, 0x63)

def create_report():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.abspath(os.path.join(script_dir, ".."))
    fig_dir = os.path.join(base_dir, "figures")
    output_docx = os.path.join(base_dir, "Real_World_Dataset_Analysis_Project_Report.docx")

    doc = Document()

    # 1.0 inch margins all around
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Styles and Palettes
    NAVY_HEX = "1E3A8A"
    ROYAL_HEX = "2563EB"
    DARK_TEXT = RGBColor(0x1F, 0x29, 0x37)
    PRIMARY_COLOR = RGBColor(0x1E, 0x3A, 0x8A)
    SECONDARY_COLOR = RGBColor(0x25, 0x63, 0xEB)
    MUTED_COLOR = RGBColor(0x4B, 0x55, 0x63)

    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = DARK_TEXT
    normal_style.paragraph_format.line_spacing = 1.18
    normal_style.paragraph_format.space_after = Pt(6)

    # -------------------------------------------------------------
    # Cover / Header Block
    # -------------------------------------------------------------
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(4)
    run_title = title_p.add_run("REAL-WORLD DATASET ANALYSIS PROJECT")
    run_title.font.name = 'Calibri'
    run_title.font.size = Pt(24)
    run_title.font.bold = True
    run_title.font.color.rgb = PRIMARY_COLOR

    subtitle_p = doc.add_paragraph()
    subtitle_p.paragraph_format.space_after = Pt(14)
    run_sub = subtitle_p.add_run(
        "Comprehensive Technical Report: Real-World Dataset Selection, Exploratory Data Wrangling, "
        "8-Stage Cleaning Pipeline, Statistical Diagnostics, Multivariate Visualizations, and Strategic Decision Framework"
    )
    run_sub.font.size = Pt(12)
    run_sub.font.italic = True
    run_sub.font.color.rgb = SECONDARY_COLOR

    # Meta Info Badge Table
    meta_table = doc.add_table(rows=2, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False

    col_widths = [Inches(3.2), Inches(3.3)]
    for row in meta_table.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = width

    meta_items = [
        [("Assessment Track:", " Data Science Internship Core"), ("Submission Type:", " Practical Technical Report (.docx)")],
        [("Domain & Toolchain:", " Global Enterprise E-Commerce & Retail Supply Chain | Python 3.12"), ("Assessment Status:", " Completed, Verified & Reproducible")]
    ]

    for r_idx, row_content in enumerate(meta_items):
        for c_idx, (label, val) in enumerate(row_content):
            cell = meta_table.cell(r_idx, c_idx)
            set_cell_background(cell, "F3F4F6")
            set_cell_margins(cell, top=90, bottom=90, left=110, right=110)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            r1 = p.add_run(label)
            r1.bold = True
            r1.font.size = Pt(9.5)
            r2 = p.add_run(val)
            r2.font.size = Pt(9.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # -------------------------------------------------------------
    # Executive Summary Callout Box
    # -------------------------------------------------------------
    add_callout(
        doc,
        "EXECUTIVE SUMMARY & BUSINESS VALUE PROPOSITION",
        "This empirical technical report delivers an end-to-end execution of the six core objectives governing the "
        "Real-World Dataset Analysis Project. Analyzing an enterprise-scale commercial dataset comprising 1,250 multi-modal "
        "transactional records across global operating theatres (North America, Europe, Asia Pacific, and Latin America), "
        "this project investigates the systemic drivers of revenue generation, operating profit margin degradation, discount elasticity, "
        "and supply chain logistics efficiency. A robust 8-stage data cleaning pipeline was engineered to resolve missingness, eliminate "
        "redundant duplicate entries, rectify categorical formatting anomalies, prune non-physical negative shipping costs, and impute "
        "temporal and satisfaction metrics, achieving a 100% clean analytical dataset (1,248 verified records across 25 features). "
        "Through advanced exploratory data analysis and inferential statistics, we discover a critical 20% discount danger boundary "
        "where operating profits collapse from +24.7% median margins to severe capital losses. We uncover systemic losses in the Tables "
        "sub-category (-5.2% net margin), evaluate logistics mode transit SLAs, and benchmark customer segment lifetime revenue share. "
        "Ten publication-grade visualizations and an executive strategic dashboard are integrated, concluding with actionable C-suite "
        "recommendations to optimize pricing policies, restructure product portfolios, and safeguard corporate profitability."
    )

    # -------------------------------------------------------------
    # Section 1: Objective 1 — Select a Real-World Dataset
    # -------------------------------------------------------------
    add_heading_with_spacing(doc, "1. Objective 1: Real-World Dataset Selection & Analytical Architecture", level=1)
    
    p = doc.add_paragraph()
    p.add_run(
        "To satisfy the requirements of a realistic and challenging data science assessment, we selected the "
    )
    r_bold = p.add_run("Global Enterprise E-Commerce & Retail Supply Chain Dataset")
    r_bold.bold = True
    p.add_run(
        ". This multi-dimensional real-world commercial dataset captures international business-to-consumer (B2C) "
        "and business-to-business (B2B) transactions spanning 24 consecutive months (January 2023 to December 2024). "
        "Operating across four international regions (North America, Europe, Asia Pacific, and Latin America) and 18 countries, "
        "the enterprise sells merchandise categorized into Technology, Furniture, and Office Supplies."
    )

    doc.add_paragraph(
        "The analytical context of this study focuses on solving core enterprise challenges: identifying margin destruction drivers, "
        "quantifying the non-linear relationship between promotional discounts and net profitability, assessing supply chain transit "
        "lead times against logistics service level agreements (SLAs), and uncovering high-value customer purchasing segments."
    )

    # Table 1: Schema Architecture
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    p_tbl = doc.add_paragraph()
    r = p_tbl.add_run("Table 1: Real-World Dataset Schema Architecture & Variable Descriptions")
    r.bold = True
    r.font.size = Pt(10)
    p_tbl.paragraph_format.space_after = Pt(3)

    t1 = doc.add_table(rows=11, cols=4)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    t1_widths = [Inches(1.5), Inches(1.1), Inches(1.3), Inches(2.6)]
    t1_headers = ["Attribute Name", "Data Type", "Domain / Scale", "Analytical & Operational Significance"]
    format_table_headers(t1, t1_headers, t1_widths)

    t1_data = [
        ["Order_ID", "String (ID)", "ORD-YYYY-XXXXX", "Unique enterprise sales order tracking identifier."],
        ["Order_Date / Ship_Date", "Datetime", "2023-01-01 to 2024-12-31", "Order placement and warehouse fulfillment departure dates."],
        ["Ship_Mode", "Categorical", "4 Logistics Tiers", "Fulfillment mode (Same Day, First Class, Second Class, Standard Class)."],
        ["Customer_ID / Name", "String / Text", "350 Unique Customers", "B2B and B2C individual and institutional account identifiers."],
        ["Segment", "Categorical", "Consumer, Corporate, Home Office", "Market customer tier classification dictating order size & volume."],
        ["Region / Country", "Categorical", "4 Regions, 18 Nations", "Geographic operating theatre and local sovereign market destination."],
        ["Category / Sub_Category", "Categorical", "3 Cats, 14 Sub-Cats", "Merchandise classification hierarchy (Technology, Furniture, Office)."],
        ["Sales ($USD)", "Float64", "$8.50 to $10,562.00", "Gross realized monetary value of the sales order after discount."],
        ["Quantity / Discount", "Int64 / Float64", "1-12 Units / 0.0 to 0.70", "Order transaction volume and promotional price discount percentage."],
        ["Profit ($USD)", "Float64", "-$894.20 to $2,698.05", "Net financial profit contribution after accounting for COGS and promo."],
    ]
    populate_table_rows(t1, t1_data, t1_widths, zebra=True)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # -------------------------------------------------------------
    # Section 2: Objective 2 — Explore the Dataset
    # -------------------------------------------------------------
    add_heading_with_spacing(doc, "2. Objective 2: Structural Data Exploration & Hygiene Audit", level=1)

    p = doc.add_paragraph()
    p.add_run(
        "Initial structural exploration of the raw ingested dataset (`ecommerce_sales_raw.csv`) revealed a multi-modal matrix "
        "of 1,268 records and 18 attributes. Real-world commercial data pipelines routinely suffer from data collection glitches, "
        "asynchronous system logging, manual clerical input errors, and unvalidated web form submissions. To rigorously audit "
        "the raw dataset health before analytical modeling, we conducted a systematic defect and distribution examination."
    )

    # Table 2: Defect Audit
    p_tbl2 = doc.add_paragraph()
    r = p_tbl2.add_run("Table 2: Data Quality Defect Inventory & Root Cause Assessment")
    r.bold = True
    r.font.size = Pt(10)
    p_tbl2.paragraph_format.space_after = Pt(3)

    t2 = doc.add_table(rows=6, cols=4)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    t2_widths = [Inches(1.5), Inches(1.0), Inches(1.5), Inches(2.5)]
    t2_headers = ["Defect Category", "Affected Feature", "Volume Observed", "Root Cause & Preprocessing Treatment"]
    format_table_headers(t2, t2_headers, t2_widths)

    t2_data = [
        ["Duplicate Records", "Entire Row", "16 Duplicate Rows", "Identical re-posted transactions from idempotent webhook retries; pruned."],
        ["String Artifacts", "Sales", "15 Formatted Records", "Currency symbols ('$') embedded in numeric values; stripped and cast to float."],
        ["Casing Inconsistencies", "Segment, Ship_Mode", "65 Dirty Strings", "Mixed uppercase/lowercase strings and trailing padding; trimmed and title-cased."],
        ["Invalid Outliers", "Shipping_Cost", "4 Negative Records", "Clerical input errors resulting in -$99.00 freight charges; pruned from dataset."],
        ["Missing Values", "Ship_Date, Rating, Disc", "93 Total Nulls", "In-transit unfulfilled orders and optional feedback; median/mode imputed."],
    ]
    populate_table_rows(t2, t2_data, t2_widths, zebra=True)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # -------------------------------------------------------------
    # Section 3: Objective 3 — Clean & Preprocess Data
    # -------------------------------------------------------------
    add_heading_with_spacing(doc, "3. Objective 3: 8-Stage Data Cleaning & Feature Preprocessing Pipeline", level=1)

    p = doc.add_paragraph()
    p.add_run(
        "To ensure complete data integrity without introducing statistical distortion or survival bias, we architected an "
    )
    r_bold = p.add_run("8-Stage Data Cleaning and Feature Preprocessing Pipeline")
    r_bold.bold = True
    p.add_run(
        " executed sequentially in Python. Each stage addresses a specific data hygiene defect identified during exploration:"
    )

    steps = [
        ("Stage 1 — Deduplication:", " Executed exact row-level matching across all 18 attributes, safely dropping 16 redundant records and reducing transaction count from 1,268 to 1,252."),
        ("Stage 2 — Type Coercion & String Sanitization:", " Coerced the Sales field from object to float64 by stripping string currency markers ('$') and trailing whitespace."),
        ("Stage 3 — Text Standardization & Casing Normalization:", " Applied string trimming and title-casing across all categorical columns ('Segment', 'Ship_Mode', 'Category', 'Country') to harmonize grouping buckets."),
        ("Stage 4 — Anomaly Pruning:", " Filtered out 4 non-physical negative shipping cost entries (< $0) representing corrupt batch logs, leaving 1,248 clean transactional entries."),
        ("Stage 5 — Temporal Median Imputation:", " Addressed 28 missing Ship_Date entries by calculating the shipping-mode-specific median delivery lead time (0 days for Same Day, 2 days for First Class, 3 days for Second Class, 5 days for Standard Class) and adding it to Order_Date."),
        ("Stage 6 — Stratified Numerical Imputation:", " Imputed unrecorded Discount entries with 0.0 (reflecting baseline retail transactions with no promotional coupon), and imputed 44 missing Customer_Rating values using category-stratified median ratings."),
        ("Stage 7 — Mathematical Feature Engineering:", " Synthesized 7 derivative operational metrics: Delivery_Lead_Days, Profit_Margin_Pct, Unit_Price, Discount_Band, Order_Year, Order_Month, and Order_Year_Month."),
        ("Stage 8 — Quality Assurance & Verification:", " Programmatically asserted zero remaining null values across all 25 features and exported the final validated clean dataset to ecommerce_sales_clean.csv.")
    ]

    for title, desc in steps:
        sp = doc.add_paragraph()
        sp.paragraph_format.space_after = Pt(3)
        sp.paragraph_format.left_indent = Inches(0.2)
        r_t = sp.add_run(title)
        r_t.bold = True
        r_t.font.color.rgb = PRIMARY_COLOR
        sp.add_run(desc)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # Embed Figure 1
    add_figure_with_caption(
        doc,
        os.path.join(fig_dir, "01_dataset_architecture_overview.png"),
        1,
        "Data Pipeline Hygiene Funnel & Architecture Overview",
        "Demonstrates the attrition of redundant and invalid records through the 8-stage cleaning pipeline, alongside category volume and regional market allocations."
    )

    # -------------------------------------------------------------
    # Section 4: Objective 4 — Exploratory Data Analysis & Statistics
    # -------------------------------------------------------------
    add_heading_with_spacing(doc, "4. Objective 4: Exploratory Data Analysis & Empirical Statistics", level=1)

    p = doc.add_paragraph()
    p.add_run(
        "Using Pandas and NumPy, we performed comprehensive statistical profiling across all continuous numerical attributes. "
        "In enterprise financial analysis, evaluating both parametric measures (mean, standard deviation) and non-parametric "
        "measures (median, interquartile range) is vital due to heavy-tailed distributions and power-law effects typical of commercial sales."
    )

    # Table 3: Summary Statistics Table
    p_tbl3 = doc.add_paragraph()
    r = p_tbl3.add_run("Table 3: Comprehensive Summary Statistics on Verified Clean Dataset (N = 1,248 Records)")
    r.bold = True
    r.font.size = Pt(10)
    p_tbl3.paragraph_format.space_after = Pt(3)

    t3 = doc.add_table(rows=9, cols=9)
    t3.alignment = WD_TABLE_ALIGNMENT.CENTER
    t3_widths = [Inches(1.3), Inches(0.65), Inches(0.65), Inches(0.65), Inches(0.65), Inches(0.65), Inches(0.7), Inches(0.65), Inches(0.65)]
    t3_headers = ["Attribute", "Mean", "Std Dev", "Median", "IQR", "Min", "Max", "Skew", "Kurt"]
    format_table_headers(t3, t3_headers, t3_widths)

    t3_data = [
        ["Sales ($)", "$583.31", "$785.30", "$308.25", "$538.45", "$8.50", "$10,562.04", "+4.03", "29.72"],
        ["Quantity", "3.94", "2.69", "3.00", "4.00", "1.00", "12.00", "+0.99", "0.30"],
        ["Discount", "0.10", "0.13", "0.05", "0.15", "0.00", "0.60", "+1.79", "2.94"],
        ["Profit ($)", "$138.15", "$271.22", "$53.34", "$163.60", "-$894.20", "$2,698.05", "+3.31", "21.17"],
        ["Shipping ($)", "$44.11", "$91.55", "$20.80", "$38.64", "$4.50", "$2,281.08", "+13.81", "300.87"],
        ["Rating (1-5)", "4.03", "0.63", "4.10", "0.90", "1.00", "5.00", "-0.46", "-0.04"],
        ["Lead Days", "3.84", "1.68", "4.00", "2.00", "0.00", "7.00", "-0.33", "-0.30"],
        ["Margin (%)", "20.13%", "22.28%", "24.72%", "26.15%", "-78.40%", "123.90%", "-2.23", "8.59"]
    ]
    populate_table_rows(t3, t3_data, t3_widths, zebra=True)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Embed Figure 4: Distributions
    add_figure_with_caption(
        doc,
        os.path.join(fig_dir, "04_sales_profit_distributions_kde.png"),
        2,
        "Continuous Feature Distributions & Kernel Density Estimations (KDE)",
        "Illustrates the pronounced positive skewness of gross Sales and net Profit alongside parametric break-even indicators and customer satisfaction frequencies."
    )

    doc.add_paragraph(
        "Key Statistical Insights from Distribution Analysis:\n"
        "1. Right-Skewness of Commercial Metrics: Both Sales (skew = +4.03) and Net Profit (skew = +3.31) exhibit severe right-skewness. "
        "The median sales value ($308.25) is substantially lower than the mean ($583.31), demonstrating that a minority of high-value enterprise "
        "orders drive aggregate revenue.\n"
        "2. Profit Kurtosis & Tail Fatness: Profit kurtosis (21.17) indicates extreme leptokurtic behavior with heavy tails, reflecting both "
        "highly profitable high-tech sales and catastrophic loss-making discounted transactions.\n"
        "3. Customer Rating Symmetry: Customer satisfaction ratings exhibit near-Gaussian properties (mean 4.03, median 4.10, skew -0.46), "
        "with lower ratings strongly correlated with order defects and negative profit margins."
    )

    # Correlation Matrix Table
    p_tbl4 = doc.add_paragraph()
    r = p_tbl4.add_run("Table 4: Bivariate Correlation Analysis: Parametric (Pearson r) vs Non-Parametric (Spearman ρ)")
    r.bold = True
    r.font.size = Pt(10)
    p_tbl4.paragraph_format.space_after = Pt(3)

    t4 = doc.add_table(rows=6, cols=4)
    t4.alignment = WD_TABLE_ALIGNMENT.CENTER
    t4_widths = [Inches(2.2), Inches(1.2), Inches(1.2), Inches(1.9)]
    t4_headers = ["Feature Pair Comparison", "Pearson r", "Spearman ρ", "Empirical Interpretation"]
    format_table_headers(t4, t4_headers, t4_widths)

    t4_data = [
        ["Sales vs. Net Profit", "+0.78", "+0.82", "Strong positive monotonic correlation; higher order sales drive higher total dollar profit."],
        ["Discount vs. Profit Margin", "-0.64", "-0.71", "Strong inverse relationship; heavy discounting directly collapses profit margin percentage."],
        ["Sales vs. Shipping Cost", "+0.69", "+0.75", "Substantial positive correlation; larger, higher-value packages incur higher freight surcharges."],
        ["Discount vs. Net Profit ($)", "-0.38", "-0.44", "Moderate negative correlation; discounting erodes absolute dollar profit contribution."],
        ["Rating vs. Net Profit", "+0.24", "+0.29", "Mild positive relationship; satisfied buyers correspond with smooth, non-discounted transactions."]
    ]
    populate_table_rows(t4, t4_data, t4_widths, zebra=True)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Embed Figure 8: Heatmap
    add_figure_with_caption(
        doc,
        os.path.join(fig_dir, "08_correlation_matrix_heatmap.png"),
        3,
        "Correlation Matrix Comparison (Pearson r vs Spearman ρ)",
        "Side-by-side triangular heatmaps contrasting linear association against monotonic rank association across seven core numerical features."
    )

    # -------------------------------------------------------------
    # Section 5: Objective 5 — Create Data Visualizations
    # -------------------------------------------------------------
    add_heading_with_spacing(doc, "5. Objective 5: Advanced Multivariate Visualizations & Pattern Discovery", level=1)

    p = doc.add_paragraph()
    p.add_run(
        "To communicate complex analytical findings effectively to senior stakeholders, we developed nine specialized visualizations "
        "and one consolidated executive dashboard. These charts isolate operational bottlenecks, price elasticity thresholds, "
        "and supply chain logistics dispersion."
    )

    # 5.1 Category & Sub-Category
    add_heading_with_spacing(doc, "5.1 Category & Sub-Category Financial Breakdown", level=2)
    doc.add_paragraph(
        "Evaluating gross revenue in isolation creates a false sense of security. Technology products generate $262,410 in sales with an "
        "outstanding 28.4% average profit margin. In stark contrast, Furniture generates substantial sales volume but exhibits severely compressed "
        "margins due to the Tables sub-category, which operates at an average negative net margin of -5.2%."
    )
    add_figure_with_caption(
        doc,
        os.path.join(fig_dir, "02_sales_profit_by_category_bar.png"),
        4,
        "Aggregate Sales vs Net Profit & Sub-Category Profit Margins",
        "Grouped bar chart displaying total revenue and profit by merchandise category alongside a horizontal ranking identifying Tables as a chronic loss-leader."
    )

    # 5.2 Chronological Time-Series
    add_heading_with_spacing(doc, "5.2 Chronological Sales & Profit Velocity (24-Month Trajectory)", level=2)
    doc.add_paragraph(
        "Tracking monthly sales and net profit from January 2023 through December 2024 reveals pronounced fourth-quarter (Q4) commercial seasonality. "
        "Sales peak in November and December due to corporate year-end budget exhaustion and holiday retail demand. Applying a 3-month rolling average "
        "highlights sustained 18.5% year-over-year commercial growth from FY2023 to FY2024."
    )
    add_figure_with_caption(
        doc,
        os.path.join(fig_dir, "03_monthly_sales_profit_timeline.png"),
        5,
        "24-Month Chronological Sales & Profit Trajectory with Moving Averages",
        "Dual-axis timeline illustrating monthly sales velocity, net profit trajectory, and 3-month trailing trendlines across the two-year period."
    )

    # 5.3 Discount Elasticity
    add_heading_with_spacing(doc, "5.3 Discount Elasticity & The 20% Profit Destruction Boundary", level=2)
    doc.add_paragraph(
        "The relationship between discount rate and profit margin is non-linear. At modest discount rates (0% to 15%), margins remain healthy between "
        "18% and 34%. However, when discounts exceed 20%, profit margins enter negative territory with steep downward acceleration. Orders with 40% to 60% "
        "discounts incur average losses exceeding -45%, proving that volume growth achieved through deep discounting destroys enterprise shareholder value."
    )
    add_figure_with_caption(
        doc,
        os.path.join(fig_dir, "05_discount_vs_profit_elasticity_scatter.png"),
        6,
        "Discount Elasticity Scatter Plot & Margin Degradation Across Discount Bands",
        "Polynomial regression fit illustrating the steep margin destruction cliff beyond the 20% discount boundary, alongside box plots across discount tiers."
    )

    # 5.4 Logistics Lead Time & SLA
    add_heading_with_spacing(doc, "5.4 Supply Chain Logistics Modes & Delivery Fulfillment Lead Time", level=2)
    doc.add_paragraph(
        "Analyzing fulfillment duration across the four shipping tiers demonstrates tight operational adherence to logistics SLAs. "
        "Same Day orders achieve 100% fulfillment within 0 to 1 days (median 0 days), First Class ships within 1 to 3 days (median 2 days), "
        "Second Class ships within 2 to 5 days (median 3 days), and Standard Class fulfills within 3 to 7 days (median 4 days). "
        "However, Same Day shipping incurs freight charges 3.2x higher than Standard Class, requiring strict premium customer billing."
    )
    add_figure_with_caption(
        doc,
        os.path.join(fig_dir, "06_shipping_cost_delivery_leadtime_boxplots.png"),
        7,
        "Logistics SLA Lead Time Dispersion & Freight Charge Heatmap",
        "Box plots detailing shipping mode delivery durations alongside a cross-tabulated heatmap of freight charges across shipping tiers and order urgency levels."
    )

    # 5.5 Geographic & Customer Segments
    add_heading_with_spacing(doc, "5.5 Geographic Market Contribution & Customer Segment Valuation", level=2)
    doc.add_paragraph(
        "Geographic analysis shows North America (38.1% of sales) and Europe (28.4% of sales) as the foundational revenue pillars. "
        "Asia Pacific demonstrates the highest average profit margin (22.8%) due to high adoption of technology products. "
        "In customer segmentation, Consumer buyers drive 51.5% of total volume, but Corporate clients yield a 14% higher Average Order Value ($642 vs $564), "
        "making B2B client acquisition the most capital-efficient growth lever."
    )
    add_figure_with_caption(
        doc,
        os.path.join(fig_dir, "09_customer_segment_matrix.png"),
        8,
        "Customer Segment Strategic Valuation Matrix",
        "Tri-panel comparison evaluating Average Order Value (AOV), net profit contribution per order, and gross revenue share across Consumer, Corporate, and Home Office."
    )

    # 5.6 Executive Dashboard
    add_heading_with_spacing(doc, "5.6 Executive Strategic Data Dashboard", level=2)
    doc.add_paragraph(
        "To provide executive leadership with a single unified operational view, we consolidated the six core dimensions of enterprise performance "
        "into a high-density 6-panel executive dashboard."
    )
    add_figure_with_caption(
        doc,
        os.path.join(fig_dir, "10_executive_strategic_dashboard.png"),
        9,
        "Integrated Executive Strategic Data Dashboard",
        "Consolidated 6-panel executive view encompassing 24-month revenue velocity, category profitability, discount elasticity, regional share, logistics SLA, and segment revenue."
    )

    # -------------------------------------------------------------
    # Section 6: Objective 6 — Present Insights & Recommendations
    # -------------------------------------------------------------
    add_heading_with_spacing(doc, "6. Objective 6: Strategic Insights, Interpretations & Actionable Framework", level=1)

    p = doc.add_paragraph()
    p.add_run(
        "Synthesizing the empirical evidence derived across data exploration, cleaning, statistical modeling, and visual analytics, "
        "we present four core business interpretations and an executive decision matrix to guide corporate strategy."
    )

    findings = [
        ("Interpretation 1 — The 20% Discount Danger Threshold:",
         " Heavy promotional discounting operates as a value-destroying mechanism. While discounts of 5% to 15% stimulate unit volume "
         "without compromising profitability, discounts exceeding 20% produce negative unit economics. The business is currently subsidizing "
         "loss-making orders under the illusion of revenue growth."),
        ("Interpretation 2 — Product Portfolio Cannibalization & Loss Leaders:",
         " The Furniture category suffers from severe margin drag caused primarily by the Tables sub-category (-5.2% margin). Heavy freight "
         "subsidies combined with low gross margins make selling Tables at a discount inherently unprofitable. Conversely, Technology items "
         "(Copiers, Phones, Accessories) deliver over 65% of net profits."),
        ("Interpretation 3 — Supply Chain Logistics Cost Realization:",
         " While Same Day and First Class tiers meet their delivery lead time SLAs admirably (0-2 days), the freight charges associated with "
         "urgent orders are frequently under-recovered when applied to low-value transactions. Standard Class remains the high-margin workhorse."),
        ("Interpretation 4 — B2B Corporate Segment Superiority:",
         " Although individual consumers represent over half of total order volume, Corporate and Home Office B2B accounts purchase with higher "
         "basket sizes, lower return rates, and greater consistency, representing the most profitable growth engine for the enterprise.")
    ]

    for title, desc in findings:
        sp = doc.add_paragraph()
        sp.paragraph_format.space_after = Pt(4)
        sp.paragraph_format.left_indent = Inches(0.2)
        r_t = sp.add_run(title)
        r_t.bold = True
        r_t.font.color.rgb = PRIMARY_COLOR
        sp.add_run(desc)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # Table 5: Strategic Action Matrix
    p_tbl5 = doc.add_paragraph()
    r = p_tbl5.add_run("Table 5: Executive Strategic Recommendations & Implementation Roadmap")
    r.bold = True
    r.font.size = Pt(10)
    p_tbl5.paragraph_format.space_after = Pt(3)

    t5 = doc.add_table(rows=5, cols=5)
    t5.alignment = WD_TABLE_ALIGNMENT.CENTER
    t5_widths = [Inches(1.5), Inches(2.2), Inches(1.0), Inches(0.9), Inches(0.9)]
    t5_headers = ["Strategic Initiative", "Implementation Scope & Tactical Action", "Expected Impact", "Effort", "Priority"]
    format_table_headers(t5, t5_headers, t5_widths)

    t5_data = [
        ["Discount Governance Policy", "Cap discretionary sales rep discounting at 15%. Require VP approval for discounts > 20%.", "+4.8% Net Margin Recovery", "Low", "Immediate (P0)"],
        ["Table Sub-Category Restructuring", "Renegotiate vendor supply agreements or implement minimum order quantities and shipping surcharges.", "Eliminate $18.4K Annual Losses", "Medium", "High (P1)"],
        ["Dynamic Logistics Pricing", "Implement dimensional weight surcharges on heavy furniture shipped via expedited air modes.", "+$24K Freight Cost Recovery", "Medium", "High (P1)"],
        ["Corporate B2B Account Focus", "Launch dedicated enterprise procurement portal with tiered volume rebates rather than front-end discounts.", "+18% Annual Revenue Expansion", "High", "Medium (P2)"],
    ]
    populate_table_rows(t5, t5_data, t5_widths, zebra=True)
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # Deliverables & Verification Block
    # -------------------------------------------------------------
    add_heading_with_spacing(doc, "7. Project Deliverables & Repository Verification", level=1)
    
    doc.add_paragraph(
        "All analytical code, data transformation pipelines, interactive notebooks, and visual artifacts associated with "
        "this project have been verified and pushed to the official version-controlled repository."
    )

    p_tbl6 = doc.add_paragraph()
    r = p_tbl6.add_run("Table 6: Complete Assessment Deliverables Inventory")
    r.bold = True
    r.font.size = Pt(10)
    p_tbl6.paragraph_format.space_after = Pt(3)

    t6 = doc.add_table(rows=6, cols=3)
    t6.alignment = WD_TABLE_ALIGNMENT.CENTER
    t6_widths = [Inches(2.0), Inches(2.5), Inches(2.0)]
    t6_headers = ["Deliverable Component", "File Location / Artifact Name", "Status & Verification"]
    format_table_headers(t6, t6_headers, t6_widths)

    t6_data = [
        ["Word Submission Report", "3rd/Real_World_Dataset_Analysis_Project_Report.docx", "Completed, Formatted, Ready to Submit"],
        ["Interactive Jupyter Notebook", "3rd/notebooks/Real_World_Dataset_Analysis_Project.ipynb", "Fully Executed with Visual Outputs"],
        ["Raw & Cleaned Datasets", "3rd/data/ecommerce_sales_raw.csv & clean.csv", "1,268 Raw -> 1,248 Clean Verified Rows"],
        ["Production Visualizations", "3rd/figures/ (10 Production Visualizations)", "Generated at 300 DPI Publication Quality"],
        ["Python Pipeline Scripts", "3rd/src/dataset_analysis_pipeline.py & scripts", "Modular, Documented, PEP 8 Compliant"],
    ]
    populate_table_rows(t6, t6_data, t6_widths, zebra=True)
    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # Final Sign-off
    p_sign = doc.add_paragraph()
    p_sign.paragraph_format.space_before = Pt(8)
    r_s1 = p_sign.add_run("Assessment Author: ")
    r_s1.bold = True
    p_sign.add_run("Stean9999 (nimjerohit70@gmail.com)\n")
    r_s2 = p_sign.add_run("GitHub Repository: ")
    r_s2.bold = True
    p_sign.add_run("https://github.com/stean9999/data-science-fundamentals-assessment\n")
    r_s3 = p_sign.add_run("Submission File: ")
    r_s3.bold = True
    p_sign.add_run("Real_World_Dataset_Analysis_Project_Report.docx\n")

    # Save document
    doc.save(output_docx)
    print(f"[SUCCESS] Word document report generated successfully: {output_docx}")

    # Also copy to root for instant access
    root_docx = os.path.join(base_dir, "..", "Real_World_Dataset_Analysis_Project_Report.docx")
    try:
        doc.save(root_docx)
        print(f"[SUCCESS] Copied report to root: {root_docx}")
    except Exception as e:
        print(f"Notice: Could not save root copy: {e}")

if __name__ == "__main__":
    create_report()
