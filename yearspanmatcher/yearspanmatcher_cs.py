"""
=============================================================================
Project   : ATRIUM
Package   : yearspanmatcher
Module    : yearspanmatcher_cs.py
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Summary   : YearSpan matcher (Czech)
Imports   : regex, enums, relib, yearspan
Example   :
License   : https://github.com/cbinding/yearspans/blob/main/LICENSE.md
=============================================================================
History
05/04/2024 CFB Initially created script
=============================================================================
"""
import regex
from . import enums
from .relib import maybe, oneof, group, zeroormore, oneormore, SPACE, SPACEORDASH, NUMERICYEAR, patterns
from .yearspan import YearSpan
from .yearspanmatcher_en import YearSpanMatcherEN


class YearSpanMatcherCS(YearSpanMatcherEN):

    def __init__(self) -> None:
        super(YearSpanMatcherEN, self).__init__("cs")
        self.MILLENNIUM = r"tisíciletí"
        self.CENTURY = r"století"


    def matchSeasonYear(self, value: str) -> YearSpan:
        year = 0

        pattern = "".join([
            maybe(oneof(self.DATEPREFIXES, "datePrefix") + SPACE),
            oneof(self.SEASONNAMES, "seasonName"),
            (SPACE + "roku" + SPACE),
            group(NUMERICYEAR, "year"),
            maybe(SPACE + oneof(self.DATESUFFIXES, "dateSuffix"))
        ])
        match = regex.fullmatch(pattern, value, regex.IGNORECASE)
        if not match:
            return None

        if "year" in match.groupdict():
            year = int(match.group("year"))
        if 'dateSuffix' in match.groupdict():
            suffixEnum = self.getDateSuffixEnum(match.group('dateSuffix'))
        if (suffixEnum == enums.DateSuffix.BC):
            year *= -1
        elif (suffixEnum == enums.DateSuffix.BP):
            year = self.present - year
        span = YearSpan(year, year, value)
        return span

    def matchYearWithPrefix(self, value: str) -> YearSpan:
        # e.g. "early 1950"
        year = 0
        prefixEnum = None
        suffixEnum = None

        pattern = "".join([
            oneof(self.DATEPREFIXES, "datePrefix"),
            (SPACE + "roku" + SPACE),
            group(NUMERICYEAR, "year"),
            maybe(SPACEORDASH + oneof(self.DATESUFFIXES, "dateSuffix"))
        ])
        match = regex.fullmatch(pattern, value, regex.IGNORECASE)
        if not match:
            return None
        if 'datePrefix' in match.groupdict():
            prefixEnum = self.getDatePrefixEnum(match.group('datePrefix'))
        if 'dateSuffix' in match.groupdict():
            suffixEnum = self.getDateSuffixEnum(match.group('dateSuffix'))
        if 'year' in match.groupdict():
            year = int(match.group('year'))
        if (suffixEnum == enums.DateSuffix.BC):
            year *= -1
        elif (suffixEnum == enums.DateSuffix.BP):
            year = self.present - year
        span = YearSpan(year, year, value)
        return span


    def matchLoneDecade(self, value: str) -> YearSpan:
        # e.g. "1950er"
        decade = 0

        pattern = "".join([
            maybe(oneof(self.DATEPREFIXES, "datePrefix") + SPACE),
            group(r"\b\d0", "decade"),
            group(r"\. l[eé]ta?"),
            maybe(group(r"\s\d{1,2}", "century") + "\."), 
            SPACE + "století",
            maybe(SPACE + oneof(self.DATESUFFIXES, "dateSuffix"))           
        ])
        match = regex.fullmatch(pattern, value, regex.IGNORECASE)
        if not match:
            return None
        if 'decade' in match.groupdict():
            decade = int(match.group('decade'))
        if 'century' in match.groupdict():
            century = (int(match.group('century')) -1) * 100
            decade += century
        span = YearSpan(decade, decade + 9, value)
        return span

    def matchDecadeToDecade(self, value: str) -> YearSpan:
        decade1 = 0
        decade2 = 0
        pattern = "".join([
            maybe(oneof(self.DATEPREFIXES, "datePrefix") + SPACE),
            group(r"\b\d0", "decade1") + r"\.",
            oneof(self.DATESEPARATORS),
            group(r"\b\d0", "decade2") + r"\.",
            group(r"\sl[eé]ta?"),
            maybe(group(r"\s\d{1,2}", "century") + "\."),
            SPACE + "století",
            maybe(SPACE + oneof(self.DATESUFFIXES, "dateSuffix"))            
        ])
        match = regex.fullmatch(pattern, value, regex.IGNORECASE)
        if not match:
            return None
        if 'decade1' in match.groupdict():
            decade1 = int(match.group('decade1'))
        if 'decade2' in match.groupdict():
            decade2 = int(match.group('decade2'))
        if 'century' in match.groupdict():
            century = (int(match.group('century')) - 1) * 100
            decade1 += century
            decade2 += century
        span = YearSpan(decade1, decade2 + 9, value)
        return span
