from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "raw" / "WA_Fn-UseC_-HR-Employee-Attrition.csv"

OUTPUT_FILE = BASE_DIR / "data" / "processed" / "employee_synthesized.csv"

TARGET_ROWS = 100_000

HISTORY_PERCENT = 0.20

TRANSFER_PERCENT = 0.30

DIRTY_DATA_PERCENT = 0.05

RANDOM_SEED = 42