"""
=============================================================================
Project   : ARIADNEplus
Package   : yearspans
Module    : match_yearspans.py
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Summary   :
Custom python script to Derive start/end years from delimited text file of
textual temporal values. Derives new (minYear, maxYear) values and adds to
existing data as additional columns (creates new file as output)
Note - looks for a column header 'value' as values to be processed
Imports   : argparse, shutil, datetime
Example   : PYTHON3 match_yearspans.py -i "mydata.txt" -o "myoutput.csv"
            if -o parameter is omitted, outputs to "mydata.txt.output.csv"
License   : https://github.com/cbinding/yearspans/blob/main/LICENSE.md
=============================================================================
History
13/10/2022 CFB Initially created script
=============================================================================
"""
import argparse                         # for argument parsing
from datetime import datetime as DT     # For process timestamps
import csv                      # for parsing/writing CSV files

import os
import sys
from os.path import dirname, abspath, join

from yearspanmatcher import *
from yearspanmatcher import YearSpanMatcher


def main() -> None:
    # initiate the input arguments parser
    parser = argparse.ArgumentParser(prog=__file__,
                                     description='derive start/end years from text file of timespan expressions')

    # add long and short argument descriptions
    parser.add_argument("--inputfile", "-i",
                        required=False,
                        help="Input file name with path")

    parser.add_argument("--outputfile", "-o",
                        nargs='?',
                        help="Output file name with path. If not provided the output file will be inputfile.output.csv")

    parser.add_argument("--language", "-l",
                        nargs='?',
                        choices=['cy', 'de', 'en', 'es',
                                 'fr', 'it', 'nl', 'no', 'sv'],
                        default='en',
                        help="Language of timespan expressions in input file")

    inputFilePath = ""
    outputFilePath = ""

    # parse and return command line arguments
    args = parser.parse_args()

    # check for required named arguments
    if args.inputfile:
        inputFilePath = args.inputfile.strip()
        outputFilePath = f"{inputFilePath}.output.csv"  # default name..
    if args.outputfile:
        outputFilePath = args.outputfile.strip()  # ..overridden if supplied
    if args.language:
        language = args.language.strip().lower()

    # write header information to screen
    print("\n**********************************************************")
    timestamp1 = DT.now()
    print(f"{__file__} started at {timestamp1}")
    print(f"input file = {inputFilePath}")
    print(f"output file = {outputFilePath}")
    print(f"language = '{language}'")

    data = []
    counter = 0
    matcher = YearSpanMatcher(language)

    # read and parse text input rows into [{"value": "x"}, {"value": "y"}, {"value": "x"}]
    print(f"Reading '{inputFilePath}'")
    data = []
    try:
        with open(inputFilePath, 'r') as f:
            contents = f.read()
            data = list(map(lambda row: {"value": row}, contents.split("\n")))
            counter = len(data)
            print(f"Read {counter} rows")
    except:
        print(f"Could not read '{inputFilePath}'")

    # process the input data to get min and max year
    print(f"processing rows")
    for item in data:
        span = matcher.match(item.get("value", ""))
        if (span is not None):
            # print(span.toISO8601())
            item["minYear"] = YearSpan.yearToISO8601(span.minYear)
            item["maxYear"] = YearSpan.yearToISO8601(span.maxYear)
            item["isoSpan"] = span.toISO8601()
            item["duration"] = span.duration()
    print(f"Processed {len(data)} rows")

    # write results to delimited output data file
    print(f"Writing to {outputFilePath}")
    with open(outputFilePath, mode='w') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(["value", "minYear", "maxYear", "isoSpan", "duration"])
        for item in data:
            writer.writerow([
                item.get("value", ""),
                item.get("minYear", ""),
                item.get("maxYear", ""),
                item.get("isoSpan", ""),
                item.get("duration", 0)
            ])
    print(f"Finished writing to {outputFilePath}")

    # Finished - write footer information to screen
    timestamp2 = DT.now()
    print(f"{__file__} finished at {timestamp2}")
    duration = timestamp2 - timestamp1
    print(f"{counter} records processed in {duration}")


if __name__ == "__main__":
    main()
