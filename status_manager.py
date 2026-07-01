import json
import os


STATUS_FILE = "status.json"


def load_status():

    if not os.path.exists(STATUS_FILE):
        return {}

    try:

        with open(STATUS_FILE, "r") as file:
            return json.load(file)

    except Exception:
        return {}


def save_status(status):

    with open(STATUS_FILE, "w") as file:

        json.dump(
            status,
            file,
            indent=4
        )