from pathlib import Path
import pandas as pd

# Load your generated dataset
FILE = Path("../data/processed/employee_synthesized.csv")
df = pd.read_csv(FILE)

print("=" * 50)
print("DATASET VALIDATION")
print("=" * 50)
print(f"Rows    : {len(df)}")
print(f"Columns : {len(df.columns)}")

# -------------------------
# SCD TYPE 2 VALIDATION
# -------------------------

print("\nSCD Distribution")
print(df.groupby("EmployeeID").size().value_counts().sort_index())

current_counts = df.groupby("EmployeeID")["IsCurrent"].sum()

invalid_current = (current_counts != 1).sum()
print(f"\nEmployees without exactly one current record: {invalid_current}")

# EndDate should be NULL only for current rows
bad_end_dates = (
    (df["IsCurrent"] == 1) & (df["EndDate"].notna())
).sum()

bad_current_rows = (
    (df["IsCurrent"] == 0) & (df["EndDate"].isna())
).sum()

print(f"Current rows with EndDate filled : {bad_end_dates}")
print(f"Historic rows with NULL EndDate  : {bad_current_rows}")

# EffectiveDate <= EndDate
date_df = df.copy()
date_df["EffectiveDate"] = pd.to_datetime(date_df["StartDate"])
date_df["EndDate"] = pd.to_datetime(date_df["EndDate"])

invalid_dates = (
    date_df["EndDate"].notna() &
    (date_df["EffectiveDate"] > date_df["EndDate"])
).sum()

print(f"Invalid date ranges              : {invalid_dates}")

# -------------------------
# DIRTY DATA VALIDATION
# -------------------------

bad_departments = [
    "R&D",
    "R&DD",
    "research & development",
    "Sales "
]

dirty_mask = (
    df["MonthlyIncome"].isna() |
    (df["MonthlyIncome"] < 0) |
    df["Email"].isna() |
    (~df["Gender"].isin(["Male", "Female"])) |
    ((df["Age"] < 18) | (df["Age"] > 65)) |
    (df["Department"].isin(bad_departments))
)

print("\nDirty Data Summary")
print(f"NULL Salary       : {df['MonthlyIncome'].isna().sum()}")
print(f"Negative Salary   : {(df['MonthlyIncome'] < 0).sum()}")
print(f"NULL Email        : {df['Email'].isna().sum()}")
print(f"Bad Department    : {df['Department'].isin(bad_departments).sum()}")
print(f"Invalid Gender    : {(~df['Gender'].isin(['Male','Female'])).sum()}")
print(f"Age Outliers      : {((df['Age'] < 18) | (df['Age'] > 65)).sum()}")

# Duplicate email across different employees
email_check = df.groupby("Email")["EmployeeID"].nunique()
duplicate_emails = (email_check > 1).sum()
print(f"Duplicate Emails  : {duplicate_emails}")

# Only one dirty issue per employee
dirty_per_employee = (
    df[dirty_mask]
    .groupby("EmployeeID")
    .size()
)

multiple_dirty = (dirty_per_employee > 1).sum()
print(f"Multiple dirty issues/employee : {multiple_dirty}")

# -------------------------
# FINAL RESULT
# -------------------------

passed = (
    invalid_current == 0 and
    bad_end_dates == 0 and
    bad_current_rows == 0 and
    invalid_dates == 0 and
    multiple_dirty == 0
)

print("\n" + "=" * 50)
print("PASS" if passed else "FAIL")
print("=" * 50)