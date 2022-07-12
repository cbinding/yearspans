# =============================================================================
# Package   : yearspans
# Module    : yearspanmatcher_nl.py
# Version   : Draft 0.1
# Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
# Contact   : ceri.binding@southwales.ac.uk
# Project   : ReMatch
# Summary   : YearSpan matcher (Dutch)
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
import enums
from relib import maybe, oneof, group, zeroormore, oneormore, SPACE, SPACEORDASH, NUMERICYEAR, patterns
from yearspan import YearSpan
from yearspanmatcher_en import YearSpanMatcherEN


class YearSpanMatcherNL(YearSpanMatcherEN):

    def __init__(self):
        super(YearSpanMatcherEN, self).__init__("nl")  
        self.MILLENNIUM = r"millennium"
        self.CENTURY = r"eeuw"         
              

    def matchLoneDecade(self, value: str) -> YearSpan:
        # e.g. "1950au"
        #datePrefix = None
        #dateSuffix = None
        decade = 0
        
        pattern = "".join([
            maybe(oneof(self.DATEPREFIXES, "datePrefix") + SPACE),
            (r"jaren" + SPACE),
            group(r"\b[1-9]\d{1,2}0", "decade"),
            maybe(SPACE + oneof(self.DATESUFFIXES, "dateSuffix"))
        ])
        match = regex.fullmatch(pattern, value, regex.IGNORECASE)
        if not match:
            return None
        #if 'datePrefix' in match.groupdict():
            #prefixEnum = getDatePrefixEnum(match.group('datePrefix')) 
        #if 'dateSuffix' in match.groupdict():
            #suffixEnum = getDateSuffixEnum(match.group('dateSuffix')) 
        if 'decade' in match.groupdict():
            decade = int(match.group('decade'))
        span = YearSpan(decade, decade + 9, value)
        return span   
    

    def matchDecadeToDecade(self, value: str) -> YearSpan:
        # e.g. "1950au i 1960au"
        pattern = "".join([
            maybe(oneof(self.DATEPREFIXES, "datePrefix") + SPACE),
            (r"jaren" + SPACE),
            group(r"\b[1-9]\d{1,2}0", "decade1"),
            oneof(self.DATESEPARATORS),
            group(r"\b[1-9]\d{1,2}0", "decade2"),
            maybe(SPACE + oneof(self.DATESUFFIXES, "dateSuffix"))
        ])
        match = regex.fullmatch(pattern, value, regex.IGNORECASE)
        if not match:
            return None
        #if 'datePrefix' in match.groupdict():
            #prefixEnum = self.__getDatePrefixEnum(match.group('datePrefix')) 
        #if 'dateSuffix' in match.groupdict():
            #suffixEnum = self.__getDateSuffixEnum(match.group('dateSuffix')) 
        if 'decade1' in match.groupdict():
            decade1 = int(match.group('decade1'))
        if 'decade2' in match.groupdict():
            decade2 = int(match.group('decade2'))
        span = YearSpan(decade1, decade2 + 9, value)
        return span