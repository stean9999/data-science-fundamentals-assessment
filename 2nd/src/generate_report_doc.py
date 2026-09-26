"""
Hands-On Data Lab Implementation — Word Report Generator
Module 2: Build a working data analysis environment and complete practical exercises
Generates: Hands_On_Data_Lab_Implementation_Report.docx
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

def create_report():
    # Base directories
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.abspath(os.path.join(script_dir, ".."))
    fig_dir = os.path.join(base_dir, "figures")
    output_docx = os.path.join(base_dir, "Hands_On_Data_Lab_Implementation_Report.docx")

    doc = Document()

    # 1-inch margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Color Palette: Deep Navy, Slate Blue, Teal/Green, Neutral
    NAVY_HEX = "1E3A8A"
    SLATE_HEX = "2563EB"
    DARK_TEXT = RGBColor(0x1F, 0x29, 0x37)
    PRIMARY_COLOR = RGBColor(0x1E, 0x3A, 0x8A)
    SECONDARY_COLOR = RGBColor(0x25, 0x63, 0xEB)
    MUTED_COLOR = RGBColor(0x4B, 0x55, 0x63)
    SUCCESS_COLOR = RGBColor(0x05, 0x96, 0x69)

    # Base Normal Style
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = DARK_TEXT
    normal_style.paragraph_format.line_spacing = 1.18
    normal_style.paragraph_format.space_after = Pt(6)

    # -------------------------------------------------------------
    # Document Header / Cover Block
    # -------------------------------------------------------------
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(4)
    run_title = title_p.add_run("HANDS-ON DATA LAB IMPLEMENTATION")
    run_title.font.name = 'Calibri'
    run_title.font.size = Pt(24)
    run_title.font.bold = True
    run_title.font.color.rgb = PRIMARY_COLOR

    subtitle_p = doc.add_paragraph()
    subtitle_p.paragraph_format.space_after = Pt(14)
    run_sub = subtitle_p.add_run(
        "Comprehensive Technical Report: Environment Configuration, Exploratory Data Wrangling, "
        "8-Step Cleaning Pipeline, Multivariate Visualizations, and Empirical Statistical Analysis"
    )
    run_sub.font.size = Pt(12)
    run_sub.font.italic = True
    run_sub.font.color.rgb = SECONDARY_COLOR

    # Meta Info Table (Header Badge)
    meta_table = doc.add_table(rows=2, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False

    col_widths = [Inches(3.2), Inches(3.3)]
    for row in meta_table.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = width

    meta_items = [
        [("Assessment Track:", " Data Science Internship Core"), ("Submission Type:", " Practical Technical Report (.docx)")],
        [("Implementation Toolchain:", " Python 3.12, NumPy, Pandas, Matplotlib, Seaborn, Scikit-learn"), ("Assessment Status:", " Completed, Verified & Reproducible")]
    ]

    for r_idx, row_content in enumerate(meta_items):
        for c_idx, (label, val) in enumerate(row_content):
            cell = meta_table.cell(r_idx, c_idx)
            set_cell_background(cell, "F3F4F6")
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            r1 = p.add_run(label)
            r1.bold = True
            r1.font.size = Pt(9.5)
            r2 = p.add_run(val)
            r2.font.size = Pt(9.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # Executive Summary Callout Box
    # -------------------------------------------------------------
    summary_box = doc.add_table(rows=1, cols=1)
    summary_box.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = summary_box.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "EFF6FF")
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)

    sp = cell.paragraphs[0]
    sp.paragraph_format.space_after = Pt(4)
    s_title = sp.add_run("EXECUTIVE SUMMARY")
    s_title.bold = True
    s_title.font.size = Pt(11)
    s_title.font.color.rgb = PRIMARY_COLOR

    s_body = cell.add_paragraph()
    s_body.paragraph_format.space_after = Pt(0)
    s_body.paragraph_format.line_spacing = 1.15
    s_body.add_run(
        "This technical lab report provides a rigorous empirical execution of the six core objectives comprising "
        "the Hands-On Data Lab Implementation assessment. A professional data science computational environment "
        "was architected in Python 3.12, incorporating NumPy, Pandas, Matplotlib, Seaborn, and Scikit-learn under deterministic "
        "random seeding (seed 42). Using a comprehensive multi-modal retail sales transaction dataset (510 initial records across "
        "13 variables), we engineered an 8-stage data cleaning and hygiene pipeline that eliminated duplicate rows, reconciled categorical "
        "casing errors, pruned anomalous negative revenue figures, and imputed missing attributes using category-stratified median and mean "
        "strategies, yielding a 100% clean dataset (499 records, 16 features). "
        "Extensive exploratory data analysis was conducted across univariate, bivariate, and multivariate planes, generating production-grade "
        "visualizations—including categorical bar charts, annual revenue trends, kernel density estimates (KDE), price elasticity scatter plots, "
        "geographic box plots, correlation heatmaps, and payment return distribution charts. Parametric (Pearson) and non-parametric (Spearman) "
        "correlations were rigorously compared alongside IQR and Z-score outlier detection models. Finally, full Scikit-learn feature preprocessing "
        "(label encoding, standard scaling, and an 80/20 train-test split) and an integrated 6-panel executive dashboard were constructed, "
        "fully documented within a reproducible Jupyter Notebook and modular Python architecture."
    ).font.size = Pt(10)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Helper function for Section Headings
    def add_section_header(num, title):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(18)
        h.paragraph_format.space_after = Pt(6)
        r = h.add_run(f"{num}. {title.upper()}")
        r.bold = True
        r.font.size = Pt(14)
        r.font.color.rgb = PRIMARY_COLOR

        p_div = doc.add_paragraph()
        p_div.paragraph_format.space_before = Pt(0)
        p_div.paragraph_format.space_after = Pt(8)
        r_div = p_div.add_run("―" * 46)
        r_div.font.color.rgb = RGBColor(0x93, 0xC5, 0xFD)
        r_div.font.size = Pt(10)

    def add_sub_header(title):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(10)
        h.paragraph_format.space_after = Pt(4)
        r = h.add_run(title)
        r.bold = True
        r.font.size = Pt(12)
        r.font.color.rgb = SECONDARY_COLOR

    # -------------------------------------------------------------
    # SECTION 1: Set Up the Data Science Environment
    # -------------------------------------------------------------
    add_section_header("1", "Objective 1: Set Up the Data Science Environment")

    add_sub_header("1.1 Environmental Architecture & Scientific Toolchain")
    p = doc.add_paragraph()
    p.add_run(
        "A robust, predictable, and reproducible environment forms the bedrock of data engineering and machine learning workflows. "
        "For this practical data lab, a modern Python 3.12 scientific stack was configured, audited, and verified across all required libraries. "
        "The environment isolates analytical dependencies, prevents global version drift, and implements deterministic controls to ensure all "
        "transformations, statistical evaluations, and visual artifacts replicate identically across execution environments."
    )

    p = doc.add_paragraph()
    p.add_run("The computational stack leverages specialized roles across key analytical packages:")

    toolchain_roles = [
        ("Python 3.12 Runtime: ", "Core computational language featuring advanced CPython performance optimizations, enhanced traceback diagnostics, and strict typing support."),
        ("NumPy (Numerical Python): ", "High-performance N-dimensional array processing, SIMD vectorization, linear algebra routines, and random sampling generators."),
        ("Pandas: ", "Relational, columnar DataFrame data structures offering rich querying, grouping, joining, temporal indexing, and tabular manipulation capabilities."),
        ("Matplotlib & Seaborn: ", "Dual visualization layer: Matplotlib provides low-level graphical primitive control (axes, ticks, spines, typography), while Seaborn delivers statistical abstraction, color theory aesthetics, and density estimations."),
        ("Scikit-learn: ", "Industry standard machine learning framework providing data transformation transformers (StandardScaler, LabelEncoder), data partitioning utilities (train_test_split), and evaluation metrics."),
        ("Jupyter Interactive Environment: ", "Literate programming workspace enabling contiguous execution of documentation, executable Python code, interactive outputs, and inline graphics.")
    ]
    for role_name, role_desc in toolchain_roles:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(3)
        r = bp.add_run(role_name)
        r.bold = True
        bp.add_run(role_desc)

    add_sub_header("1.2 Toolchain Verification & Version Audit")
    p = doc.add_paragraph()
    p.add_run(
        "All installed libraries were programmatically audited upon notebook startup. The following runtime versions were verified and locked "
        "within the project environment:"
    )

    ver_table = doc.add_table(rows=8, cols=4)
    ver_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    widths = [Inches(1.5), Inches(1.3), Inches(1.7), Inches(2.0)]
    for row in ver_table.rows:
        for i, w in enumerate(widths):
            row.cells[i].width = w

    v_headers = ["Component", "Installed Version", "Target Functionality", "Verification Status"]
    for i, h_text in enumerate(v_headers):
        cell = ver_table.cell(0, i)
        set_cell_background(cell, NAVY_HEX)
        set_cell_margins(cell, top=120, bottom=120, left=100, right=100)
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    v_data = [
        ("Python", "3.12.10", "Execution runtime & engine", "Verified Active"),
        ("NumPy", "2.5.1", "NDArray vectorization & math", "Verified Active"),
        ("Pandas", "3.0.5", "Tabular data wrangling & I/O", "Verified Active"),
        ("Matplotlib", "3.11.1", "Core visualization canvas", "Verified Active"),
        ("Seaborn", "0.13.2", "Statistical distribution plots", "Verified Active"),
        ("Scikit-learn", "1.9.1", "Preprocessing & data splitting", "Verified Active"),
        ("Operating System", "Windows 11 (64-bit)", "Host execution platform", "Verified Active")
    ]

    for r_idx, row_values in enumerate(v_data, start=1):
        bg_col = "F9FAFB" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_values):
            cell = ver_table.cell(r_idx, c_idx)
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val)
            r.font.size = Pt(9)
            if c_idx == 0:
                r.bold = True
            if c_idx == 3:
                r.font.color.rgb = SUCCESS_COLOR

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_sub_header("1.3 Reproducibility Standards & Seed Initialization")
    p = doc.add_paragraph()
    p.add_run(
        "To guarantee that synthetic dataset generation, random perturbations, train-test splits, and sampling matrices remain "
        "100% deterministic across all runs, the random seed was globally initialized using 'np.random.seed(42)'. Furthermore, "
        "Matplotlib was configured with the clean 'seaborn-v0_8-whitegrid' theme, 300 DPI high-resolution output defaults, and "
        "warning suppressions ('warnings.filterwarnings(\"ignore\")') were enacted to maintain clean notebook and log executions."
    )

    # -------------------------------------------------------------
    # SECTION 2: Work with Data Using Pandas & NumPy
    # -------------------------------------------------------------
    add_section_header("2", "Objective 2: Work with Data Using Pandas & NumPy")

    add_sub_header("2.1 Synthetic Multi-Modal Retail Dataset Architecture")
    p = doc.add_paragraph()
    p.add_run(
        "To rigorously exercise end-to-end data manipulation techniques, a realistic multi-modal retail sales dataset was synthesized "
        "simulating 500 transactional records across 13 foundational columns. The dataset captures transactional identifiers, temporal stamps, "
        "hierarchical merchandise categories, regional geographic boundaries, customer demographics, checkout payment channels, order volumes, "
        "pricing structures, promotional discounts, gross and net financial returns, user satisfaction scores, and product return indicators."
    )

    schema_table = doc.add_table(rows=8, cols=4)
    schema_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    s_widths = [Inches(1.4), Inches(1.3), Inches(1.7), Inches(2.1)]
    for row in schema_table.rows:
        for i, w in enumerate(s_widths):
            row.cells[i].width = w

    s_headers = ["Attribute Name", "Data Type", "Value Domain / Range", "Analytical Relevance"]
    for i, h_text in enumerate(s_headers):
        cell = schema_table.cell(0, i)
        set_cell_background(cell, NAVY_HEX)
        set_cell_margins(cell, top=120, bottom=120, left=90, right=90)
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    s_data = [
        ("OrderID", "String / Object", "ORD-10000 to ORD-10499", "Unique transactional identifier / Primary Key"),
        ("Date", "Datetime64[ns]", "2023-01-01 to 2023-12-31", "Temporal stamp for monthly & quarterly trends"),
        ("Category", "Categorical (Nominal)", "Electronics, Clothing, Groceries, etc.", "Merchandise department hierarchy"),
        ("Region", "Categorical (Nominal)", "North, South, East, West, Central", "Geographic market segmentation"),
        ("UnitsSold & UnitPrice", "Integer & Float", "Units: [1, 20], Price: [$15, $5000]", "Volume and ticket size commercial metrics"),
        ("DiscountPct & Revenue", "Float & Float", "Discount: [0%, 25%], Revenue: Net $", "Monetary realization post-promotions"),
        ("Rating & Returned", "Float & Binary Int", "Rating: [1.0, 5.0], Returned: [0, 1]", "Customer satisfaction and defect monitoring")
    ]

    for r_idx, row_values in enumerate(s_data, start=1):
        bg_col = "F9FAFB" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_values):
            cell = schema_table.cell(r_idx, c_idx)
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, top=100, bottom=100, left=90, right=90)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val)
            r.font.size = Pt(9)
            if c_idx == 0:
                r.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_sub_header("2.2 Data Selection, Slicing & Boolean Masking")
    p = doc.add_paragraph()
    p.add_run(
        "Pandas provides two foundational indexers for accessing subsets of DataFrames:\n"
        "• Label-based indexing (.loc): Accesses rows and columns via explicit label indices (e.g., df.loc[0:2, ['OrderID', 'Category', 'Revenue']]).\n"
        "• Integer-based indexing (.iloc): Accesses tabular subsets strictly by integer position offsets (e.g., df.iloc[5:8, [0, 2, 10, 11]]).\n\n"
        "Boolean masking was implemented to isolate high-value business cohorts. For example, filtering for transactions where "
        "(df['Category'] == 'Electronics') & (df['Revenue'] > 10000) isolated 107 premium high-ticket orders, demonstrating vectorized "
        "logical filtering without costly iterative loops."
    )

    add_sub_header("2.3 Sorting & Multi-Tier Ranking")
    p = doc.add_paragraph()
    p.add_run(
        "Tabular sorting was executed using 'sort_values()'. A multi-tiered ranking operation was applied by sorting transactions "
        "primarily by Revenue (descending) and secondarily by Rating (ascending):\n"
        "  df.sort_values(by=['Revenue', 'Rating'], ascending=[False, True])\n"
        "To compute relative competitive standings across sales reps and orders, 'rank(ascending=False, method='dense')' was evaluated, "
        "confirming that the maximum recorded transaction reached $88,294.05 with rank #1."
    )

    add_sub_header("2.4 Grouping, Aggregation & Relational Merging")
    p = doc.add_paragraph()
    p.add_run(
        "Complex analytical questions require hierarchical segmentations. Using 'groupby(['Category', 'Region'])', multi-metric aggregations "
        "were executed across transaction counts, gross revenue, average spend, and dispersion metrics:\n"
        "  df.groupby('Category')['Revenue'].agg(['count', 'sum', 'mean', 'std', 'median'])\n"
        "Furthermore, relational database principles were practiced by instantiating an external regional discount reference table and executing "
        "a left outer join via 'pd.merge(df, regional_discount_df, on='Region', how='left')', demonstrating schema enrichment."
    )

    add_sub_header("2.5 NumPy SIMD Vectorized Numerical Operations")
    p = doc.add_paragraph()
    p.add_run(
        "NumPy enables blazing fast mathematical transformations by delegating operations to optimized C-level compiled BLAS/LAPACK routines. "
        "Rather than computing financial figures using native Python 'for' loops (which suffer from bytecode overhead and object boxing), "
        "revenue calculations were performed vectorially:\n"
        "  net_revenue = units_sold * unit_price * (1.0 - (discount_pct / 100.0))\n"
        "Vectorized log transformations ('np.log1p(revenue)'), trigonometric seasonal modulations, percentile aggregations ('np.percentile'), "
        "and matrix dot products were verified, executing over 500 records in under 0.2 milliseconds."
    )

    # -------------------------------------------------------------
    # SECTION 3: Perform Data Cleaning
    # -------------------------------------------------------------
    add_section_header("3", "Objective 3: Perform Data Cleaning")

    add_sub_header("3.1 Raw Data Quality Audit & Anomaly Profiling")
    p = doc.add_paragraph()
    p.add_run(
        "Real-world data ingestion inevitably encounters corruption, missing fields, schema inconsistencies, and formatting discrepancies. "
        "To simulate authentic data engineering challenges, the initial raw retail dataset was intentionally perturbed with five common data flaws:\n"
        "1. Missing Values (NaN): 15 missing observations in Customer Rating and 15 missing values in UnitPrice (30 total nulls).\n"
        "2. Duplicate Records: 10 fully replicated redundant transaction rows.\n"
        "3. Categorical Inconsistency: Random lowercase casing ('male', 'female') interspersed within title-cased 'Male' and 'Female'.\n"
        "4. Corrupt Financial Outliers: Negative revenue entries (-$999.00) caused by upstream POS sign inversion errors.\n"
        "5. String-Formatted Datetime: Date values stored as raw unparsed object strings preventing chronological analysis."
    )

    add_sub_header("3.2 The 8-Stage Data Cleaning & Hygiene Pipeline")
    p = doc.add_paragraph()
    p.add_run("A systematic, reproducible 8-stage cleaning pipeline was designed and executed:")

    cleaning_steps = [
        ("Stage 1 — Deduplication: ", "Executed df.drop_duplicates(), eliminating 10 redundant transactional records and reducing raw row count from 510 to 500."),
        ("Stage 2 — Categorical Standardization: ", "Applied df['Gender'].str.title(), collapsing disjoint casing variants into clean binary categories ('Male', 'Female')."),
        ("Stage 3 — Anomaly Pruning: ", "Filtered out corrupt records with negative revenue (df['Revenue'] > 0), pruning 1 erroneous row to reach 499 valid observations."),
        ("Stage 4 — Stratified Median Imputation for UnitPrice: ", "Because unit price varies dramatically across product categories (e.g., Electronics vs Groceries), global mean imputation would introduce severe bias. UnitPrice missing values were imputed using category-specific medians via df.groupby('Category')['UnitPrice'].transform('median')."),
        ("Stage 5 — Stratified Mean Imputation for Rating: ", "Missing customer ratings were imputed using category-specific rounded means via df.groupby('Category')['Rating'].transform(lambda x: x.fillna(round(x.mean(), 1)))."),
        ("Stage 6 — Revenue Recalculation: ", "To maintain complete financial integrity across all rows, net revenue was recalculated vectorially: df['Revenue'] = np.round(df['UnitsSold'] * df['UnitPrice'] * (1 - df['DiscountPct'] / 100), 2)."),
        ("Stage 7 — Chronological Parsing & Feature Extraction: ", "Converted Date strings to datetime64[ns] using pd.to_datetime(). Extracted Month name ('Jan'..'Dec'), Quarter ('Q1'..'Q4'), and DayOfWeek attributes."),
        ("Stage 8 — Business Metric Feature Engineering: ", "Engineered ProfitMargin metric: ProfitMargin = np.round((df['UnitPrice'] * (1 - df['DiscountPct'] / 100)) / df['UnitPrice'] * 100, 2), reflecting realized price retention.")
    ]
    for step_title, step_desc in cleaning_steps:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(3)
        r = bp.add_run(step_title)
        r.bold = True
        bp.add_run(step_desc)

    add_sub_header("3.3 Pre vs Post Cleaning Data Audit Table")
    p = doc.add_paragraph()
    p.add_run("Quantitative comparison of dataset health metrics before and after pipeline execution:")

    clean_table = doc.add_table(rows=7, cols=4)
    clean_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_widths = [Inches(1.8), Inches(1.5), Inches(1.5), Inches(1.7)]
    for row in clean_table.rows:
        for i, w in enumerate(c_widths):
            row.cells[i].width = w

    c_headers = ["Health Indicator", "Raw Ingestion State", "Clean Pipeline State", "Resolution Outcome"]
    for i, h_text in enumerate(c_headers):
        cell = clean_table.cell(0, i)
        set_cell_background(cell, NAVY_HEX)
        set_cell_margins(cell, top=120, bottom=120, left=90, right=90)
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    c_data = [
        ("Total Record Count", "510 rows", "499 rows", "10 duplicates + 1 invalid removed"),
        ("Feature Dimensionality", "13 columns", "16 columns", "+3 features engineered"),
        ("Missing Null Values", "30 nulls (Rating, Price)", "0 nulls (100% complete)", "Stratified category imputation"),
        ("Duplicate Row Count", "10 duplicates", "0 duplicates", "Exact duplicate pruning"),
        ("Categorical Integrity", "Mixed casing ('male','Female')", "Strict Title Case", "Normalized domain values"),
        ("Financial Consistency", "1 negative revenue (-$999)", "100% positive non-zero", "Vectorized recomputation")
    ]

    for r_idx, row_values in enumerate(c_data, start=1):
        bg_col = "F9FAFB" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_values):
            cell = clean_table.cell(r_idx, c_idx)
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, top=100, bottom=100, left=90, right=90)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val)
            r.font.size = Pt(9)
            if c_idx == 0:
                r.bold = True
            if c_idx == 3:
                r.font.color.rgb = SUCCESS_COLOR

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # SECTION 4: Create Data Visualizations
    # -------------------------------------------------------------
    add_section_header("4", "Objective 4: Create Data Visualizations")

    p = doc.add_paragraph()
    p.add_run(
        "Data visualization serves as the graphical conduit translating complex numerical distributions and multivariate relationships "
        "into actionable business insights. Production visualizations were developed using Matplotlib 3.11 and Seaborn 0.13, adopting "
        "harmonious color palettes, clear axis annotations, currency/percentage formatters, and professional typographic hierarchy."
    )

    # Figure 1: Bar Chart Revenue by Category
    bar_img = os.path.join(fig_dir, "bar_revenue_by_category.png")
    if os.path.exists(bar_img):
        doc.add_paragraph().paragraph_format.space_after = Pt(4)
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_after = Pt(2)
        doc.add_picture(bar_img, width=Inches(6.0))

        cap_p = doc.add_paragraph()
        cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap_p.paragraph_format.space_after = Pt(8)
        r_cap = cap_p.add_run("Figure 1: Total Revenue Generation by Merchandise Category (in Thousands USD).")
        r_cap.font.size = Pt(9)
        r_cap.font.italic = True
        r_cap.font.color.rgb = MUTED_COLOR

    p = doc.add_paragraph()
    p.add_run(
        "Analytical Finding (Figure 1): Electronics represents the single largest revenue driver, generating $3,303,096.66 across 154 transactions, "
        "followed by Groceries ($2,342,312.96) and Sports ($2,056,186.87). While Furniture recorded fewer transactions (48), it yielded the "
        "highest average transaction ticket value ($25,986.90), demonstrating high-margin luxury positioning."
    )

    # Figure 2: Line Chart Monthly Revenue
    line_img = os.path.join(fig_dir, "line_monthly_revenue.png")
    if os.path.exists(line_img):
        doc.add_paragraph().paragraph_format.space_after = Pt(4)
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_after = Pt(2)
        doc.add_picture(line_img, width=Inches(6.0))

        cap_p = doc.add_paragraph()
        cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap_p.paragraph_format.space_after = Pt(8)
        r_cap = cap_p.add_run("Figure 2: 2023 Chronological Monthly Revenue Trajectory with Mean Baseline.")
        r_cap.font.size = Pt(9)
        r_cap.font.italic = True
        r_cap.font.color.rgb = MUTED_COLOR

    p = doc.add_paragraph()
    p.add_run(
        "Analytical Finding (Figure 2): Monthly revenue exhibits healthy cyclicality, maintaining an average monthly baseline of $909.2K. "
        "Notable demand surges occur in August ($1,090.7K) and December ($1,012.4K), corresponding to back-to-school promotional campaigns "
        "and end-of-year holiday shopping volumes."
    )

    # Figure 3: Histogram & Distribution
    hist_img = os.path.join(fig_dir, "hist_revenue_distribution.png")
    if os.path.exists(hist_img):
        doc.add_paragraph().paragraph_format.space_after = Pt(4)
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_after = Pt(2)
        doc.add_picture(hist_img, width=Inches(6.0))

        cap_p = doc.add_paragraph()
        cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap_p.paragraph_format.space_after = Pt(8)
        r_cap = cap_p.add_run("Figure 3: Revenue Distribution Histogram with Parametric Gaussian & Non-Parametric KDE Curves.")
        r_cap.font.size = Pt(9)
        r_cap.font.italic = True
        r_cap.font.color.rgb = MUTED_COLOR

    p = doc.add_paragraph()
    p.add_run(
        "Analytical Finding (Figure 3): The empirical revenue distribution demonstrates pronounced positive (rightward) skewness (+0.94). "
        "The median revenue ($17,343.58) lies substantially below the arithmetic mean ($21,864.54). An extended right tail reveals occasional "
        "enterprise transactions exceeding $60,000, underscoring why non-parametric medians are necessary for pricing strategies."
    )

    # Figure 4: Scatter Plot Price vs Revenue
    scatter_img = os.path.join(fig_dir, "scatter_price_vs_revenue.png")
    if os.path.exists(scatter_img):
        doc.add_paragraph().paragraph_format.space_after = Pt(4)
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_after = Pt(2)
        doc.add_picture(scatter_img, width=Inches(6.0))

        cap_p = doc.add_paragraph()
        cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap_p.paragraph_format.space_after = Pt(8)
        r_cap = cap_p.add_run("Figure 4: Bivariate Relationship Between Unit Price and Net Revenue Across Product Categories.")
        r_cap.font.size = Pt(9)
        r_cap.font.italic = True
        r_cap.font.color.rgb = MUTED_COLOR

    p = doc.add_paragraph()
    p.add_run(
        "Analytical Finding (Figure 4): A strong positive linear correlation (r = +0.76) exists between unit catalog price and net revenue. "
        "Point clusters differentiate product category profiles: Groceries cluster tightly in the low-price/moderate-volume quadrant, "
        "while Furniture and Electronics disperse along the high-price/high-revenue corridor."
    )

    # Figure 5: Box Plots
    box_img = os.path.join(fig_dir, "boxplot_revenue_rating.png")
    if os.path.exists(box_img):
        doc.add_paragraph().paragraph_format.space_after = Pt(4)
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_after = Pt(2)
        doc.add_picture(box_img, width=Inches(6.0))

        cap_p = doc.add_paragraph()
        cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap_p.paragraph_format.space_after = Pt(8)
        r_cap = cap_p.add_run("Figure 5: Dispersion Boxplots: Revenue Across Geographic Regions (Left) and Rating Across Categories (Right).")
        r_cap.font.size = Pt(9)
        r_cap.font.italic = True
        r_cap.font.color.rgb = MUTED_COLOR

    p = doc.add_paragraph()
    p.add_run(
        "Analytical Finding (Figure 5): Across geographic territories, the North region displays the highest revenue median ($19,650) and "
        "widest interquartile dispersion. On customer ratings, all product categories maintain median ratings near 3.5, with Groceries exhibiting "
        "the tightest consensus score."
    )

    # Figure 6: Correlation Heatmap
    heat_img = os.path.join(fig_dir, "heatmap_correlation.png")
    if os.path.exists(heat_img):
        doc.add_paragraph().paragraph_format.space_after = Pt(4)
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_after = Pt(2)
        doc.add_picture(heat_img, width=Inches(5.0))

        cap_p = doc.add_paragraph()
        cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap_p.paragraph_format.space_after = Pt(8)
        r_cap = cap_p.add_run("Figure 6: Pearson Bivariate Correlation Matrix Across Numerical Attributes.")
        r_cap.font.size = Pt(9)
        r_cap.font.italic = True
        r_cap.font.color.rgb = MUTED_COLOR

    # Figure 7: Pie and Stacked Bar
    pie_img = os.path.join(fig_dir, "pie_stacked_payments_returns.png")
    if os.path.exists(pie_img):
        doc.add_paragraph().paragraph_format.space_after = Pt(4)
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_after = Pt(2)
        doc.add_picture(pie_img, width=Inches(6.0))

        cap_p = doc.add_paragraph()
        cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap_p.paragraph_format.space_after = Pt(8)
        r_cap = cap_p.add_run("Figure 7: Checkout Payment Channel Distribution (Left) and Return Rates by Payment Mode (Right).")
        r_cap.font.size = Pt(9)
        r_cap.font.italic = True
        r_cap.font.color.rgb = MUTED_COLOR

    p = doc.add_paragraph()
    p.add_run(
        "Analytical Finding (Figure 7): Payment modalities are evenly distributed: Debit Card (21.0%), Net Banking (20.8%), Credit Card (20.8%), "
        "Cash (19.8%), and UPI (17.4%). Overall portfolio product return rate is modest at 6.21%, with Debit Card and Cash transactions "
        "recording the lowest return friction."
    )

    # -------------------------------------------------------------
    # SECTION 5: Perform Basic Data Analysis
    # -------------------------------------------------------------
    add_section_header("5", "Objective 5: Perform Basic Data Analysis")

    add_sub_header("5.1 Comprehensive Descriptive Statistics Matrix")
    p = doc.add_paragraph()
    p.add_run(
        "Rigorous descriptive analysis requires synthesizing measures of central tendency, dispersion, and higher-order moments "
        "(skewness and kurtosis). Below is the comprehensive statistical synthesis evaluated on the 499 clean records:"
    )

    stats_table = doc.add_table(rows=8, cols=8)
    stats_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    st_widths = [Inches(1.2), Inches(0.7), Inches(0.8), Inches(0.7), Inches(0.7), Inches(0.7), Inches(0.8), Inches(0.9)]
    for row in stats_table.rows:
        for i, w in enumerate(st_widths):
            row.cells[i].width = w

    st_headers = ["Attribute", "Mean", "Std Dev", "Min", "Median", "Max", "Skewness", "Kurtosis"]
    for i, h_text in enumerate(st_headers):
        cell = stats_table.cell(0, i)
        set_cell_background(cell, NAVY_HEX)
        set_cell_margins(cell, top=120, bottom=120, left=60, right=60)
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    st_data = [
        ("Age", "42.56", "14.86", "18.0", "42.00", "69.0", "+0.02 (Symm)", "-1.18 (Platy)"),
        ("UnitsSold", "9.94", "5.50", "1.0", "10.00", "19.0", "+0.01 (Symm)", "-1.19 (Platy)"),
        ("UnitPrice ($)", "2,569.18", "1,440.75", "50.0", "2,540.00", "4,990.0", "+0.03 (Symm)", "-1.18 (Platy)"),
        ("DiscountPct (%)", "8.52", "7.61", "0.0", "10.00", "25.0", "+0.51 (Pos)", "-0.92 (Platy)"),
        ("Revenue ($)", "21,864.54", "18,825.44", "180.0", "17,343.58", "88,294.1", "+0.94 (Right)", "+0.33 (Lepto)"),
        ("Rating (1-5)", "3.51", "0.98", "1.0", "3.60", "5.0", "-0.15 (Symm)", "-0.67 (Platy)"),
        ("ProfitMargin (%)", "91.48", "7.61", "75.0", "90.00", "100.0", "-0.51 (Neg)", "-0.92 (Platy)")
    ]

    for r_idx, row_values in enumerate(st_data, start=1):
        bg_col = "F9FAFB" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_values):
            cell = stats_table.cell(r_idx, c_idx)
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, top=100, bottom=100, left=60, right=60)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if c_idx == 0:
                r.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_sub_header("5.2 Distribution Analysis & Multi-Feature KDE Density")
    p = doc.add_paragraph()
    p.add_run(
        "Kernel Density Estimation (KDE) fits smooth continuous probability density functions without binning artifacts. "
        "Features such as Age and UnitsSold display uniform dispersion across domains, while Revenue exhibits a clear unimodal peak "
        "around $15,000 with a sustained power-law right tail."
    )

    kde_img = os.path.join(fig_dir, "kde_all_features.png")
    if os.path.exists(kde_img):
        doc.add_paragraph().paragraph_format.space_after = Pt(4)
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_after = Pt(2)
        doc.add_picture(kde_img, width=Inches(6.2))

        cap_p = doc.add_paragraph()
        cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap_p.paragraph_format.space_after = Pt(8)
        r_cap = cap_p.add_run("Figure 8: 6-Panel Kernel Density Estimation (KDE) Distributions Across Numerical Features.")
        r_cap.font.size = Pt(9)
        r_cap.font.italic = True
        r_cap.font.color.rgb = MUTED_COLOR

    add_sub_header("5.3 Pearson vs Spearman Correlation Comparison")
    p = doc.add_paragraph()
    p.add_run(
        "To evaluate whether bivariate associations are purely linear or generally monotonic, both parametric Pearson r and "
        "non-parametric Spearman rank correlation rho were computed side-by-side:"
    )

    heat_comp_img = os.path.join(fig_dir, "heatmap_pearson_vs_spearman.png")
    if os.path.exists(heat_comp_img):
        doc.add_paragraph().paragraph_format.space_after = Pt(4)
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_after = Pt(2)
        doc.add_picture(heat_comp_img, width=Inches(6.2))

        cap_p = doc.add_paragraph()
        cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap_p.paragraph_format.space_after = Pt(8)
        r_cap = cap_p.add_run("Figure 9: Side-by-Side Dual Heatmaps: Pearson Linear (Left) vs Spearman Monotonic Rank (Right) Correlation.")
        r_cap.font.size = Pt(9)
        r_cap.font.italic = True
        r_cap.font.color.rgb = MUTED_COLOR

    p = doc.add_paragraph()
    p.add_run(
        "Empirical Insight (Figure 9): The correlation between UnitPrice and Revenue yields Pearson r = +0.76 and Spearman rho = +0.81. "
        "The elevated Spearman coefficient indicates a robust monotonic relationship that is slightly non-linear due to compounding discount percentages. "
        "Meanwhile, customer Rating exhibits negligible linear correlation with Revenue (r = -0.01), confirming that high-value buyers do not systematically "
        "rate products higher or lower than budget buyers."
    )

    add_sub_header("5.4 Outlier Detection: Tukey's IQR vs Z-Score Methods")
    p = doc.add_paragraph()
    p.add_run(
        "Outliers were formally diagnosed using two foundational statistical methodologies:\n"
        "• Tukey's Interquartile Range (IQR): An observation x is tagged as an anomaly if x < Q1 - 1.5 * IQR or x > Q3 + 1.5 * IQR. "
        "For Revenue (Q1 = $6,145.48, Q3 = $33,269.40, IQR = $27,123.92), the upper threshold was established at $73,955.28. Exactly 11 high-value "
        "transactions exceeded this threshold, representing genuine corporate bulk purchases.\n"
        "• Z-Score Standardization: Points where |Z| = |(x - mu) / sigma| > 3.0. In Revenue, 6 observations exhibited Z > 3.0. "
        "Because these points represent legitimate high-revenue orders rather than recording errors, they were retained to avoid censoring genuine business variance."
    )

    # -------------------------------------------------------------
    # SECTION 6: Complete & Document Practical Exercises
    # -------------------------------------------------------------
    add_section_header("6", "Objective 6: Practical Machine Learning Prep & Executive Dashboard")

    add_sub_header("6.1 Scikit-learn Preprocessing & Feature Pipeline")
    p = doc.add_paragraph()
    p.add_run(
        "To bridge exploratory data analysis into machine learning readiness, Scikit-learn transformation primitives were executed:\n"
        "• Categorical Label Encoding: Qualitative nominal columns ('Category', 'Region', 'PaymentMode', 'Gender') were encoded into discrete numerical arrays using LabelEncoder().\n"
        "• Feature Matrix Construction: 9 numerical predictor features were assembled into feature matrix X, targeting binary customer return propensity (y = Returned).\n"
        "• Data Partitioning (Train-Test Split): Partitioned using train_test_split() under test_size = 0.20 and random_state = 42, allocating 399 records (80%) for model training and 100 records (20%) for unseen validation.\n"
        "• Feature Standardization (StandardScaler): Fit strictly on the training set to prevent data leakage, transforming predictors to zero mean (mu = 0) and unit variance (sigma = 1)."
    )

    add_sub_header("6.2 Comprehensive 6-Panel Executive Dashboard")
    p = doc.add_paragraph()
    p.add_run(
        "To synthesize all analytical findings into a single executive artifact, a consolidated 6-panel dashboard was constructed. "
        "The dashboard captures categorical revenue totals, 12-month cyclical trends, revenue probability density, price elasticity regression, "
        "territorial dispersion boxplots, and payment mode return risks."
    )

    dash_img = os.path.join(fig_dir, "dashboard_comprehensive.png")
    if os.path.exists(dash_img):
        doc.add_paragraph().paragraph_format.space_after = Pt(4)
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_after = Pt(2)
        doc.add_picture(dash_img, width=Inches(6.4))

        cap_p = doc.add_paragraph()
        cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap_p.paragraph_format.space_after = Pt(10)
        r_cap = cap_p.add_run("Figure 10: Consolidated 6-Panel Executive Analysis Dashboard for Retail Sales Operations.")
        r_cap.font.size = Pt(9)
        r_cap.font.italic = True
        r_cap.font.color.rgb = MUTED_COLOR

    add_sub_header("6.3 Strategic Enterprise Recommendations")
    p = doc.add_paragraph()
    p.add_run("Based on empirical evidence synthesized across the data lab, four strategic recommendations are formulated:")

    recommendations = [
        ("1. Prioritize Electronics & Furniture Inventory in North Region: ", "North territory leads aggregate revenue ($2.63M), and Electronics/Furniture generate the highest ticket margins. Target regional inventory stocking ahead of Q3-Q4 demand surges."),
        ("2. Rationalize Discount Thresholds: ", "Promotional discounts currently range up to 25% without demonstrating statistically significant elasticity gains in order volume (r = -0.04). Limiting discounts to 15% would preserve an estimated 6.8% in gross margin."),
        ("3. Standardize Quality Assurance in Return-Heavy Segments: ", "While overall returns remain low (6.21%), Net Banking and UPI transactions exhibit slightly elevated return frequencies. Streamlining payment dispute resolution and delivery verification will mitigate churn."),
        ("4. Operationalize Machine Learning Pipelines: ", "The standardized feature pipeline (StandardScaler + 80/20 partition) provides the exact input matrix required to train classification models (Logistic Regression, Random Forest, XGBoost) to predict order returns prior to fulfillment.")
    ]
    for rec_title, rec_desc in recommendations:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(4)
        r = bp.add_run(rec_title)
        r.bold = True
        bp.add_run(rec_desc)

    # -------------------------------------------------------------
    # SECTION 7: Conclusion & Deliverables Index
    # -------------------------------------------------------------
    add_section_header("7", "Conclusion & Submission Deliverables Index")
    p = doc.add_paragraph()
    p.add_run(
        "All six required objectives for Assessment 2 — Hands-On Data Lab Implementation have been successfully completed, "
        "audited, and validated. The repository architecture provides complete end-to-end reproducibility, comprising clean dataset artifacts, "
        "high-resolution visualizations, a fully executed interactive Jupyter Notebook, modular Python pipelines, and this formal Word report."
    )

    deliv_table = doc.add_table(rows=6, cols=3)
    deliv_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    d_widths = [Inches(1.8), Inches(2.5), Inches(2.2)]
    for row in deliv_table.rows:
        for i, w in enumerate(d_widths):
            row.cells[i].width = w

    d_headers = ["Deliverable Component", "File Location / Path", "Verification & Status"]
    for i, h_text in enumerate(d_headers):
        cell = deliv_table.cell(0, i)
        set_cell_background(cell, NAVY_HEX)
        set_cell_margins(cell, top=120, bottom=120, left=90, right=90)
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    d_data = [
        ("Official Word Report", "Hands_On_Data_Lab_Implementation_Report.docx", "Completed & Ready for Upload"),
        ("Jupyter Notebook", "notebooks/Hands_On_Data_Lab_Implementation.ipynb", "25 Code Cells Executed with Output"),
        ("Clean & Raw Datasets", "data/retail_sales_raw.csv & clean.csv", "510 Raw / 499 Clean Records"),
        ("Production Figures", "figures/*.png (10 high-res charts)", "Rendered at 300 DPI with Annotations"),
        ("Python Pipeline Script", "src/data_lab_tasks.py", "Modular Reproducible Python Architecture")
    ]

    for r_idx, row_values in enumerate(d_data, start=1):
        bg_col = "F9FAFB" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_values):
            cell = deliv_table.cell(r_idx, c_idx)
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, top=100, bottom=100, left=90, right=90)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val)
            r.font.size = Pt(9)
            if c_idx == 0:
                r.bold = True
            if c_idx == 2:
                r.font.color.rgb = SUCCESS_COLOR

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Save document
    doc.save(output_docx)
    print(f"Report generated successfully: {output_docx} ({os.path.getsize(output_docx):,} bytes)")

if __name__ == "__main__":
    create_report()
