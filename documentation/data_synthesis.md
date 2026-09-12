# Phase 1 — Data Synthesis Module

## HR Analytics Data Warehouse Project

### Overview

This module synthesizes a realistic enterprise-scale HR operational dataset from the IBM HR Employee Attrition dataset. Since the original dataset contains only a single snapshot of employee information, the synthesis pipeline generates historical employee records (SCD Type 2), synthetic employee identities, enterprise projects, employee-project assignments, and controlled dirty data for ETL validation.

The output forms the **OLTP source system** for the Greenfield HR Analytics Data Warehouse and models a **100,000 employee organization**.

---

## Objectives

- Preserve all original IBM HR attributes.
- Generate **100,000 unique employees**.
- Create realistic employee identities.
- Engineer historical employee versions using **SCD Type 2**.
- Generate an enterprise project portfolio.
- Allocate employees across **1–3 concurrent projects**.
- Maintain realistic bench utilization (≈2–3%).
- Inject controlled dirty data for ETL testing.
- Validate employee, project, and assignment integrity before database loading.

---

## Project Structure

```text
mini-project-greenfield/
│
├── data/
│   ├── raw/
│   │   └── WA_Fn-UseC_-HR-Employee-Attrition.csv
│   │
│   └── processed/
│       ├── employee_synthesized.csv
│       ├── projects.csv
│       ├── assignments.csv
│       └── test_dataset.csv
│
└── synthesizer/
    ├── __init__.py
    ├── config.py
    ├── employee_generator.py
    ├── scd_generator.py
    ├── dirty_data.py
    ├── project_generator.py
    ├── assignment_generator.py
    ├── generate_data.py
    ├── generate_projects.py
    ├── validate_dataset.py
    └── validate_projects.py
```

---

## Pipeline Workflow

```text
IBM HR Dataset
        │
        ▼
Employee Generator
        │
        ▼
SCD Type 2 Generator
        │
        ▼
Dirty Data Injector
        │
        ├────────────► employee_synthesized.csv
        │
        ▼
Project Generator
        │
        ▼
Assignment Generator
        │
        ▼
Validation
        │
        ├────────────► projects.csv
        └────────────► assignments.csv
```

The employee dataset is generated first and becomes the workforce source for project and assignment synthesis.

---

## Module Responsibilities

### employee_generator.py

Generates synthetic employee identities while preserving every IBM HR attribute.

**Generated fields**

- EmployeeID
- FirstName
- LastName
- Email
- Phone
- HireDate

---

### scd_generator.py

Creates historical employee records using **Slowly Changing Dimension Type 2**.

Business events include:

- Promotion
- Salary revision
- Department transfer
- Job role change

Additional fields:

| Column | Description |
|---|---|
| StartDate | Version effective date |
| EndDate | Version expiry date |
| IsCurrent | Current version flag |

Each employee has **exactly one current record**.

---

### dirty_data.py

Injects approximately **5%** controlled data quality issues.

Supported dirty data includes:

- NULL Salary
- Negative Salary
- NULL Email
- Invalid Gender
- Bad Department
- Age Outlier
- Duplicate Email
- Trailing Spaces

Each employee receives **at most one** dirty data issue.

---

### project_generator.py

Generates a realistic enterprise project portfolio.

Each project contains:

| Attribute | Description |
|---|---|
| ProjectID | Unique project identifier |
| ProjectName | Synthetic project name |
| Client | Client organization |
| Priority | High / Medium / Low |
| Budget | Project budget |
| Status | Active / On Hold / Completed |
| StartDate | Project start date |
| EndDate | Planned end date |
| RequiredHeadcount | Workforce demand |

Projects are generated independently and later populated through employee assignments.

---

### assignment_generator.py

Implements an **employee-first resource allocation algorithm**.

Business rules:

- Employees work on **1–3 concurrent projects**
- Total allocation always equals **100%**
- Approximately **2–3%** employees remain on bench
- No duplicate employee-project assignments
- Active assignments have NULL EndDate
- Completed assignments retain historical EndDate

Typical allocation patterns:

