import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure directories exist
os.makedirs("data", exist_ok=True)
os.makedirs("figures", exist_ok=True)

# -------------------------------------------------------------
# Part 1: Python Programming Basics & Data Generation
# -------------------------------------------------------------
print("="*60)
print("1. GENERATING SYNTHETIC DATASET FOR DATA SCIENCE FUNDAMENTALS")
print("="*60)

np.random.seed(42)
n_samples = 250

customer_ids = [f"CUST_{1000 + i}" for i in range(n_samples)]
ages = np.random.randint(18, 70, size=n_samples)
incomes = np.round(np.random.normal(loc=55000, scale=15000, size=n_samples), 2)
incomes = np.clip(incomes, 20000, 120000)

satisfaction_levels = ["Low", "Medium", "High", "Very High"]
satisfaction = np.random.choice(satisfaction_levels, size=n_samples, p=[0.15, 0.35, 0.35, 0.15])

departments = ["Retail", "Corporate", "SME", "Private Banking"]
department = np.random.choice(departments, size=n_samples, p=[0.40, 0.25, 0.20, 0.15])

start_date = pd.to_datetime("2023-01-01")
end_date = pd.to_datetime("2024-01-01")
random_days = np.random.randint(0, (end_date - start_date).days, size=n_samples)
signup_dates = [start_date + pd.Timedelta(days=int(d)) for d in random_days]

feedback_snippets = [
    "Excellent customer service and transparent charges.",
    "Mobile app response is sluggish, need urgent bug fixes.",
    "Great interest rates on savings accounts and smooth onboarding.",
    "Customer support phone line was busy for over twenty minutes.",
    "Prompt transaction confirmation and easy foreign remittances.",
    "Account statements are confusing and fees were charged unexpectedly."
]
customer_feedback = np.random.choice(feedback_snippets, size=n_samples)

credit_scores = np.random.normal(loc=680, scale=60, size=n_samples).astype(int)
credit_scores = np.clip(credit_scores, 300, 850)

# Simulate churn probability influenced by income and satisfaction
churn_probs = []
for i in range(n_samples):
    score = 0.3
    if satisfaction[i] in ["Low"]:
        score += 0.35
    elif satisfaction[i] in ["Medium"]:
        score += 0.1
    if credit_scores[i] < 620:
        score += 0.2
    churn_probs.append(min(0.95, max(0.05, score)))

churned = [np.random.binomial(1, p) for p in churn_probs]

df = pd.DataFrame({
    "CustomerID": customer_ids,
    "Age": ages,
    "AnnualIncome": incomes,
    "Department": department,
    "SatisfactionLevel": satisfaction,
    "CreditScore": credit_scores,
    "SignupDate": signup_dates,
    "CustomerFeedback": customer_feedback,
    "Churned": churned
})

csv_path = "data/customer_churn_sample.csv"
df.to_csv(csv_path, index=False)
print(f"Dataset successfully created and saved to '{csv_path}' ({len(df)} rows).")

# -------------------------------------------------------------
# Part 2: Statistical Foundations Implementation
# -------------------------------------------------------------
print("\n" + "="*60)
print("2. COMPUTING STATISTICAL FOUNDATIONS")
print("="*60)

def calculate_descriptive_stats(series, name):
    mean_val = np.mean(series)
    median_val = np.median(series)
    # Mode
    values, counts = np.unique(series, return_counts=True)
    mode_val = values[np.argmax(counts)]
    
    variance_val = np.var(series, ddof=1)
    std_dev = np.std(series, ddof=1)
    p25 = np.percentile(series, 25)
    p50 = np.percentile(series, 50)
    p75 = np.percentile(series, 75)
    iqr = p75 - p25
    skewness = pd.Series(series).skew()
    
    stats_dict = {
        "Metric": name,
        "Mean": round(float(mean_val), 2),
        "Median": round(float(median_val), 2),
        "Mode": round(float(mode_val), 2),
        "Variance": round(float(variance_val), 2),
        "Std_Dev": round(float(std_dev), 2),
        "25th_Percentile": round(float(p25), 2),
        "75th_Percentile": round(float(p75), 2),
        "IQR": round(float(iqr), 2),
        "Skewness": round(float(skewness), 2)
    }
    return stats_dict

