from pathlib import Path
import pandas as pd

from generate_data import generate_dataset
from config import INPUT_FILE


# --------------------------------------------------
# Generate Test Dataset
# --------------------------------------------------

df = generate_dataset(
    input_file=INPUT_FILE,
    output_file=Path("../data/processed/test_dataset.csv"),
    target_rows=100,
    history_percent=0.20,
    transfer_percent=0.30,
    dirty_percent=0.05,
    seed=42
)

print("=" * 50)
print("TEST RESULTS")
print("=" * 50)

print(f"Rows    : {len(df)}")
print(f"Columns : {len(df.columns)}")


# --------------------------------------------------
# SCD TYPE 2 VALIDATION
# --------------------------------------------------

print("\nSCD Distribution")
print(df.groupby("EmployeeID").size().value_counts())

current_counts = df.groupby("EmployeeID")["IsCurrent"].sum()

print(
    "\nEmployees without exactly one current:",
    (current_counts != 1).sum()
)


# --------------------------------------------------
# DIRTY DATA VALIDATION
# --------------------------------------------------

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

# Count dirty records
print("\nDirty Data Summary")
print(f"NULL Salary       : {df['MonthlyIncome'].isna().sum()}")
print(f"Negative Salary   : {(df['MonthlyIncome'] < 0).sum()}")
print(f"NULL Email        : {df['Email'].isna().sum()}")
print(f"Bad Department    : {df['Department'].isin(bad_departments).sum()}")
print(f"Invalid Gender    : {(~df['Gender'].isin(['Male','Female'])).sum()}")
print(f"Age Outliers      : {((df['Age'] < 18) | (df['Age'] > 65)).sum()}")

# True duplicate emails (ignore SCD history)
email_check = df.groupby("Email")["EmployeeID"].nunique()
print(f"Duplicate Emails  : {(email_check > 1).sum()}")

# Ensure one dirty issue per employee
dirty_per_employee = (
    df[dirty_mask]
    .groupby("EmployeeID")
    .size()
)

print(
    "Employees with multiple dirty issues:",
    (dirty_per_employee > 1).sum()
)


# --------------------------------------------------
# SAMPLE OUTPUT
# --------------------------------------------------

print("\nFirst Five Records")
print(df.head())