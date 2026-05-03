import sys
import os

# Allow imports from dev/ when running pytest from anywhere
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
