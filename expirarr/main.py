import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from maintainerr_integration import process_collections
from ahti_the_janitor import cleanup_temp_files, validate_processed_data

def main():
    print("Starting Expirarr...")
    # run cleanup tasks
    cleanup_temp_files()
    validate_processed_data()

    # process collections using Maintainerr API
    process_collections()
    print("Processing completed.")

if __name__ == "__main__":
    main()
