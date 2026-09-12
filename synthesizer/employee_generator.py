from datetime import date, timedelta
from faker import Faker
import random

fake = Faker("en_IN")


class EmployeeGenerator:

    def __init__(self, seed=None):

        if seed is not None:
            Faker.seed(seed)
            random.seed(seed)

    @staticmethod
    def generate_employee_id(index: int) -> str:
        return f"EMP{index:07d}"

    @staticmethod
    def derive_hire_date(years_at_company: int):
        """
        HireDate is derived from YearsAtCompany so the data
        remains internally consistent.
        """

        today = date.today()

        extra_days = random.randint(0, 364)

        return today - timedelta(
            days=(years_at_company * 365) + extra_days
        )

    def generate(self, hr_row, index: int):

        try:

            employee = hr_row.to_dict()

            first = fake.first_name()
            last = fake.last_name()

            employee["EmployeeID"] = self.generate_employee_id(index)
            employee["FirstName"] = first
            employee["LastName"] = last

            employee["Email"] = (
                f"{first.lower()}.{last.lower()}{index}@company.com"
            )

            employee["Phone"] = fake.msisdn()[:10]

            employee["HireDate"] = self.derive_hire_date(
                int(employee["YearsAtCompany"])
            )

            return employee

        except Exception as e:
            raise ValueError(
                f"Employee generation failed for row {index}: {e}"
            )