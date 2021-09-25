"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
import json


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = ('datetime_utc', 'distance_au', 'velocity_km_s', 'designation', 'name', 'diameter_km', 'potentially_hazardous')

    with open(filename, "x+") as f:
        header_line = ",".join(fieldnames) + ",\n"
        f.write(header_line)

        for approach in results:
            data = approach.serialize()

            result = ""
            
            result += str(data["datetime_utc"]) + ","
            result += str(data["distance_au"]) + ","
            result += str(data["velocity_km_s"]) + ","
            result += str(data["designation"]) + ","
            result += str(data["name"]) + ","
            result += str(data["diameter"]) + ","
            result += str(data["hazardous"]) + ","

            result += "\n"

            f.write(result)


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    with open(filename, "w") as f:
        #f.write("[\n")

        entries = []
        for result in results:
            approach = result.serialize()
            entry = extract_data_as_map(approach)
            entries.append(entry)
        
        f.write(json.dumps(entries, sort_keys=True, indent=2, separators=(',', ': ')))
        
        #f.write("]")


def extract_neo_data(neo):

    result = {}
    result["designation"] = neo["designation"]
    if neo["name"] != 'None':
        result["name"] = neo["name"]
    else:
        result["name"] = ""
    result["diameter_km"] = float(neo["diameter_km"])
    result["potentially_hazardous"] = bool(neo["potentially_hazardous"])

    return result


def extract_data_as_map(approach):

    entry = {}
    entry["datetime_utc"] = str(approach["datetime_utc"])
    entry["distance_au"] = float(approach["distance_au"])
    entry["velocity_km_s"] = float(approach["velocity_km_s"])

    neo = None
    try:
        neo = approach["neo"]
    except KeyError:
        neo = None

    if neo:
        neo_data =  approach["neo"].serialize()
        neo = extract_neo_data(neo_data)

    entry["neo"] = neo

    return entry