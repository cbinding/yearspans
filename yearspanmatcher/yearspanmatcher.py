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
if __package__ is None or __package__ == '':
    # uses current directory visibility
    from yearspanmatcher_base import YearSpanMatcherBase
    from yearspanmatcher_cs import YearSpanMatcherCS
    from yearspanmatcher_cy import YearSpanMatcherCY
    from yearspanmatcher_de import YearSpanMatcherDE
    from yearspanmatcher_en import YearSpanMatcherEN
    from yearspanmatcher_es import YearSpanMatcherES
    from yearspanmatcher_fr import YearSpanMatcherFR
    from yearspanmatcher_it import YearSpanMatcherIT
    from yearspanmatcher_nl import YearSpanMatcherNL
    from yearspanmatcher_no import YearSpanMatcherNO
    from yearspanmatcher_sv import YearSpanMatcherSV
    from yearspan import YearSpan
else:
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


class YearSpanMatcher():
    def __init__(self, language: str="en") -> None:
        self.language = language
        self._matcher = self._getMatcher()

    # language property getter and setter
    @property
    def language(self) -> str: return self._language
    
    @language.setter
    def language(self, value: str):
        self._language = (value or "en").strip().lower()
 
    def _getMatcher(self) -> YearSpanMatcherBase:
        match self.language:
            case "cs": return YearSpanMatcherCS(periodo_authority_id="p0wctqt") 
            case "cy": return YearSpanMatcherCY()
            case "de": return YearSpanMatcherDE(periodo_authority_id="p0qhb66")
            case "es": return YearSpanMatcherES(periodo_authority_id="p0qhb66")
            case "fr": return YearSpanMatcherFR(periodo_authority_id="p02chr4")
            case "it": return YearSpanMatcherIT(periodo_authority_id="p0qhb66")
            case "nl": return YearSpanMatcherNL(periodo_authority_id="p0pqptc")
            case "no": return YearSpanMatcherNO(periodo_authority_id="p04h98q")
            case "sv": return YearSpanMatcherSV(periodo_authority_id="p0qhb66")
            case _: return YearSpanMatcherEN(periodo_authority_id="p0kh9ds")
    

    def match(self, input: str="") -> YearSpan:
        span = self._matcher.match(input)
        return span


if __name__ == "__main__":
    # initiate the input arguments parser
    parser = argparse.ArgumentParser(
        prog=__file__, description='derive start/end year for temporal expression')

    # add long and short argument descriptions. TODO: add required output format?
    parser.add_argument("--language", "-l", nargs='?', default='en',
                        help="ISO language (short code). If not provided the default asssumed is 'en' (English)")
    parser.add_argument("--input", "-i", required=False,
                        default="Edwardian", help="Input temporal expression")

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
    span = YearSpanMatcher(language).match(inputval)
    print(span or "Not matched")
