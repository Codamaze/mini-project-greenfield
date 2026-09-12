import random
import pandas as pd


class AssignmentGenerator:

    def __init__(self, seed=None):
        if seed is not None:
            random.seed(seed)

    def _split(self, count):

        if count == 1:
            return [100]

        if count == 2:
            return random.choice([
                [60, 40],
                [50, 50],
                [70, 30]
            ])

        return random.choice([
            [50, 30, 20],
            [40, 30, 30],
            [50, 25, 25]
        ])

    def generate(self, employee_df, project_df):

        employees = (
            employee_df[
                employee_df["IsCurrent"] == 1
            ]
            .drop_duplicates("EmployeeID")
            .reset_index(drop=True)
        )

        active_projects = (
            project_df[
                project_df["Status"].isin(["Active", "On Hold"])
            ]
            .copy()
            .reset_index(drop=True)
        )

        completed_projects = (
            project_df[
                project_df["Status"] == "Completed"
            ]
        )

        # -------------------------------------------------
        # Workforce Plan (1.5% bench)
        # -------------------------------------------------

        active_staff = employees.sample(
            frac=0.985,
            random_state=random.randint(1, 999999)
        ).copy()

        employee_plan = {}

        for _, emp in active_staff.iterrows():

            project_count = random.choices(
                [1, 2, 3],
                weights=[69, 22, 9]
            )[0]

            employee_plan[emp["EmployeeID"]] = {
                "allocations": self._split(project_count),
                "projects": set()
            }

        # -------------------------------------------------
        # Project Remaining Seats
        # -------------------------------------------------

        project_state = {}

        for _, project in active_projects.iterrows():

            planned = int(project["RequiredHeadcount"])

            state = random.choices(
                ["Balanced", "Under", "Over"],
                weights=[70, 20, 10]
            )[0]

            if state == "Balanced":
                seats = round(planned * random.uniform(0.99, 1.01))

            elif state == "Under":
                seats = round(planned * random.uniform(0.90, 0.95))

            else:
                seats = round(planned * random.uniform(1.04, 1.08))

            project_state[project["ProjectID"]] = {
                "remaining": seats,
                "row": project
            }

        assignments = []
        assignment_id = 1

        # -------------------------------------------------
        # Employee First Allocation
        # -------------------------------------------------

        employee_ids = list(employee_plan.keys())
        random.shuffle(employee_ids)

        for emp in employee_ids:

            allocations = employee_plan[emp]["allocations"]

            for alloc in allocations:

                available = [
                    pid for pid, info in project_state.items()
                    if info["remaining"] > 0
                    and pid not in employee_plan[emp]["projects"]
                ]

                if not available:
                    continue

                available.sort(
                    key=lambda x: project_state[x]["remaining"],
                    reverse=True
                )

                top = available[:min(10, len(available))]
                project_id = random.choice(top)

                project_state[project_id]["remaining"] -= 1
                employee_plan[emp]["projects"].add(project_id)

                project = project_state[project_id]["row"]

                assignments.append({

                    "AssignmentID": assignment_id,
                    "EmployeeID": emp,
                    "ProjectID": project_id,
                    "AllocationPercent": alloc,
                    "AssignmentStart": project["StartDate"],
                    "AssignmentEnd": None,
                    "Status": "Assigned"

                })

                assignment_id += 1

        # -------------------------------------------------
        # Historical Completed Projects
        # -------------------------------------------------

        all_employees = employees["EmployeeID"].tolist()

        for _, project in completed_projects.iterrows():

            count = round(
                int(project["RequiredHeadcount"])
                * random.uniform(0.90, 1.05)
            )

            chosen = random.sample(
                all_employees,
                min(count, len(all_employees))
            )

            for emp in chosen:

                assignments.append({

                    "AssignmentID": assignment_id,
                    "EmployeeID": emp,
                    "ProjectID": project["ProjectID"],
                    "AllocationPercent": 0,
                    "AssignmentStart": project["StartDate"],
                    "AssignmentEnd": project["EndDate"],
                    "Status": "Completed"

                })

                assignment_id += 1

        return pd.DataFrame(assignments)