income_stats = calculate_descriptive_stats(df["AnnualIncome"], "Annual Income ($)")
credit_stats = calculate_descriptive_stats(df["CreditScore"], "Credit Score")
age_stats = calculate_descriptive_stats(df["Age"], "Age (Years)")

stats_summary = pd.DataFrame([income_stats, credit_stats, age_stats])
print(stats_summary.to_string(index=False))

# Pearson and Spearman Correlation
pearson_corr = df["AnnualIncome"].corr(df["CreditScore"], method="pearson")
spearman_corr = df["AnnualIncome"].corr(df["CreditScore"], method="spearman")
print(f"\nIncome vs Credit Score Correlation:")
print(f" - Pearson (Linear) correlation: {pearson_corr:.4f}")
print(f" - Spearman (Rank/Monotonic) correlation: {spearman_corr:.4f}")

# -------------------------------------------------------------
# Part 3: Generating Visualizations for the Assessment Report
# -------------------------------------------------------------
print("\n" + "="*60)
print("3. GENERATING HIGH-QUALITY VISUALIZATIONS")
print("="*60)

plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams.update({'font.sans-serif': 'Arial', 'font.size': 11})

# Plot 1: Income and Credit Score Distributions
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Data Science Statistical Foundations: Variable Distributions", fontsize=14, fontweight="bold")

sns.histplot(df["AnnualIncome"], kde=True, ax=axes[0], color="#2563EB", bins=20)
axes[0].set_title("Annual Income Distribution (Continuous Numerical)", fontsize=12)
axes[0].set_xlabel("Annual Income ($)")
axes[0].axvline(df["AnnualIncome"].mean(), color="#DC2626", linestyle="--", label=f'Mean: ${df["AnnualIncome"].mean():,.0f}')
axes[0].axvline(df["AnnualIncome"].median(), color="#16A34A", linestyle="-", label=f'Median: ${df["AnnualIncome"].median():,.0f}')
axes[0].legend()

sns.boxplot(x="SatisfactionLevel", y="CreditScore", data=df, order=["Low", "Medium", "High", "Very High"], ax=axes[1], palette="Blues_r")
axes[1].set_title("Credit Score by Satisfaction Tier (Ordinal Data Analysis)", fontsize=12)
axes[1].set_xlabel("Satisfaction Level")
axes[1].set_ylabel("Credit Score")

plt.tight_layout()
fig.savefig("figures/distribution_plots.png", dpi=300)
plt.close(fig)
print("Saved figures/distribution_plots.png")

# Plot 2: Correlation and Churn Analysis
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Correlation Matrix & Customer Churn Relationships", fontsize=14, fontweight="bold")

numerical_cols = ["Age", "AnnualIncome", "CreditScore", "Churned"]
corr_matrix = df[numerical_cols].corr()

sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", vmin=-1, vmax=1, fmt=".2f", ax=axes[0], linewidths=1)
axes[0].set_title("Pearson Correlation Heatmap", fontsize=12)

# Churn by Department
dept_churn = df.groupby("Department")["Churned"].mean().reset_index()
sns.barplot(x="Department", y="Churned", data=dept_churn, ax=axes[1], palette="crest")
axes[1].set_title("Churn Rate by Department (Categorical Aggregation)", fontsize=12)
axes[1].set_ylabel("Churn Proportion (0.0 to 1.0)")
for p in axes[1].patches:
    axes[1].annotate(f"{p.get_height()*100:.1f}%", (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='center', xytext=(0, 5), textcoords='offset points', fontweight='bold')

plt.tight_layout()
fig.savefig("figures/correlation_matrix.png", dpi=300)
plt.close(fig)
print("Saved figures/correlation_matrix.png")

print("\nData Science execution completed successfully.")
