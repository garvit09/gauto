# config.py
import os
import sys

# Get the absolute path to the project's main directory
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# Add all subdirectories to sys.path
for root, dirs, files in os.walk(PROJECT_DIR):
    for d in dirs:
        sys.path.append(os.path.join(root, d))
