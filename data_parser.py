# this file will parse the data into json

import csv
import math
import os
import re

import pandas as pd

# from biothings import config
from biothings.utils.dataload import dict_convert

# logging = config.logger


def load_annotations(data_folder):
    # convert and check if the data file exist
    infile = os.path.join(data_folder, "all_cell_markers.tsv")
    assert os.path.exists(infile)

    # #
    # dat = (
    #     pd.read_csv(infile, sep="\t", quoting=csv.QUOTE_NONE)
    #     .squeeze("columns")
    #     .to_dict(orient="records")
    # )
    # results = {}
    # for rec in dat:
    #     if not rec["Gene"] or pd.isna(rec["Gene"]):
    #         logging.warning(
    #             "No gene information for annotation ID '%s'", rec["Annotation ID"]
    #         )
    #         continue
    #     _id = re.match(".* \((.*?)\)", rec["Gene"]).groups()[0]
    #     # we'll remove space in keys to make queries easier. Also, lowercase is preferred
    #     # for a BioThings API. We'll an helper function from BioThings SDK
    #     process_key = lambda k: k.replace(" ", "_").lower()
    #     rec = dict_convert(rec, keyfn=process_key)
    #     results.setdefault(_id, []).append(rec)

    # for _id, docs in results.items():
    #     doc = {"_id": _id, "annotations": docs}
    #     yield doc


load_annotations("data")
