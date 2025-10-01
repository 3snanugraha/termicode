"""CLI entry point for termicode"""
import sys
import os

# Add the parent directory to Python path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

def main():
    """Main entry point for the CLI"""
    from main import main as app_main
    app_main()

if __name__ == "__main__":
    main()