"""
=============================================================================
Project   : ARIADNEplus
Package   : yearspanmatcher
Module    : yearspanmatcher.py
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Summary   : 
Imports   : argparse
Example   : python3 yearspanmatcher.py -i "bronze age" -l "en" # output: -0699/2600 (bronze age)
License   : https://creativecommons.org/licenses/by/4.0/ [CC BY 4.0]
=============================================================================
History
14/02/2020 CFB Initially created script
=============================================================================
"""
import argparse

from .yearspanmatcher_base import YearSpanMatcherBase
from .yearspanmatcher_cy import YearSpanMatcherCY
from .yearspanmatcher_de import YearSpanMatcherDE
from .yearspanmatcher_en import YearSpanMatcherEN
from .yearspanmatcher_es import YearSpanMatcherES
from .yearspanmatcher_fr import YearSpanMatcherFR
from .yearspanmatcher_it import YearSpanMatcherIT
from .yearspanmatcher_nl import YearSpanMatcherNL
from .yearspanmatcher_no import YearSpanMatcherNO
from .yearspanmatcher_sv import YearSpanMatcherSV
from .yearspan import YearSpan


def getMatcherForLanguage(language="en") -> YearSpanMatcherBase:
    lang = language.strip().lower()
    matcher = None

    if lang == "cy":
        matcher = YearSpanMatcherCY()
    elif lang == "de":
        matcher = YearSpanMatcherDE()
    elif lang == "es":
        matcher = YearSpanMatcherES()
    elif lang == "fr":
        matcher = YearSpanMatcherFR()
    elif lang == "it":
        matcher = YearSpanMatcherIT()
    elif lang == "nl":
        matcher = YearSpanMatcherNL()
    elif lang == "no":
        matcher = YearSpanMatcherNO()
    elif lang == "sv":
        matcher = YearSpanMatcherSV()
    else:
        matcher = YearSpanMatcherEN()
    return matcher


def get_match(input, language) -> YearSpan:
    matcher = getMatcherForLanguage(language)
    span = matcher.match(input)
    return span


if __name__ == "__main__":
    # initiate the input arguments parser
    parser = argparse.ArgumentParser(
        prog=__file__, description='derive start/end year for temporal expression')

    # add long and short argument descriptions
    parser.add_argument("--language", "-l", nargs='?', default='en',
                        help="ISO language (short code). If not provided the default asssumed is 'en' (English)")
    parser.add_argument("--input", "-i", required=False,
                        default="", help="Input temporal expression")

    # parse and return args from command line
    input = ""
    language = ""

    args = parser.parse_args()
    if args.input:
        input = args.input.strip()
    if args.language:
        language = args.language.strip().lower()

    # print result output
    #print(f"language='{language}', input='{input}'")
    span = get_match(input, language)
    print(span or "Not matched")
