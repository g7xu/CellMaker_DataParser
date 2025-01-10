# this file will parse the data into json

import csv
import math
import os
import re

import pandas as pd

# from biothings import config
from biothings.utils.dataload import dict_convert, dict_sweep

# logging = config.loggers


def pairUp_seq_info(value_dict: dict) -> list:
    """pair up all the element in each value of the dictionary

    Args:
        value_dict (dict): values that needs to be paired up

    Return:
        a list of dictionary where the each dict is a pairings
    """
    print(value_dict)


def load_annotations(data_folder):
    """Converting data into expected JSON format

    Args:
        data_folder (str): the relative data path to the data source

    Return:
        the yield JSON data
    """

    # convert and check if the data file exist
    infile_all_cell = os.path.join(data_folder, "all_cell_markers.txt")
    infile_single_cell = os.path.join(data_folder, "Single_cell_markers.txt")

    assert os.path.exists(infile_all_cell)
    assert os.path.exists(infile_single_cell)

    # import data and store them in a list
    data = []
    with open(infile_all_cell, mode="r") as file:
        reader = csv.DictReader(file, delimiter="\t", quoting=csv.QUOTE_NONE)
        data += [row for row in reader]
    with open(infile_single_cell, mode="r") as file:
        reader = csv.DictReader(file, delimiter="\t", quoting=csv.QUOTE_NONE)
        data += [row for row in reader]

    results = dict()

    for record in data:
        # converting all the key to standard format
        process_key = lambda k: k.replace(" ", "_").lower()
        record = dict_convert(record, keyfn=process_key)

        if record["geneid"] == "NA":
            continue

        _id = record["geneid"]
        # cell_marker = record["cellMarker"]
        results.setdefault(_id, []).append(record)

        # zip these elements together to get multiple copies
        ZIP_COLUMNS = ["cellmarker", "genesymbol", "geneid"]

        for gene_expression in pairUp_seq_info(
            {key: record[key] for key in record if key in ZIP_COLUMNS}
        ):
            print(gene_expression)
            return

    for _id, docs in results.items():
        doc = {"_id": _id, "cellMarker": docs}
        yield doc

    # return results


if __name__ == "__main__":
    load_annotations("data")
