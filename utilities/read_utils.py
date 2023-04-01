"""All read, write activities on files can be done using this module"""
import json


def get_dictionary_from_json(file_path):
    return json.load(open(file_path))
