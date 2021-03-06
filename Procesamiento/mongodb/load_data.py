#!/usr/bin/env python
import os
from pymongo import MongoClient
import pandas as pd
import json
import progressbar

STEP = 200


def import_content(filepath):
    # cdir = os.path.dirname(__file__)
    # file_res = os.path.join(cdir, filepath)
    client = MongoClient()

    # Creates the database for the San Francisco city incidents data
    db = client['datascience']

    # Creates the collection of the documents of that will represent the incidents
    incid = db.incidents
    # We delete any content of the incidents collection, just in case it has anything
    incid.remove()

    # Reads the csv file into python's dataframe type (in my case I named it incid.csv)
    csv = pd.read_csv('Incidents.csv')

    bar = progressbar.ProgressBar()
    for start in bar(range(0, len(csv.index), STEP)):
        partial_csv = csv.ix[start:(start + STEP), :]

        # Reads the dataframe as json using orient=records,
        # form info https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_json.html
        csv_to_json = json.loads(partial_csv.to_json(orient='records'))

        # We bulk all data in
        incid.insert(csv_to_json)

        # we free some memory as csv is not needed anymore ;)
        del partial_csv
        del csv_to_json


if __name__ == "__main__":
    filepath = '~/Downloads/incid.csv'
    import_content(filepath)
