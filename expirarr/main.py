import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from maintainerr_integration import process_collections

def main():
    print("Starting LastCallPosters with Maintainerr integration...")
    process_collections()
    print("Processing completed.")

if __name__ == "__main__":
    main()
