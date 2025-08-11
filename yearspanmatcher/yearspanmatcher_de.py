"""
=============================================================================
Project   : ARIADNEplus
Package   : yearspanmatcher
Module    : yearspanmatcher_de.py
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Summary   : YearSpan matcher (German)
Imports   : regex, enums, relib, yearspan
Example   :
License   : https://github.com/cbinding/yearspans/blob/main/LICENSE.md
=============================================================================
History
14/02/2020 CFB Initially created script
=============================================================================
"""
import regex

from . import enums
from .yearspan import YearSpan    
from .relib import maybe, oneof, group, zeroormore, oneormore, SPACEORDASH, NUMERICYEAR
from .yearspanmatcher_en import YearSpanMatcherEN


class YearSpanMatcherDE(YearSpanMatcherEN):

    def __init__(self, present: int=2000, periodo_authority_id="p0qhb66") -> None:
        super(YearSpanMatcherEN, self).__init__(
            language="de", 
            periodo_authority_id=periodo_authority_id
        )
        self.MILLENNIUM = r"Jahrtausends?"
        self.CENTURY = r"(?:Jahrhundert|Jh)"


    def matchLoneDecade(self, value: str) -> YearSpan | None:
        # e.g. "1950er"
        decade = 0

        pattern = r"\s*".join([
            maybe(oneof(self.DATEPREFIXES, "datePrefix")),
            group(r"\b[1-9]\d{1,2}0", "decade") + "er",
            maybe(oneof(self.DATESUFFIXES, "dateSuffix")),
            maybe("Jahre")
        ])
        match = regex.fullmatch(pattern, value, regex.IGNORECASE)
        if not match:
            return None
        if 'decade' in match.groupdict():
            decade = int(match.group('decade'))
        span = YearSpan(decade, decade + 9, value)
        return span


    def matchDecadeToDecade(self, value: str) -> YearSpan | None:
        decade1: int = 0
        decade2: int = 0

        # e.g. "1950er bis 1960er"
        pattern = r"\s*".join([
            maybe(oneof(self.DATEPREFIXES, "datePrefix")),
            group(r"\b[1-9]\d{1,2}0", "decade1") + "er",
            oneof(self.DATESEPARATORS),
            group(r"\b[1-9]\d{1,2}0", "decade2") + "er",
            maybe(oneof(self.DATESUFFIXES, "dateSuffix")),
            maybe("Jahre")
        ])
        match = regex.fullmatch(pattern, value, regex.IGNORECASE)
        if not match:
            return None
        if 'decade1' in match.groupdict():
            decade1 = int(match.group('decade1'))
        if 'decade2' in match.groupdict():
            decade2 = int(match.group('decade2'))
        span = YearSpan(decade1, decade2 + 9, value)
        return span

if __name__ == "__main__":
    span = YearSpanMatcherDE().match("Frühes elfte Jahrhundert n. Chr")
    print(span)
