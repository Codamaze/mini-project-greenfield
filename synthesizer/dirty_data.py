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

            dirty_rows = max(
                len(self.issue_types),
                int(len(dirty_df) * self.dirty_percent)
            )

            available_rows = list(dirty_df.index)
            random.shuffle(available_rows)

            selected_rows = available_rows[:dirty_rows]

            # ---------- Guarantee every issue once ----------
            for idx, issue in zip(selected_rows, self.issue_types):
                self._apply_issue(dirty_df, idx, issue)

            # ---------- Remaining rows receive random issues ----------
            remaining = selected_rows[len(self.issue_types):]

            for idx in remaining:
                issue = random.choice(self.issue_types)
                self._apply_issue(dirty_df, idx, issue)

            return dirty_df

        except Exception as e:
            raise RuntimeError(f"Dirty data injection failed: {e}")