import random
from datetime import datetime, timedelta
import pandas as pd


class ProjectGenerator:

    def __init__(self, clients, domains, priorities, seed=None):

        self.clients = clients
        self.domains = domains
        self.priorities = priorities

        if seed is not None:
            random.seed(seed)

    def generate(self, project_count, employee_count):

        today = datetime.today()

        projects = []

        active_indexes = []

        # 98.5% active workforce
        active_employees = round(employee_count * 0.985)

        # Average 1.40 projects / employee
        total_required = round(active_employees * 1.40)

        for i in range(1, project_count + 1):

            status = random.choices(
                ["Completed", "Active", "On Hold"],
                weights=[44, 42, 14]
            )[0]

            if status == "Completed":

                end = today - timedelta(days=random.randint(30, 365))
                start = end - timedelta(days=random.randint(180, 720))

            else:

                start = today - timedelta(days=random.randint(30, 540))
                end = today + timedelta(days=random.randint(30, 365))

            projects.append({

                "ProjectID": f"PRJ{i:05d}",

                "ProjectName":
                    f"{random.choice(self.domains)} Transformation {i}",

                "Client":
                    random.choice(self.clients),

                "Priority":
                    random.choice(self.priorities),

                "Budget":
                    random.randint(500000, 8000000),

                "StartDate": start.date(),
                "EndDate": end.date(),
                "Status": status,

                "RequiredHeadcount": 0

            })

            if status != "Completed":
                active_indexes.append(i - 1)

        projects = pd.DataFrame(projects)

        weights = [
            random.gammavariate(2.5, 1)
            for _ in active_indexes
        ]

        total = sum(weights)

        headcounts = [
            max(20, round(total_required * w / total))
            for w in weights
        ]

        drift = total_required - sum(headcounts)

        while drift != 0:

            idx = random.randrange(len(headcounts))

            if drift > 0:
                headcounts[idx] += 1
                drift -= 1

            elif headcounts[idx] > 20:
                headcounts[idx] -= 1
                drift += 1

        for row, hc in zip(active_indexes, headcounts):
            projects.at[row, "RequiredHeadcount"] = hc

        completed = projects[
            projects["Status"] == "Completed"
        ].index

        for idx in completed:
            projects.at[idx, "RequiredHeadcount"] = random.randint(30, 180)

        return projects