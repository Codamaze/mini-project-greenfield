import random
import pandas as pd
from pathlib import Path 

from config import (
    INPUT_FILE,
    OUTPUT_FILE,
    TARGET_ROWS,
    HISTORY_PERCENT,
    TRANSFER_PERCENT,
    DIRTY_DATA_PERCENT,
    RANDOM_SEED
)

from employee_generator import EmployeeGenerator
from scd_generator import SCDGenerator
from dirty_data import DirtyDataInjector


def generate_dataset(
    input_file,
    output_file,
    target_rows,
    history_percent,
    transfer_percent,
    dirty_percent,
    seed
):
    input_file = Path(input_file)
    output_file = Path(output_file)

    try:

        random.seed(seed)

        raw_df = pd.read_csv(input_file)

        generator = EmployeeGenerator(seed)

        scd = SCDGenerator(
            history_probability=history_percent,
            transfer_probability=transfer_percent,
            seed=seed
        )

        injector = DirtyDataInjector(
            dirty_percent=dirty_percent,
            seed=seed
        )

        departments = (
            raw_df["Department"]
            .dropna()
            .unique()
            .tolist()
        )

        records = []

        for i in range(1, target_rows + 1):

            random_index = random.randrange(len(raw_df))

            hr_row = raw_df.iloc[random_index]

            employee = generator.generate(hr_row, i)

            records.extend(
                scd.generate(
                    employee,
                    departments
                )
            )

        final_df = pd.DataFrame(records)

        final_df = injector.inject(final_df)

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        final_df.to_csv(output_file, index=False)

        return final_df

    except FileNotFoundError:
        raise FileNotFoundError(
            f"Input file not found: {input_file}"
        )

    except pd.errors.EmptyDataError:
        raise ValueError(
            "IBM HR dataset is empty."
        )

    except Exception as e:
        raise RuntimeError(
            f"Dataset generation failed: {e}"
        )


if __name__ == "__main__":

    df = generate_dataset(
        input_file=INPUT_FILE,
        output_file=OUTPUT_FILE,
        target_rows=TARGET_ROWS,
        history_percent=HISTORY_PERCENT,
        transfer_percent=TRANSFER_PERCENT,
        dirty_percent=DIRTY_DATA_PERCENT,
        seed=RANDOM_SEED
    )

    print("=" * 50)
    print("DATASET GENERATED SUCCESSFULLY")
    print("=" * 50)
    print(f"Rows    : {len(df):,}")
    print(f"Columns : {len(df.columns)}")
    print(f"Saved   : {OUTPUT_FILE}")