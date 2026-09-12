from pathlib import Path
import pandas as pd

from config import (
    OUTPUT_FILE,
    OUTPUT_PROJECT_FILE,
    OUTPUT_ASSIGNMENT_FILE,
    PROJECT_COUNT,
    CLIENTS,
    PROJECT_DOMAINS,
    PROJECT_PRIORITIES,
    RANDOM_SEED
)

from project_generator import ProjectGenerator
from assignment_generator import AssignmentGenerator


def generate_project_data(
    employee_file,
    project_output,
    assignment_output,
    project_count,
    clients,
    domains,
    priorities,
    seed
):

    try:

        employees = pd.read_csv(employee_file)

        project_generator = ProjectGenerator(
            clients=clients,
            domains=domains,
            priorities=priorities,
            seed=seed
        )

        current_count = (
            employees[employees["IsCurrent"] == 1]
            .EmployeeID.nunique()
        )

        projects = project_generator.generate(
            project_count=project_count,
            employee_count=current_count
        )

        assignment_generator = AssignmentGenerator(
            seed=seed
        )

        assignments = assignment_generator.generate(
            employee_df=employees,
            project_df=projects
        )

        project_output.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        projects.to_csv(
            project_output,
            index=False
        )

        assignments.to_csv(
            assignment_output,
            index=False
        )

        print("Projects generated :", len(projects))
        print("Assignments generated :", len(assignments))

        return projects, assignments

    except FileNotFoundError:
        raise FileNotFoundError(
            f"Employee dataset not found: {employee_file}"
        )

    except pd.errors.EmptyDataError:
        raise ValueError(
            "Employee dataset is empty."
        )

    except Exception as e:
        raise RuntimeError(
            f"Project data generation failed: {e}"
        )


if __name__ == "__main__":

    generate_project_data(
        employee_file=Path(OUTPUT_FILE),
        project_output=Path(OUTPUT_PROJECT_FILE),
        assignment_output=Path(OUTPUT_ASSIGNMENT_FILE),
        project_count=PROJECT_COUNT,
        clients=CLIENTS,
        domains=PROJECT_DOMAINS,
        priorities=PROJECT_PRIORITIES,
        seed=RANDOM_SEED
    )