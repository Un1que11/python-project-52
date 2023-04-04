import os
import json


FILES = {
        'users': 'users.json',
}


def get_fixture_path(file_name):
    workdir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(workdir, 'fixtures', file_name)


def read_json(file_name):
    json_file = get_fixture_path(file_name)
    with open(json_file, 'r') as f:
        data = json.load(f)
    return data


def get_data(category):
    look_file = FILES.get(category, None)
    if look_file:
        return read_json(look_file)
