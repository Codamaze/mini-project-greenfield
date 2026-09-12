from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "raw" / "WA_Fn-UseC_-HR-Employee-Attrition.csv"

OUTPUT_FILE = BASE_DIR / "data" / "processed" / "employee_synthesized.csv"

TARGET_ROWS = 100_000

HISTORY_PERCENT = 0.20

TRANSFER_PERCENT = 0.30

DIRTY_DATA_PERCENT = 0.05

RANDOM_SEED = 42

PROJECT_COUNT = 1000

MAX_PROJECTS_PER_EMPLOYEE = 4

CLIENTS = [
    "Amazon",
    "Microsoft",
    "Google",
    "Oracle",
    "HSBC",
    "Accenture",
    "Deloitte",
    "Infosys",
    "TCS",
    "IBM"
]

PROJECT_DOMAINS = [
    "AI",
    "Cloud",
    "ERP",
    "Retail",
    "Healthcare",
    "Banking",
    "Analytics"
]

PROJECT_PRIORITIES = [
    "High",
    "Medium",
    "Low"
]

OUTPUT_PROJECT_FILE = (
    BASE_DIR / "data" / "processed" / "projects.csv"
)

OUTPUT_ASSIGNMENT_FILE = (
    BASE_DIR / "data" / "processed" / "assignments.csv"
)