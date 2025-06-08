"""
Main entry point for processing tracking numbers through the pipeline.

This script sets up the PostgreSQL database (ensuring required schemas/tables),
then processes a list of tracking numbers one by one, transforming and uploading
their data into the database.
"""

from utils.db_utils import setup_db
from constants.pipeline_contants import TRACKING_NUMBERS
from src.transformer import process_tracking_number


def main() -> None:
    """
    Initializes the database and processes all tracking numbers defined in the constants.

    Each tracking number is passed through a transformation pipeline and inserted into the database.
    Errors during processing of individual tracking numbers are caught and logged without halting the pipeline.
    """
    try:
        # Step 1: Set up database schema and tables
        setup_db()
        print("Database setup complete.\n")

        # Step 2: Process each tracking number individually
        for tracking_number in TRACKING_NUMBERS:
            try:
                print(f"Processing tracking number: {tracking_number}")
                process_tracking_number(tracking_number)
                print(f"✓ Completed: {tracking_number}\n")
            except Exception as inner_e:
                print(f"✗ Error processing {tracking_number}: {inner_e}\n")

        print("✅ All tracking numbers processed.")

    except Exception as e:
        print(f"❌ Critical error occurred during setup or batch processing: {e}")


if __name__ == "__main__":
    main()
