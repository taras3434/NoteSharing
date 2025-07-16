import json
import os
from flask import current_app

def load_json(file_name):
    data_path = os.path.join(current_app.root_path, 'data', file_name)
    with open(data_path, 'r') as file:
        return json.load(file)