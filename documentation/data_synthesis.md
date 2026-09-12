# Phase 1 — Data Synthesis Module

## HR Analytics Data Warehouse Project

### Overview

This module synthesizes a realistic HR employee dataset from the IBM HR Employee Attrition dataset. The original dataset contains only a single snapshot of employee information, so this pipeline engineers historical employee versions (SCD Type 2), generates synthetic employee identities, and injects controlled dirty data for ETL testing.

The output is a production-scale dataset containing **120,384 records** and **44 columns**, ready for loading into the MySQL staging schema.

---

## Objectives

* Preserve all original IBM HR attributes.
* Generate **100,000 unique employees**.
* Create realistic employee identities (ID, name, email, phone).
* Engineer historical employee versions using **Slowly Changing Dimension Type 2 (SCD2)**.
* Inject realistic dirty data for ETL validation.
* Validate data integrity before database loading.

---

## Project Structure

```text
mini-project-greenfield/
│
├── data/
│   ├── raw/
│   │   └── WA_Fn-UseC_-HR-Employee-Attrition.csv
│   └── processed/
│       ├── employee_synthesized.csv
│       └── test_dataset.csv
│
└── synthesizer/
    ├── __init__.py
    ├── config.py
    ├── employee_generator.py
    ├── scd_generator.py
    ├── dirty_data.py
    ├── generate_data.py
    └── test_generator.py
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
        ▼
Validation Script
        │
        ▼
employee_synthesized.csv
```

---

## Modules

### 1. employee_generator.py

**Responsibility:** Generate one synthetic employee while preserving every IBM HR attribute.

**Adds**

* EmployeeID
* FirstName
* LastName
* Email
* Phone
* HireDate (derived from YearsAtCompany)

All original IBM columns remain unchanged.

### 2. scd_generator.py

Engineers historical employee versions.

Possible business events include:

* Promotion
* Salary Revision
* Department Transfer
* Role Change

Additional SCD fields:

| Column    | Description         |
| --------- | ------------------- |
| StartDate | Version start date  |
| EndDate   | Version end date    |
| IsCurrent | Current record flag |

Each employee always has **exactly one current record**.

### 3. dirty_data.py

Injects approximately **5%** controlled data quality issues.

Dirty data types:

* NULL Salary
* Negative Salary
* NULL Email
* Invalid Gender
* Bad Department Names
* Age Outliers
* Duplicate Emails
* Trailing Spaces

Each employee receives **at most one** dirty data issue.

### 4. generate_data.py

Main orchestration script.

Responsibilities:

1. Read raw dataset
2. Generate synthetic employees
3. Create SCD history
4. Inject dirty data
5. Export CSV

### 5. test_generator.py

Validates the generated dataset before database loading.

Checks include:

* Row count
* Column count
* SCD distribution
* Exactly one current record
* Date integrity
* Dirty data counts
* One dirty issue per employee

---

## Final Dataset Statistics

| Metric              |       Value |
| ------------------- | ----------: |
| Synthetic Employees |     100,000 |
| Total Records       | **120,384** |
| Total Columns       |      **44** |
| Historical Versions |      20,384 |
| Current Versions    |     100,000 |

### SCD Distribution

| Employee Versions |  Count |
| ----------------- | -----: |
| One Version       | 79,616 |
| Two Versions      | 20,384 |

---

## Validation Results

```text
Rows: 120384
Columns: 44

SCD Distribution
1 -> 79,616
2 -> 20,384

Employees without exactly one current record: 0

Current rows with EndDate filled : 0
Historic rows with NULL EndDate  : 0
Invalid date ranges              : 0

Multiple dirty issues per employee: 0
```

All validation tests passed successfully.

---

## Technologies Used

* Python 3.11+
* Pandas
* Faker
* pathlib
* Object-Oriented Programming (OOP)

---

## Output

Generated dataset:

```text
data/processed/employee_synthesized.csv
```

This dataset serves as the input for **Phase 2: MySQL Staging & ETL Pipeline**.
