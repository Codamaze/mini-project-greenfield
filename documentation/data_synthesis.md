
# Phase 1 — Data Synthesis Module

## Enterprise HR Analytics Data Warehouse

### Overview

This module transforms the IBM HR Analytics dataset (1,470 records) into a realistic **100,000+ employee** enterprise operational dataset. It generates historical employee records using **SCD Type 2**, enterprise projects, project assignments, and annual performance reviews to serve as the **OLTP source** for the data warehouse.

---

## Objectives

- Scale IBM HR dataset to **100,000 employees**
- Generate synthetic employee identities
- Implement **SCD Type 2** employee history
- Create enterprise projects and assignments
- Generate annual performance reviews (2023–2025)
- Maintain realistic bench utilization (~2.5%)
- Validate all business rules before database loading

---

## Project Structure

```text
mini-project-greenfield/

├── data/
│   ├── raw/
│   └── processed/
│       ├── employee_synthesized.csv
│       ├── projects.csv
│       ├── assignments.csv
│       └── performance_reviews.csv
│
└── synthesizer/
    ├── employee_generator.py
    ├── scd_generator.py
    ├── dirty_data.py
    ├── project_generator.py
    ├── assignment_generator.py
    ├── review_generator.py
    ├── generate_data.py
    ├── generate_projects.py
    ├── validate_dataset.py
    ├── validate_projects.py
    └── validate_reviews.py
```

---

## Data Pipeline

```text
IBM HR Dataset
      │
      ▼
Employee Generator
      ▼
SCD Type 2 Generator
      ▼
Dirty Data Injection
      ├── employee_synthesized.csv
      ▼
Project Generator
      ▼
Assignment Generator
      ├── projects.csv
      ├── assignments.csv
      ▼
Review Generator
      └── performance_reviews.csv
      ▼
Validation
```

---

## Modules

| Module | Responsibility |
|---|---|
| `employee_generator.py` | Generate employee identity |
| `scd_generator.py` | SCD Type 2 history |
| `dirty_data.py` | Controlled dirty data |
| `project_generator.py` | Enterprise projects |
| `assignment_generator.py` | Employee allocations |
| `review_generator.py` | Annual performance reviews |
| `validate_*` | Business rule validation |

---

# Dataset Statistics

### Employees

| Metric | Value |
|---|---:|
| Employees | **100,000** |
| Total Records | **120,384** |
| Historical Records | 20,384 |
| Current Records | 100,000 |
| Columns | 44 |

### Projects

| Metric | Value |
|---|---:|
| Total Projects | **1,000** |
| Active | 409 |
| On Hold | 141 |
| Completed | 450 |

### Assignments

| Metric | Value |
|---|---:|
| Total Assignments | **182,299** |
| Active | 136,617 |
| Historical | 45,682 |
| Bench Employees | **2,493 (2.49%)** |

### Performance Reviews

| Metric | Value |
|---|---:|
| Total Reviews | **266,131** |
| Employees Reviewed | **100,000** |
| Review Years | 2023–2025 |

---

# Validation Results

### Employee & SCD Validation

```text
PASS

Rows                     : 120,384
Exactly one current row  : ✓
Invalid date ranges      : 0
Multiple dirty issues    : 0
```

### Project & Assignment Validation

```text
PASS

Invalid Employee IDs : 0
Invalid Project IDs  : 0
Allocation Errors    : 0
Duplicate Records    : 0
Bench Employees      : 2,493
```

### Performance Review Validation

```text
PASS

Duplicate Review IDs              : 0
Duplicate Annual Reviews          : 0
Invalid Employee IDs             : 0
Invalid Performance Scores        : 0
Reviews Before Hire Date          : 0
Incorrect Review Counts           : 0
Unrealistic Score Jumps           : 0
Reviews Outside Employment Period : 0

Employees Validated : 100,000
Reviews Validated   : 266,131
```

---

# Business Rules

- Exactly one **current** employee record
- SCD Type 2 history maintained
- Employees assigned to **1–3 projects**
- Allocation totals **100%**
- Bench utilization maintained (~2.5%)
- No duplicate employee–project assignments
- Active assignments have `NULL` EndDate
- One performance review per employee per year
- Reviews occur only after hire date
- Reviews fall within valid SCD employment periods

---

# Technologies

- Python 3.11
- Pandas
- Faker
- Object-Oriented Programming (OOP)

---

# Outputs

```text
data/processed/

├── employee_synthesized.csv
├── projects.csv
├── assignments.csv
└── performance_reviews.csv
```

These datasets serve as the source for **Phase 2: MySQL OLTP, ETL, and OLAP Star Schema**.