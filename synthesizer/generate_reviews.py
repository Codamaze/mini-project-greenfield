import pandas as pd
from performance_review_generator import PerformanceReviewGenerator

EMPLOYEE_FILE = "../data/processed/employee_synthesized.csv"
OUTPUT_FILE = "../data/processed/performance_reviews.csv"


def main():

    employees = pd.read_csv(EMPLOYEE_FILE)

    generator = PerformanceReviewGenerator(employees)

    reviews = generator.generate()

    reviews.to_csv(OUTPUT_FILE, index=False)

    print("=" * 40)
    print("PERFORMANCE REVIEWS GENERATED")
    print("=" * 40)
    print(f"Current Employees : {employees[employees['IsCurrent']==1]['EmployeeID'].nunique():,}")
    print(f"Reviews Generated : {len(reviews):,}")
    print(f"Output File       : {OUTPUT_FILE}")


if __name__ == "__main__":
    main()