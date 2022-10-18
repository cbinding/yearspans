This folder contains results of some 'real world' testing of the year span matching functionality.

test-data-ads.xml is a short extract of a larger XML file containing archaeological collections medatata supplied by Archaeology Data Service (ADS) for ingest to ARIADNEplus agggregation platform. fix_ads_yearspans.py is a bespoke bulk processing script run against selected ADS collection files in this XML format; it locates values in the dcterms:temporal field and supplements them with sibling _minYear_ and _maxYear_ properties. The example output is contained in file test-data-ads.xml.output.xml

Other files in this directory are the input (TXT) and output (CSV) results of running script match_yearspans.py. The input files contain values originating from specific dataset fields in a range of datasets obtained from ADS.
