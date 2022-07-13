# =============================================================================
# Package   : yearspans
# Module    : yearspanmatcher_sv.py
# Version   : Draft 0.1
# Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
# Contact   : ceri.binding@southwales.ac.uk
# Project   : ReMatch
# Summary   : YearSpan matcher (Swedish)
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


class YearSpanMatcherSV(YearSpanMatcherEN):

    def __init__(self):
        super(YearSpanMatcherEN, self).__init__("sv")   
        self.MILLENNIUM = r"millenniet"
        self.CENTURY = r"århundradet?" 

    def matchCardinalCentury(self, value: str) -> YearSpan:
        # e.g. "Tidigt 1100-tal e.Kr."    
        prefixEnum = None
        suffixEnum = None
        centuryNo = 0

        pattern = "".join([
            maybe(oneof(self.DATEPREFIXES,"datePrefix") + SPACE),
            group(r"\d+", "cardinal") + r"00-tal(?:et)?",
            maybe(SPACE + oneof(self.DATESUFFIXES, "dateSuffix"))
        ])
        match = regex.fullmatch(pattern, value, regex.IGNORECASE)
        if not match:
            return None
        if 'datePrefix' in match.groupdict():
            prefixEnum = self.getDatePrefixEnum(match.group('datePrefix')) 
        if 'dateSuffix' in match.groupdict():
            suffixEnum = self.getDateSuffixEnum(match.group('dateSuffix'))
        if 'cardinal' in match.groupdict():
            centuryNo = int(match.group('cardinal'))            
        span = self.getCenturyYearSpan(centuryNo, prefixEnum, suffixEnum)
        span.label = value
        return span     
              

    def matchCardinalToCardinalCentury(self, value: str) -> YearSpan:
        # e.g. "tidigt 1000-tal till slutet av 1100-talet e.Kr." (early 11th to late 12th century AD)
        prefixEnum1 = None
        prefixEnum2 = None
        suffixEnum = None
        fromCenturyNo = 0
        toCenturyNo = 0
        pattern = "".join([
            maybe(oneof(self.DATEPREFIXES, "datePrefix1") + SPACE),
            group(r"\d+", "fromCardinal") + r"00(?:-tal(?:et)?)?",
            oneof(self.DATESEPARATORS),
            maybe(oneof(self.DATEPREFIXES, "datePrefix2") + SPACE),
            group(r"\d+", "toCardinal") + r"00-tal(?:et)?",
            maybe(SPACE + oneof(self.DATESUFFIXES, "dateSuffix"))
        ])    
        match = regex.fullmatch(pattern, value, regex.IGNORECASE)
        if not match:
            return None
        if 'datePrefix1' in match.groupdict():
            prefixEnum1 = self.getDatePrefixEnum(match.group('datePrefix1')) 
        if 'datePrefix2' in match.groupdict():
            prefixEnum2 = self.getDatePrefixEnum(match.group('datePrefix2')) 
        if 'dateSuffix' in match.groupdict():
            suffixEnum = self.getDateSuffixEnum(match.group('dateSuffix'))
        if 'fromCardinal' in match.groupdict():
            fromCenturyNo = int(match.group('fromCardinal')) 
        if 'toCardinal' in match.groupdict():
            toCenturyNo = int(match.group('toCardinal')) 
        span1 = self.getCenturyYearSpan(fromCenturyNo, prefixEnum1, suffixEnum)
        span2 = self.getCenturyYearSpan(toCenturyNo, prefixEnum2, suffixEnum)
        
        span = YearSpan(span1.minYear, span2.maxYear, value)
        #span.label = value
        return span

    def matchLoneDecade(self, value: str) -> YearSpan:
        # e.g. "1950-tallet"
        #datePrefix = None
        #dateSuffix = None
        decade = 0
        
        pattern = "".join([
            maybe(oneof(self.DATEPREFIXES, "datePrefix") + SPACE),
            group(r"\b[1-9]\d{1,2}0", "decade") + r"(?:\-(?:tal(?:et)?)?)",
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
        # e.g. "1950- til 1960-tallet"
        decade1 = 0
        decade2 = 0

        pattern = "".join([
            maybe(oneof(self.DATEPREFIXES, "datePrefix") + SPACE),
            group(r"\b[1-9]\d{1,2}0", "decade1") + r"(?:\-(?:tal(?:et)?)?)",
            oneof(self.DATESEPARATORS),
            group(r"\b[1-9]\d{1,2}0", "decade2") + r"(?:\-(?:tal(?:et)?)?)",
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