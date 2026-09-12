import random
import pandas as pd


class DirtyDataInjector:
    """
    Injects realistic dirty data into a synthesized employee dataset.
    Guarantees at least one occurrence of each error type.
    """

    def __init__(self, dirty_percent=0.05, seed=None):
        self.dirty_percent = dirty_percent

        if seed is not None:
            random.seed(seed)

        self.issue_types = [
            "null_salary",
            "negative_salary",
            "bad_department",
            "null_email",
            "bad_gender",
            "age_outlier",
            "duplicate_email",
            "trailing_space"
        ]

    def _apply_issue(self, df, idx, issue):

        if issue == "null_salary":
            df.at[idx, "MonthlyIncome"] = None

        elif issue == "negative_salary":
            df.at[idx, "MonthlyIncome"] = -5000

        elif issue == "bad_department":
            df.at[idx, "Department"] = random.choice([
                "R&D",
                "R&DD",
                "research & development",
                "Sales "
            ])

        elif issue == "null_email":
            df.at[idx, "Email"] = None

        elif issue == "bad_gender":
            df.at[idx, "Gender"] = random.choice([
                "M",
                "F",
                "Unknown"
            ])

        elif issue == "age_outlier":
            df.at[idx, "Age"] = random.choice([
                15,
                87,
                130
            ])

        elif issue == "duplicate_email":
            if idx != df.index.min():
                previous = df.index[df.index.get_loc(idx) - 1]
                df.at[idx, "Email"] = df.at[previous, "Email"]

        elif issue == "trailing_space":
            df.at[idx, "Department"] = (
                str(df.at[idx, "Department"]) + "   "
            )

    def inject(self, df: pd.DataFrame):

        try:

            dirty_df = df.copy()

            # Number of employees to corrupt (not rows)
            dirty_employees = max(
                len(self.issue_types),
                int(dirty_df["EmployeeID"].nunique() * self.dirty_percent)
            )

            # Select unique employees
            employee_ids = dirty_df["EmployeeID"].drop_duplicates().tolist()
            random.shuffle(employee_ids)

            selected_employees = employee_ids[:dirty_employees]

            # -------- Guarantee every issue once --------
            for emp_id, issue in zip(selected_employees, self.issue_types):

                idx = dirty_df[
                    (dirty_df["EmployeeID"] == emp_id) &
                    (dirty_df["IsCurrent"] == 1)
                ].index[0]

                self._apply_issue(dirty_df, idx, issue)

            # -------- Remaining employees receive one random issue --------
            remaining_employees = selected_employees[len(self.issue_types):]

            for emp_id in remaining_employees:

                idx = dirty_df[
                    (dirty_df["EmployeeID"] == emp_id) &
                    (dirty_df["IsCurrent"] == 1)
                ].index[0]

                issue = random.choice(self.issue_types)
                self._apply_issue(dirty_df, idx, issue)

            return dirty_df

        except Exception as e:
            raise RuntimeError(f"Dirty data injection failed: {e}")