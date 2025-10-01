"""
Pytest configuration file to ensure proper imports.
"""
import sys
from pathlib import Path

# Add project root to Python path for all tests
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))