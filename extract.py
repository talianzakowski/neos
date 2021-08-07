"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def extract_headers(neo_csv_path):

    with open(neo_csv_path) as file:
        line = file.readline()
        headers = line.split(",")
        return headers

def extract_data(headers, neo_csv_file):
    """Retrieve NEO data from csv file and construct NearEarthObject istances with said data.

    :param headers: A list of strings of header names
    :param neo_csv_file: A path to a CSV file containing data about near-Earth objects. 
    """

    neos = []

    with open(neo_csv_file) as file:
        file.readline() # Discard header line

        for line in file:
            data = line.split(",")
            raw_neo_data_item  = zip(data, headers) # Data, header pairs; data first so as to retrieve all column names

            neo = NearEarthObject(raw_neo_data_item)
            neos.append(neo)
    
    return neos

def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    headers = extract_headers(neo_csv_path)
    neos = extract_data(headers, neo_csv_path)
    
    return neos


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    # TODO: Load close approach data from the given JSON file.
    return ()
