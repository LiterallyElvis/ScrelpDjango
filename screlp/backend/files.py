"""
files.py is a component of Screlp that handles file writing.

Specifically, it has functions to write a results file and a debug file. The
debug file is just the raw JSON output in a .txt file, and the true results
file is a CSV file.
"""

import json
import csv

METERS_PER_MILE = 1609  # number of meters in one mile.


def write_raw_result(api_result):
    """
    Writes raw JSON data to a local file, for debugging purposes.

    If for some reason the script returns an empty CSV file, or complete
    garbage, it could be useful to have this file generated. Such a file would
    reveal any Oauth errors, for example.
    """
    with open("raw_output.txt", "w") as file:
        json.dump(api_result, file, sort_keys=True, indent=4)


def write_csv_file(items):
    """
    Writes CSV file of returned data from list of Business objects.
    """
    with open("results.csv", "w") as csvout:
        output = csv.writer(csvout)
        output.writerow(["Rank", "ID", "Name", "Address", "City", "State",
                         "Zip", "Rating", "Review Count", "Category", "URL"])
        output.writerows(items)
