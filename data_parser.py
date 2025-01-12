# this file will parse the data into json

import csv
import os
import re

import numpy as np
import pandas

# from biothings import config
from biothings.utils.dataload import dict_convert, dict_sweep

# logging = config.logger


def str_to_list(listLikeStr: str) -> list:
    """Case str-like-list into actual list, nested list will be expand

    Args:
        listLikeStr (str): the list like str

    Return:
        the converted list

    >>> str_to_list("A")
    ['A']
    >>> str_to_list("A, B")
    ['A', 'B']
    >>> str_to_list("A B")
    ['A B']
    >>> str_to_list("A, [A, B], C")
    ['A', 'A', 'B', 'C']
    >>> str_to_list("A, B, C, D, [E, F], [G, H I]")
    ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H I']
    """
    parsed_str = re.sub(r"[\[\]]", "", listLikeStr)
    parsed_str_list = parsed_str.split(",")
    return [val.strip() for val in parsed_str_list]


def pairUp_seq_info(value_dict: dict) -> list:
    """pair up all the element in each value of the dictionary

    Args:
        value_dict (dict): values that needs to be paired up

    Return:
        a list of dictionary where the each dict is a pairings
    """
    key_list = []
    value_list = []
    temp = []
    for key, listLikeStr in value_dict.items():
        key_list.append(key)
        value_list.append(str_to_list(listLikeStr))

    for matched_values in zip(*value_list):
        temp.append({key: value for key, value, in zip(key_list, matched_values)})

    return temp


def make_uniqueMarker(cellMarkers: list) -> list:

    cellMarkers = list({tuple(sorted(marker.items())) for marker in cellMarkers})
    return [dict(marker) for marker in cellMarkers]


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

        # zip these elements together to get multiple copies
        ZIP_COLUMNS = ["cellmarker", "genesymbol", "geneid"]

        for gene_expression in pairUp_seq_info(
            {key: record[key] for key in record if key in ZIP_COLUMNS}
        ):
            _id = gene_expression["geneid"]
            if _id.casefold() == "na":
                continue
            results.setdefault(_id, []).append(
                {k: v for k, v in gene_expression.items() if k != "geneid"}
            )

    results_unqiueMarker = {
        geneid: make_uniqueMarker(markers) for geneid, markers in results.items()
    }

    for _id, docs in results_unqiueMarker.items():
        doc = {"_id": _id, "cellMarker": docs}
        yield doc


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    x = load_annotations("data")

    y = [i for i in x]
    breakpoint()
    print(y)

    # print(str_to_list("Intestinal Alkaline Phosphatase"))
