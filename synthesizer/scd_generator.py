import random
from datetime import timedelta, date


class SCDGenerator:

    def __init__(
        self,
        history_probability=0.20,
        transfer_probability=0.30,
        seed=None
    ):

        self.history_probability = history_probability
        self.transfer_probability = transfer_probability

        if seed is not None:
            random.seed(seed)

    def generate(self, employee, departments):

        try:

            hire_date = employee["HireDate"]
            today = date.today()

            # 80% unchanged
            if random.random() > self.history_probability:

                current = employee.copy()

                current["StartDate"] = hire_date
                current["EndDate"] = None
                current["IsCurrent"] = 1

                return [current]

            # ---------- Choose business event ----------
            event = random.choice([
                "promotion",
                "salary_revision",
                "transfer",
                "role_change"
            ])

            total_days = (today - hire_date).days

            change_days = random.randint(
                365,
                max(total_days - 30, 366)
            )

            change_date = hire_date + timedelta(days=change_days)

            old = employee.copy()

            old["StartDate"] = hire_date
            old["EndDate"] = change_date - timedelta(days=1)
            old["IsCurrent"] = 0

            new = employee.copy()

            if event == "promotion":

                new["JobLevel"] = min(
                    int(old["JobLevel"]) + 1,
                    5
                )

                new["MonthlyIncome"] = int(
                    old["MonthlyIncome"] * random.uniform(1.20, 1.40)
                )

            elif event == "salary_revision":

                new["MonthlyIncome"] = int(
                    old["MonthlyIncome"] * random.uniform(1.08, 1.15)
                )

            elif event == "transfer":

                choices = [
                    d for d in departments
                    if d != old["Department"]
                ]

                if choices:
                    new["Department"] = random.choice(choices)

                new["MonthlyIncome"] = int(
                    old["MonthlyIncome"] * random.uniform(1.10, 1.20)
                )

            elif event == "role_change":

                new["YearsWithCurrManager"] = 0

                new["MonthlyIncome"] = int(
                    old["MonthlyIncome"] * random.uniform(1.10, 1.25)
                )

            new["StartDate"] = change_date
            new["EndDate"] = None
            new["IsCurrent"] = 1

            return [old, new]

        except Exception as e:
            raise ValueError(
                f"SCD generation failed for {employee.get('EmployeeID')}: {e}"
            )