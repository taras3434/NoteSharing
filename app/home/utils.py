import json
import os
from flask import current_app

def load_json(file_name):
    """
    Load and parse a JSON file from the app's 'data' directory

    Args:
        file_name (str): Name of the JSON file

    Returns:
        dict or list: Parsed JSON content
    """
    # Construct the full file path relative to the Flask app root
    data_file_path = os.path.join(current_app.root_path, 'data', file_name)

    # Open the file and parse JSON content
    with open(data_file_path, 'r') as file:
        return json.load(file)