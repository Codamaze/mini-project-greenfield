import random
from datetime import date
import pandas as pd


class PerformanceReviewGenerator:

    REVIEW_YEARS = [2023, 2024, 2025]

    def __init__(self, employee_df: pd.DataFrame):
        # Only current employee records (SCD2)
        self.df = employee_df[employee_df["IsCurrent"] == 1].copy()

    @staticmethod
    def review_id(number: int) -> str:
        return f"REV{number:08d}"

    @staticmethod
    def clamp(score: float) -> float:
        return round(max(1.0, min(5.0, score)), 1)

    @staticmethod
    def score_to_rating(score: float) -> int:
        if score < 2:
            return 1
        elif score < 3:
            return 2
        elif score < 4:
            return 3
        return 4

    def generate(self) -> pd.DataFrame:

        reviews = []
        counter = 1

        for _, emp in self.df.iterrows():

            hire_date = pd.to_datetime(emp["HireDate"])
            hire_year = hire_date.year

            # IBM rating (1–4) → baseline score (2–5)
            score = float(emp["PerformanceRating"]) + 1.0

            # Slight overtime penalty
            if emp["OverTime"] == "Yes":
                score -= 0.2

            score = self.clamp(score)

            for year in self.REVIEW_YEARS:

                review_date = date(year, 12, 31)

                # Employee not yet eligible
                if hire_year > year:
                    continue

                if hire_date > pd.Timestamp(review_date):
                    continue

                # Small yearly movement (±0.5 max)
                movement = random.uniform(-0.5, 0.5)
                score = self.clamp(score + movement)

                reviews.append({
                    "ReviewID": self.review_id(counter),
                    "EmployeeID": emp["EmployeeID"],
                    "ReviewDate": review_date,
                    "PerformanceScore": score,
                    "PerformanceRating": self.score_to_rating(score)
                })

                counter += 1

        return pd.DataFrame(reviews)