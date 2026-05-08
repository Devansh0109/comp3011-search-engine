"""Storage module for saving and loading the inverted index as JSON."""

import json
import os

DEFAULT_INDEX_PATH = "data/index.json"

def save_index(index, filepath=DEFAULT_INDEX_PATH):
    """Save the inverted index to a JSON file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(index, file, indent=2)

    print(f"Index saved to {filepath}")


def load_index(filepath=DEFAULT_INDEX_PATH):
    """Load the inverted index from a JSON file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"Index file not found at {filepath}. Please run 'build' first."
        )

    with open(filepath, "r", encoding="utf-8") as file:
        index = json.load(file)

    print(f"Index loaded from {filepath}")
    return index