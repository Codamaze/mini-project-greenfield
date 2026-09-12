import pandas as pd

# ==================================================
# LOAD DATA
# ==================================================

reviews = pd.read_csv("../data/processed/performance_reviews.csv")
employees = pd.read_csv("../data/processed/employee_synthesized.csv")

# Date conversion
reviews["ReviewDate"] = pd.to_datetime(reviews["ReviewDate"])

employees["HireDate"] = pd.to_datetime(employees["HireDate"])
employees["StartDate"] = pd.to_datetime(employees["StartDate"])
employees["EndDate"] = pd.to_datetime(
    employees["EndDate"],
    errors="coerce"
)

current = employees[employees["IsCurrent"] == 1].copy()

print("=" * 65)
print("      PERFORMANCE REVIEW BUSINESS VALIDATION")
print("=" * 65)

# ==================================================
# RULE 1 : Review IDs must be unique
# ==================================================

duplicate_review_ids = reviews["ReviewID"].duplicated().sum()

print(f"1. Duplicate Review IDs                  : {duplicate_review_ids}")

# ==================================================
# RULE 2 : One review per employee per year
# ==================================================

duplicate_cycles = reviews.duplicated(
    subset=["EmployeeID", "ReviewDate"]
).sum()

print(f"2. Duplicate Annual Reviews              : {duplicate_cycles}")

# ==================================================
# RULE 3 : Valid Employee IDs
# ==================================================

invalid_employee_ids = (
    set(reviews["EmployeeID"])
    - set(employees["EmployeeID"])
)

print(f"3. Invalid Employee IDs                 : {len(invalid_employee_ids)}")

# ==================================================
# RULE 4 : Score range (1.0–5.0)
# ==================================================

invalid_scores = reviews[
    (reviews["PerformanceScore"] < 1.0) |
    (reviews["PerformanceScore"] > 5.0)
]

print(f"4. Invalid Performance Scores            : {len(invalid_scores)}")

# ==================================================
# RULE 5 : Review cannot occur before hire
# ==================================================

hire_validation = reviews.merge(
    current[["EmployeeID", "HireDate"]],
    on="EmployeeID",
    how="left"
)

before_hire = (
    hire_validation["ReviewDate"] <
    hire_validation["HireDate"]
).sum()

print(f"5. Reviews Before Hire Date              : {before_hire}")

# ==================================================
# RULE 6 : Correct review count based on eligibility
# ==================================================

review_years = [2023, 2024, 2025]

expected = current[["EmployeeID", "HireDate"]].copy()

expected["ExpectedReviews"] = expected["HireDate"].apply(
    lambda d: sum(
        d <= pd.Timestamp(f"{yr}-12-31")
        for yr in review_years
    )
)

actual = (
    reviews.groupby("EmployeeID")
    .size()
    .rename("ActualReviews")
    .reset_index()
)

review_count = expected.merge(
    actual,
    on="EmployeeID",
    how="left"
)

review_count["ActualReviews"] = (
    review_count["ActualReviews"]
    .fillna(0)
    .astype(int)
)

incorrect_counts = (
    review_count["ExpectedReviews"] !=
    review_count["ActualReviews"]
).sum()

print(f"6. Incorrect Review Counts               : {incorrect_counts}")

# ==================================================
# RULE 7 : Maximum yearly movement = 0.5
# ==================================================

ordered = reviews.sort_values(
    ["EmployeeID", "ReviewDate"]
).copy()

ordered["PreviousScore"] = (
    ordered.groupby("EmployeeID")["PerformanceScore"]
    .shift(1)
)

movement = (
    ordered["PerformanceScore"]
    .sub(ordered["PreviousScore"])
    .abs()
    .round(1)
)

score_jumps = (movement > 0.5).sum()

print(f"7. Unrealistic Yearly Score Jumps        : {score_jumps}")

# ==================================================
# RULE 8 : Review must lie within a valid SCD2 period
# (Fully vectorized)
# ==================================================

history = employees[[
    "EmployeeID",
    "StartDate",
    "EndDate"
]]

validation = reviews.merge(
    history,
    on="EmployeeID",
    how="left"
)

valid_period = (
    (validation["ReviewDate"] >= validation["StartDate"]) &
    (
        validation["EndDate"].isna() |
        (validation["ReviewDate"] <= validation["EndDate"])
    )
)

# Each review may join to multiple history rows.
# Keep review if ANY joined row is valid.
review_validity = (
    pd.DataFrame({
        "ReviewID": validation["ReviewID"],
        "Valid": valid_period
    })
    .groupby("ReviewID")["Valid"]
    .any()
)

outside_period = (~review_validity).sum()

print(f"8. Reviews Outside Employment Period     : {outside_period}")

# ==================================================
# SUMMARY
# ==================================================

print("=" * 65)

checks = [
    duplicate_review_ids,
    duplicate_cycles,
    len(invalid_employee_ids),
    len(invalid_scores),
    before_hire,
    incorrect_counts,
    score_jumps,
    outside_period
]

if sum(checks) == 0:
    print("PASS  All business rules satisfied")
else:
    print("FAIL  Validation errors detected")

print("=" * 65)

# Optional dataset summary
print(f"Employees Validated : {current['EmployeeID'].nunique():,}")
print(f"Reviews Validated   : {len(reviews):,}")