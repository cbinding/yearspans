# =============================================================================
# Project   : ARIADNEplus
# Package   : yearspans
# Module    : fix_ads_yearspans.py
# Version   : 1.0.0
# Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
# Contact   : ceri.binding@southwales.ac.uk
# Summary   :
# Custom python script specifically written for enriching XML data files from 
# Archaeology Data Service (ADS). Derives start/end years for dcterms:temporal 
# values in ADS XML aggregation files prior to data ingest. Derives new
# (minYear, maxYear) elements and adds to existing XML structure as inline siblings
# of the dcterms:temporal element, writes resultant enriched structure to new XML file
# (to ensure existing XML data is not changed).
# Imports   : argparse, shutil, xml.etree, datetime
# Example   : PYTHON3 fix_ads_yearspans.py -i "mydatafile.xml" -o "myoutput.xml"
#             if -o parameter is omitted, outputs "mydatafile.xml.temporal.xml"
# License   : http://creativecommons.org/publicdomain/zero/1.0/ [CC0]
# =============================================================================
# History
# 0.0.1 14/02/2020 CFB Initially created script
# 1.0.0 11/03/2020 CFB Revised to insert derived minYear and maxYear elements
# 1.0.1 13/10/2022 CFB Made yearspanmatcher imports more modular
# =============================================================================
import argparse                         # for argument parsing
import shutil                           # for file copying
import xml.etree.ElementTree as ET      # For XML parsing
from datetime import datetime as DT     # For process timestamps
import os, sys
from os.path import dirname, abspath, join

#from yearspanmatcher.yearspan import YearSpan
#from yearspanmatcher.yearspanmatcher_en import YearSpanMatcherEN
from yearspanmatcher import YearSpan, YearSpanMatcherEN

def main():
    
    # initiate the input arguments parser
    parser = argparse.ArgumentParser(prog=__file__, description='parse ADS yearspans into separate fields')

    # add long and short argument descriptions
    parser.add_argument("--inputfile", "-i", required=True, help="Input file name with path")
    parser.add_argument("--outputfile", "-o", nargs='?', help="Output file name with path. If not provided the output file will be inputfile.output.xml")

    # parse and return command line arguments
    args = parser.parse_args()

    # check for required named arguments
    if args.inputfile:
        inputFilePath = args.inputfile.strip()
        outputFilePath = f"{inputFilePath}.output.xml"
    if args.outputfile:
        outputFilePath = args.outputfile.strip() # overridden if supplied

    # write header information to screen
    print("\n**********************************************************")
    timestamp1 = DT.now()
    print(f"{__file__} started at {timestamp1}")

    # create a copy of the XML input file to modify the data without affecting the original
    # (actually we now overwrite the whole thing anyway so no need to copy, just new file?)
    print(f"creating a copy of {inputFilePath} as {outputFilePath}")
    shutil.copy(inputFilePath, outputFilePath)

    # read and parse the XML records
    print(f"reading from {inputFilePath}")
    try:
        # read XML file
        tree = ET.parse(inputFilePath)
        root = tree.getroot()
    except:
        print(f"Could not read from {inputFilePath}")
    else:
        counter = 0
        # declare and register required namespaces for XML data handling
        ns = {
            "ads": "https://archaeologydataservice.ac.uk/",
            "dc": "http://purl.org/dc/elements/1.1/",
            "dcterms": "http://purl.org/dc/terms/",
            "xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xsd": "http://www.w3.org/2001/XMLSchema"
        }
        for key, value in ns.items():
            ET.register_namespace(key, value)

        # process all dc:subjectPeriod elements present in the tree
        # for element in root.findall(".//record[@type='record']/dc:subjectPeriod", ns):
        for element in root.findall(".//record[@type='record']", ns):
            # should have max 1 temporal element, but loop in case more
            for temporal in element.findall("dcterms:temporal", ns):
                # derive new minYear and maxYear values
                #span = relib.en.dateSpanMatcher(temporal.text)
                matcher = YearSpanMatcherEN() 
                span = matcher.match(temporal.text)
                if span is not None:
                    # create minYear element appended as child of current dc:subjectPeriod element, sibling of dcterms:temporal
                    minYearElement = ET.SubElement(element, 'minYear')
                    minYearElement.text = YearSpan.toISO8601year(value=span.minYear, minDigits=4, zeroIsBC=True)
                    minYearElement.set('{http://www.w3.org/2001/XMLSchema-instance}type', 'http://www.w3.org/2001/XMLSchema#gYear')
                    minYearElement.tail = "\n" # included just for readability of output
                    
                    # create maxYear element appended as child of current dc:subjectPeriod element, sibling of dcterms:temporal
                    maxYearElement = ET.SubElement(element, 'maxYear')
                    maxYearElement.text = YearSpan.toISO8601year(value=span.maxYear, minDigits=4, zeroIsBC=True)
                    maxYearElement.set('{http://www.w3.org/2001/XMLSchema-instance}type', 'http://www.w3.org/2001/XMLSchema#gYear')
                    maxYearElement.tail = "\n" # included just for readability of output
                    counter += 1

        # write entire revised XML to output file
        print(f"writing to {outputFilePath}")
        tree.write(outputFilePath, xml_declaration=True, default_namespace=None, encoding='utf-8', method="xml")

    # Finished. Write footer information to screen
    timestamp2 = DT.now()
    print(f"{__file__} finished at {timestamp2}")
    duration = timestamp2 - timestamp1
    print(f"{counter} temporal records processed in {duration}")


if __name__ == "__main__":
    main()
