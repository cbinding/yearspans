"""
=============================================================================
Project   : ARIADNEplus
Package   : yearspanmatcher
Module    : yearspanmatcher.py
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Summary   : 
Imports   : argparse
Example   : python3 yearspanmatcher.py -i "bronze age" -l "en" -p "p0kh9ds" 
#           output: -0699/-2599 (bronze age)
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
    def __init__(self, language: str="en", periodo_authority_id: str=None) -> None:
        self.language = language
        self._matcher = self._getMatcher(periodo_authority_id)

    # language property getter and setter
    @property
    def language(self) -> str: return self._language
    
    @language.setter
    def language(self, value: str):
        self._language = (value or "en").strip().lower()
 
    def _getMatcher(self, periodo_authority_id: str=None) -> YearSpanMatcherBase:
        match self.language:
            case "cs": return YearSpanMatcherCS(periodo_authority_id=periodo_authority_id) 
            case "cy": return YearSpanMatcherCY(periodo_authority_id=periodo_authority_id)
            case "de": return YearSpanMatcherDE(periodo_authority_id=periodo_authority_id)
            case "es": return YearSpanMatcherES(periodo_authority_id=periodo_authority_id)
            case "fr": return YearSpanMatcherFR(periodo_authority_id=periodo_authority_id)
            case "it": return YearSpanMatcherIT(periodo_authority_id=periodo_authority_id)
            case "nl": return YearSpanMatcherNL(periodo_authority_id=periodo_authority_id)
            case "no": return YearSpanMatcherNO(periodo_authority_id=periodo_authority_id)
            case "sv": return YearSpanMatcherSV(periodo_authority_id=periodo_authority_id)
            case _: return YearSpanMatcherEN(periodo_authority_id=periodo_authority_id)
    

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

    parser.add_argument("--periodo", "-p", required=False,
                        nargs='?',                       
                        help="Perio.do authority ID. If not supplied a default is used for each language (see docs)")


    # parse and return args from command line
    inputval = ""
    language = ""
    periodo_authority_id = ""

    args = parser.parse_args()
    if args.input:
        inputval = args.input.strip()
    if args.language:
        language = args.language.strip().lower()
    if args.periodo:
        periodo_authority_id = args.periodo.strip()

    # print result output
    #print(f"language='{language}', input='{input}'")
    span = YearSpanMatcher(language, periodo_authority_id).match(inputval)
    print(span or "Not matched")