| Projects | Allocation |
|---|---|
| 1 | 100 |
| 2 | 60/40, 50/50, 70/30 |
| 3 | 50/30/20, 40/30/30 |

---

### generate_data.py

Main employee synthesis orchestration.

Responsibilities:

1. Load IBM dataset
2. Generate employee identities
3. Create SCD history
4. Inject dirty data
5. Export employee dataset

---

### generate_projects.py

Main project synthesis orchestration.

Responsibilities:

1. Load current employees
2. Generate projects
3. Generate assignments
4. Export project datasets

---

### validate_dataset.py

Validates employee synthesis.

Checks:

- Row count
- Column count
- SCD distribution
- Exactly one current record
- Date integrity
- Dirty data distribution
- One dirty issue per employee

---

### validate_projects.py

Validates project and assignment datasets.

Checks:

- Referential integrity
- Duplicate assignments
- Allocation = 100%
- Bench utilization
- Project staffing balance
- Historical assignment dates
- Active assignment rules

---

## Final Dataset Statistics

### Employee Dataset

| Metric | Value |
|---|---:|
| Synthetic Employees | 100,000 |
| Total Records | **120,384** |
| Current Records | 100,000 |
| Historical Records | 20,384 |
| Total Columns | **44** |

### Project Dataset

| Metric | Value |
|---|---:|
| Total Projects | **1,000** |
| Active | 409 |
| On Hold | 141 |
| Completed | 450 |

### Assignment Dataset

| Metric | Value |
|---|---:|
| Total Assignments | **182,299** |
| Active Assignments | 136,617 |
| Historical Assignments | 45,682 |
| Bench Employees | **2,493 (2.49%)** |

### Active Workload Distribution

| Concurrent Projects | Employees |
|---|---:|
| 1 Project | 67,220 |
| 2 Projects | 21,464 |
| 3 Projects | 8,823 |

---

## Employee Validation Results

```text
==================================================
DATASET VALIDATION
==================================================

Rows    : 120384
Columns : 44

SCD Distribution
1 -> 79,616
2 -> 20,384

Employees without exactly one current record : 0
Current rows with EndDate filled            : 0
Historic rows with NULL EndDate             : 0
Invalid date ranges                        : 0

Dirty Data Summary
NULL Salary       : 619
Negative Salary   : 620
NULL Email        : 617
Bad Department    : 625
Invalid Gender    : 680
Age Outliers      : 645
Duplicate Emails  : 453
Multiple dirty issues/employee : 0

PASS
```

---

## Project & Assignment Validation Results

```text
============================================================
PROJECT DATA VALIDATION
============================================================

Projects          : 1,000
Assignments       : 182,299
Current Employees : 100,000

Integrity Checks
Invalid Employee IDs : 0
Invalid Project IDs  : 0
Allocation Errors    : 0
Bench Employees      : 2,493
Duplicate Records    : 0

Business Rule Checks
Completed Ending Future : 0
Active Already Ended    : 0
Completed Missing End   : 0
Assigned Has End Date   : 0

Projects per Employee
1 -> 67,220
2 -> 21,464
3 -> 8,823

Active Project Staffing
Understaffed : 68
Balanced     : 304
Overstaffed  : 37

PASS
```

---

## Business Rules Implemented

| Rule | Status |
|---|---|
| Exactly one current employee record | ✓ |
| SCD Type 2 maintained | ✓ |
| Employees assigned to 1–3 projects | ✓ |
| Allocation totals 100% | ✓ |
| Bench workforce maintained | ✓ |
| No duplicate employee-project records | ✓ |
| Active assignments have NULL EndDate | ✓ |
| Completed assignments retain EndDate | ✓ |
| Realistic staffing variation for analytics | ✓ |

---

## Technologies Used

- Python 3.11+
- Pandas
- Faker
- pathlib
- Object-Oriented Programming (OOP)

---

## Output

Generated datasets:

```text
data/processed/
├── employee_synthesized.csv
├── projects.csv
└── assignments.csv
```

These datasets serve as the operational source for **Phase 2: MySQL OLTP Database & ETL Pipeline**.