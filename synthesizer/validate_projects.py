import pandas as pd
from pathlib import Path

from config import (
    OUTPUT_FILE,
    OUTPUT_PROJECT_FILE,
    OUTPUT_ASSIGNMENT_FILE
)


def validate():

    employees = pd.read_csv(Path(OUTPUT_FILE))
    projects = pd.read_csv(Path(OUTPUT_PROJECT_FILE))
    assignments = pd.read_csv(Path(OUTPUT_ASSIGNMENT_FILE))

    current = (
        employees[
            employees["IsCurrent"] == 1
        ]
        .drop_duplicates("EmployeeID")
    )

    today = pd.Timestamp.today().normalize()

    print("=" * 60)
    print("PROJECT DATA VALIDATION")
    print("=" * 60)

    print(f"Projects          : {len(projects):,}")
    print(f"Assignments       : {len(assignments):,}")
    print(f"Current Employees : {len(current):,}")

    # --------------------------------------------------
    # Integrity Checks
    # --------------------------------------------------

    invalid_employee = (
        ~assignments["EmployeeID"]
        .isin(current["EmployeeID"])
    ).sum()

    invalid_project = (
        ~assignments["ProjectID"]
        .isin(projects["ProjectID"])
    ).sum()

    current_assignments = assignments[
        assignments["Status"] == "Assigned"
    ]

    # ---------- Allocation Validation ----------

    allocation = (
        current_assignments
        .groupby("EmployeeID")["AllocationPercent"]
        .sum()
        .reset_index(name="TotalAllocation")
    )

    allocation_errors = allocation[
        allocation["TotalAllocation"] != 100
    ]

    assigned_ids = set(current_assignments["EmployeeID"])

    bench = (
        ~current["EmployeeID"].isin(assigned_ids)
    ).sum()

    duplicate_assignments = (
        assignments
        .duplicated(["EmployeeID", "ProjectID"])
        .sum()
    )

    print("\nIntegrity Checks")
    print(f"Invalid Employee IDs : {invalid_employee}")
    print(f"Invalid Project IDs  : {invalid_project}")
    print(f"Allocation Errors    : {len(allocation_errors)}")
    print(f"Bench Employees      : {bench:,}")
    print(f"Duplicate Records    : {duplicate_assignments}")

    if not allocation_errors.empty:

        print("\nEmployees with Invalid Allocation")
        print(
            allocation_errors
            .head(10)
            .to_string(index=False)
        )

    # --------------------------------------------------
    # Business Rule Checks
    # --------------------------------------------------

    completed_future = (
        (projects["Status"] == "Completed") &
        (pd.to_datetime(projects["EndDate"]) > today)
    ).sum()

    active_past = (
        (projects["Status"] == "Active") &
        (pd.to_datetime(projects["EndDate"]) < today)
    ).sum()

    completed_missing_end = (
        (assignments["Status"] == "Completed") &
        (assignments["AssignmentEnd"].isna())
    ).sum()

    assigned_has_end = (
        (assignments["Status"] == "Assigned") &
        (assignments["AssignmentEnd"].notna())
    ).sum()

    print("\nBusiness Rule Checks")
    print(f"Completed Ending Future : {completed_future}")
    print(f"Active Already Ended    : {active_past}")
    print(f"Completed Missing End   : {completed_missing_end}")
    print(f"Assigned Has End Date   : {assigned_has_end}")

    # --------------------------------------------------
    # Employee Workload
    # --------------------------------------------------

    workload = (
        current_assignments
        .groupby("EmployeeID")
        .size()
        .value_counts()
        .sort_index()
    )

    print("\nProjects per Employee")
    print(workload)

    # --------------------------------------------------
    # Project Staffing
    # --------------------------------------------------

    staffing = (
        current_assignments
        .groupby("ProjectID")
        .size()
        .rename("Assigned")
        .reset_index()
    )

    summary = projects.merge(
        staffing,
        on="ProjectID",
        how="left"
    )

    summary["Assigned"] = (
        summary["Assigned"]
        .fillna(0)
        .astype(int)
    )

    summary["Gap"] = (
        summary["RequiredHeadcount"] -
        summary["Assigned"]
    )

    active = summary[
        summary["Status"] == "Active"
    ]

    under = (active["Gap"] > 5).sum()

    balanced = (
        (active["Gap"] >= -5) &
        (active["Gap"] <= 5)
    ).sum()

    over = (active["Gap"] < -5).sum()

    print("\nActive Project Staffing Summary")
    print(f"Understaffed : {under}")
    print(f"Balanced     : {balanced}")
    print(f"Overstaffed  : {over}")

    print("\nProject Status Distribution")
    print(projects["Status"].value_counts())

    print("\nAssignment Status Distribution")
    print(assignments["Status"].value_counts())

    # --------------------------------------------------
    # Analytics Samples
    # --------------------------------------------------

    print("\nTop 10 Understaffed Projects")
    print(
        active[active["Gap"] > 0]
        .sort_values("Gap", ascending=False)[
            [
                "ProjectID",
                "RequiredHeadcount",
                "Assigned",
                "Gap"
            ]
        ].head(10)
    )

    print("\nTop 10 Overstaffed Projects")
    print(
        active[active["Gap"] < 0]
        .sort_values("Gap")[
            [
                "ProjectID",
                "RequiredHeadcount",
                "Assigned",
                "Gap"
            ]
        ].head(10)
    )

    # --------------------------------------------------
    # Final Result
    # --------------------------------------------------

    if (
        invalid_employee == 0 and
        invalid_project == 0 and
        len(allocation_errors) == 0 and
        duplicate_assignments == 0 and
        completed_future == 0 and
        active_past == 0 and
        completed_missing_end == 0 and
        assigned_has_end == 0
    ):

        print("\n" + "=" * 60)
        print("PASS")
        print("=" * 60)

    else:

        print("\n" + "=" * 60)
        print("FAILED")
        print("=" * 60)


if __name__ == "__main__":
    validate()