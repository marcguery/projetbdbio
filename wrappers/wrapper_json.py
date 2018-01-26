#!/usr/bin/env python
# -*- coding: utf-8 -*-
# version 2018-01-12
# run : python json_wrapper.py
# =============================================================================
#	Class for interacting with JSON files
# =============================================================================

import json # https://docs.python.org/3.6/library/json.html?highlight=json

'''
WrapperJSON class for parsing json file
'''

class WrapperJSON:

    def __init__(self, json_file):
        self.json_file = json_file # path of the json file

    def parse(self):
        with open(self.json_file, encoding='utf-8') as data_file:
            data = json.loads(data_file.read())
            return data

# a simple example
if (__name__ == "__main__"):
    file_json_interactions = 'sources/interactions-PMID-17446270.json'  # path to JSON file
    conn_json = WrapperJSON(file_json_interactions)
    dict_json = conn_json.parse()
    print(dict_json)