# mini-project-greenfield (Team 6)
# HR Analytics Data Warehouse

A complete end-to-end **HR Analytics Data Engineering** project that transforms the IBM HR Employee Attrition dataset into a scalable **OLTP + OLAP** data warehouse using ETL pipelines, SCD Type 2 implementation, and an interactive Streamlit dashboard.

---

## Project Overview

This project demonstrates the complete data engineering lifecycle:

- Synthetic HR data generation (100,000+ employees)
- Historical employee records using **Slowly Changing Dimension (SCD Type 2)**
- ETL pipeline with data cleaning and validation
- Normalized **OLTP** database in MySQL
- **Star Schema OLAP** data warehouse
- Interactive analytics dashboard using Streamlit

---

## Tech Stack

| Layer | Technology |
|--------|------------|
| Data Generation | Python, Pandas, Faker |
| Database | MySQL Workbench |
| ETL | SQL, Python |
| Data Warehouse | Star Schema, SCD Type 2 |
| Dashboard | Streamlit |

---

## Architecture

```text
IBM HR Employee Attrition Dataset
                │
                ▼
     Synthetic Data Generation
        (100,000+ Employees)
                │
                ▼
        Staging Database
                │
                ▼
   ETL Cleaning & Validation
                │
                ▼
     OLTP Database (3NF)
                │
                ▼
  OLAP Data Warehouse (Star Schema)
                │
                ▼
   Streamlit Analytics Dashboard
```

---

## Repository Structure

```text
mini-project-greenfield/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── synthesizer/
│
├── database/
│
├── streamlit_app/
│
├── docs/
│
└── README.md
```

---

## Key Features

- Generates **120,000+** realistic HR employee records
- Preserves all original IBM HR dataset attributes
- Implements **SCD Type 2** for historical employee tracking
- Injects controlled dirty data for ETL testing
- Builds a normalized **OLTP** schema
- Designs an **OLAP Star Schema** with surrogate keys
- Supports advanced SQL analytics using procedures and window functions

---

## Dataset Summary

| Metric | Value |
|--------|------:|
| Synthetic Employees | 100,000 |
| Total Records | 120,384 |
| Total Columns | 44 |
| Historical Records | 20,384 |

---

## Documentation

Detailed implementation is available in the `docs/` directory:

- `documentation/data_synthesis.md`
- `documentation/etl.md`
- `documentation/oltp.md`
- `documentation/olap.md`

---

## Team

**Mini Project** — HR Analytics Data Warehouse
**Team** - Nagasupriya Bandlamudi, Ishvi Jain, Jatin
