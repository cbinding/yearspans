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
License   : https://github.com/cbinding/yearspans/blob/main/LICENSE.md
=============================================================================
History
14/02/2020 CFB Initially created script
=============================================================================
"""
import argparse

from .yearspanmatcher_base import YearSpanMatcherBase
from .yearspanmatcher_cs import YearSpanMatcherCS
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


def getMatcherForLanguage(language: str="en") -> YearSpanMatcherBase:
    match language.strip().lower():
        case "cs": return YearSpanMatcherCS()
        case "cy": return YearSpanMatcherCY()
        case "de": return YearSpanMatcherDE()
        case "es": return YearSpanMatcherES()
        case "fr": return YearSpanMatcherFR()
        case "it": return YearSpanMatcherIT()
        case "nl": return YearSpanMatcherNL()
        case "no": return YearSpanMatcherNO()
        case "sv": return YearSpanMatcherSV()
        case _: return YearSpanMatcherEN()
    

def get_match(input, language: str) -> YearSpan:
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
    inputval = ""
    language = ""

    args = parser.parse_args()
    if args.input:
        inputval = args.input.strip()
    if args.language:
        language = args.language.strip().lower()

    # print result output
    #print(f"language='{language}', input='{input}'")
    span = get_match(inputval, language)
    print(span or "Not matched")
