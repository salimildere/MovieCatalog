import json


def get_mocked_response(file_name):
    with open(file_name, 'r') as file:
        return json.loads(file.read())
