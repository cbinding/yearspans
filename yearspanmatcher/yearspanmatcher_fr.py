# =============================================================================
# Package   : yearspans
# Module    : yearspanmatcher_fr.py
# Version   : Draft 0.1
# Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
# Contact   : ceri.binding@southwales.ac.uk
# Project   : ReMatch
# Summary   : YearSpan matcher (French)
# Require   : 
# Imports   : regex, enums, relib, yearspan
# Example   : 
# License   : http://creativecommons.org/publicdomain/zero/1.0/ [CC0]
# =============================================================================
# History
# 14/02/2020 CFB Initially created script
# =============================================================================
# from enums import Day, Month, Season, DatePrefix, DateSuffix
import regex
from . import enums
from .relib import maybe, oneof, group, zeroormore, oneormore, SPACE, SPACEORDASH, NUMERICYEAR, patterns
from .yearspan import YearSpan
from .yearspanmatcher_en import YearSpanMatcherEN


class YearSpanMatcherFR(YearSpanMatcherEN):

    def __init__(self):
        super(YearSpanMatcherEN, self).__init__("fr")  
        self.MILLENNIUM = r"mill[ée]naire"
        self.CENTURY = r"si[èe]cle"  

        
    def matchLoneDecade(self, value: str) -> YearSpan:
        # e.g. "les années 1950"
        decade = 0
        
        pattern = "".join([
            maybe(oneof(self.DATEPREFIXES, "datePrefix") + SPACE),
            r"(?:les\s)?années\s",
            group(r"\b[1-9]\d{1,2}0", "decade"),
            maybe(SPACE + oneof(self.DATESUFFIXES, "dateSuffix"))            
        ])
        match = regex.fullmatch(pattern, value, regex.IGNORECASE)
        if not match:
            return None
        if 'decade' in match.groupdict():
            decade = int(match.group('decade'))
        span = YearSpan(decade, decade + 9, value)
        return span   
    

    def matchDecadeToDecade(self, value: str) -> YearSpan:
        # e.g. "Années 1950 à 1960"
        pattern = "".join([
            maybe(oneof(self.DATEPREFIXES, "datePrefix") + SPACE),
            r"(?:les\s)?années\s",
            group(r"\b[1-9]\d{1,2}0", "decade1"),
            oneof(self.DATESEPARATORS),
            group(r"\b[1-9]\d{1,2}0", "decade2"),
            maybe(SPACE + oneof(self.DATESUFFIXES, "dateSuffix")),
            maybe(SPACE + "Jahre")
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