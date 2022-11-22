# =============================================================================
# Package   : yearspans
# Module    : yearspanmatcher_en.py
# Version   : Draft 0.1
# Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
# Contact   : ceri.binding@southwales.ac.uk
# Project   : ReMatch
# Summary   : YearSpan matcher (English)
# Require   :
# Imports   : regex, enums, relib, yearspan
# Example   : replaces module "en.py" - then create other language versions
# License   : https://creativecommons.org/licenses/by/4.0/ [CC BY 4.0]
# =============================================================================
# History
# 14/02/2020 CFB Initially created script
# =============================================================================
import regex

from . import enums
from .relib import maybe, oneof, group, zeroormore, oneormore, SPACE, SPACEORDASH, NUMERICYEAR, patterns
from .yearspan import YearSpan
from .yearspanmatcher_base import YearSpanMatcherBase


class YearSpanMatcherEN(YearSpanMatcherBase):

    def __init__(self):
        super(YearSpanMatcherEN, self).__init__("en")
        self.CENTURY = r"C(?:entury)?"
        self.MILLENNIUM = r"millennium"

    def matchMonthYear(self, value: str) -> YearSpan:
        year = 0

        pattern = "".join([
            maybe(oneof(self.DATEPREFIXES, "datePrefix") + SPACE),
            oneof(self.MONTHNAMES, "monthName"),
            SPACEORDASH,
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
            year = self.PRESENT - year
        span = YearSpan(year, year, value)
        return span

    def matchSeasonYear(self, value: str) -> YearSpan:
        # e.g. "early Summer 1950 AD"
        #prefixEnum = None
        #suffixEnum = None
        #monthEnum = None
        year = 0
        pattern = "".join([
            maybe(oneof(self.DATEPREFIXES, "datePrefix") + SPACE),
            oneof(self.SEASONNAMES, "seasonName"),
            SPACEORDASH,
            group(NUMERICYEAR, "year"),
            maybe(SPACE + oneof(self.DATESUFFIXES, "dateSuffix"))
        ])
        match = regex.fullmatch(pattern, value, regex.IGNORECASE)
        if not match:
            return None
        # if 'datePrefix' in match.groupdict():
            #prefixEnum = getDatePrefixEnum(match.group('datePrefix'))
        if 'dateSuffix' in match.groupdict():
            suffixEnum = self.getDateSuffixEnum(match.group('dateSuffix'))
        # if 'seasonName' in match.groupdict():
            #seasonEnum = getSeasonNameEnum(match.group('monthName'))
        if 'year' in match.groupdict():
            year = int(match.group('year'))
        if (suffixEnum == enums.DateSuffix.BC):
            year *= -1
        elif (suffixEnum == enums.DateSuffix.BP):
            year = self.PRESENT - year
        span = YearSpan(year, year, value)
        return span

    def matchCardinalCentury(self, value: str) -> YearSpan:
        # e.g. "early 11C AD"
        prefixEnum = None
        suffixEnum = None
        centuryNo = 0

        pattern = "".join([
            maybe(oneof(self.DATEPREFIXES, "datePrefix") + maybe(SPACE)),
            oneof(self.CARDINALS, "cardinal"),
            maybe(SPACEORDASH),
            self.CENTURY,  # + "C(?:entury)?",
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
            centuryNo = self.getCardinalValue(match.group('cardinal'))
        span = self.getCenturyYearSpan(centuryNo, prefixEnum, suffixEnum)
        span.label = value
        return span

    def matchCardinalToCardinalCentury(self, value: str) -> YearSpan:
        # e.g. "early 11th to late 12th century AD"
        prefixEnum1 = None
        prefixEnum2 = None
        suffixEnum = None
        fromCenturyNo = 0
        toCenturyNo = 0
        pattern = "".join([
            maybe(oneof(self.DATEPREFIXES, "datePrefix1") + SPACE),
            group(r"\d+", "fromCardinal"),
            maybe(SPACE + self.CENTURY),
            oneof(self.DATESEPARATORS),
            maybe(oneof(self.DATEPREFIXES, "datePrefix2") + SPACE),
            group(r"\d+", "toCardinal"),
            (SPACEORDASH + self.CENTURY),
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

    def matchOrdinalCentury(self, value: str) -> YearSpan:
        # e.g. "early eleventh century AD"
        prefixEnum = None
        suffixEnum = None
        centuryNo = 0

        pattern = "".join([
            maybe(oneof(self.DATEPREFIXES, "datePrefix") + maybe(SPACE)),
            oneof(self.ORDINALS, "ordinal"),
            (SPACEORDASH + self.CENTURY),
            maybe(SPACE + oneof(self.DATESUFFIXES, "dateSuffix"))
        ])
        match = regex.fullmatch(pattern, value, regex.IGNORECASE)
        if not match:
            return None
        if 'datePrefix' in match.groupdict():
            prefixEnum = self.getDatePrefixEnum(match.group('datePrefix'))
        if 'dateSuffix' in match.groupdict():
            suffixEnum = self.getDateSuffixEnum(match.group('dateSuffix'))
        if 'ordinal' in match.groupdict():
            centuryNo = self.getOrdinalValue(match.group('ordinal'))
        span = self.getCenturyYearSpan(centuryNo, prefixEnum, suffixEnum)
        span.label = value
        return span

    def matchOrdinalToOrdinalCentury(self, value: str) -> YearSpan:
        # e.g. "early eleventh to late twelfth century AD"
        prefixEnum1 = None
        prefixEnum2 = None
        suffixEnum = None
        fromCenturyNo = 0
        toCenturyNo = 0
        pattern = "".join([
            maybe(oneof(self.DATEPREFIXES, "datePrefix1") + maybe(SPACE)),
            oneof(self.ORDINALS, "fromOrdinal"),
            maybe(SPACEORDASH + self.CENTURY),
            oneof(self.DATESEPARATORS),
            maybe(oneof(self.DATEPREFIXES, "datePrefix2") + maybe(SPACE)),
            oneof(self.ORDINALS, "toOrdinal"),
            maybe(SPACEORDASH + self.CENTURY),
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
        if 'fromOrdinal' in match.groupdict():
            fromCenturyNo = self.getOrdinalValue(match.group('fromOrdinal'))
        if 'toOrdinal' in match.groupdict():
            toCenturyNo = self.getOrdinalValue(match.group('toOrdinal'))
        span1 = self.getCenturyYearSpan(fromCenturyNo, prefixEnum1, suffixEnum)
        span2 = self.getCenturyYearSpan(toCenturyNo, prefixEnum2, suffixEnum)
        span = YearSpan(span1.minYear, span2.maxYear)
        span.label = value
        return span

    def matchOrdinalMillennium(self, value: str) -> YearSpan:
        # e.g. "late 1st millennium AD"
        prefixEnum = None
        suffixEnum = None
        millenniumNo = 0

        pattern = "".join([
            maybe(oneof(self.DATEPREFIXES, "datePrefix") + SPACE),
            oneof(self.ORDINALS, "ordinal"),
            (SPACEORDASH + self.MILLENNIUM),
            maybe(SPACE + oneof(self.DATESUFFIXES, "dateSuffix"))
        ])
        match = regex.fullmatch(pattern, value, regex.IGNORECASE)
        if not match:
            return None
        if 'datePrefix' in match.groupdict():
            prefixEnum = self.getDatePrefixEnum(match.group('datePrefix'))
        if 'dateSuffix' in match.groupdict():
            suffixEnum = self.getDateSuffixEnum(match.group('dateSuffix'))
        if 'ordinal' in match.groupdict():
            millenniumNo = self.getOrdinalValue(match.group('ordinal'))
        span = self.getMillenniumYearSpan(millenniumNo, prefixEnum, suffixEnum)
        span.label = value
        return span

    def matchOrdinalToOrdinalMillennium(self, value: str) -> YearSpan:
        # e.g. "late 1st to early 2nd millennium AD"
        prefixEnum1 = None
        prefixEnum2 = None
        suffixEnum = None
        fromMillenniumNo = 0
        toMillenniumNo = 0

        pattern = "".join([
            maybe(oneof(self.DATEPREFIXES, "datePrefix1") + SPACE),
            oneof(self.ORDINALS, "fromOrdinal"),
            oneof(self.DATESEPARATORS),
            maybe(oneof(self.DATEPREFIXES, "datePrefix2") + SPACE),
            oneof(self.ORDINALS, "toOrdinal"),
            (SPACEORDASH + self.MILLENNIUM),
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
        if 'fromOrdinal' in match.groupdict():
            fromMillenniumNo = self.getOrdinalValue(match.group('fromOrdinal'))
        if 'toOrdinal' in match.groupdict():
            toMillenniumNo = self.getOrdinalValue(match.group('toOrdinal'))
        span1 = self.getMillenniumYearSpan(
            fromMillenniumNo, prefixEnum1, suffixEnum)
        span2 = self.getMillenniumYearSpan(
            toMillenniumNo, prefixEnum2, suffixEnum)
        span = YearSpan(span1.minYear, span2.maxYear, value)
        return span

    def matchYearWithPrefix(self, value: str) -> YearSpan:
        # e.g. "early 1950"
        year = 0
        prefixEnum = None
        suffixEnum = None

        pattern = "".join([
            oneof(self.DATEPREFIXES, "datePrefix"),
            maybe(SPACE),
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
            year = self.PRESENT - year
        span = YearSpan(year, year, value)
        return span

    def matchYearWithSuffix(self, value: str) -> YearSpan:
        # e.g. "1950 AD"
        year = 0
        #prefixEnum = None
        suffixEnum = None

        pattern = "".join([
            maybe(oneof(self.DATEPREFIXES, "datePrefix") + SPACE),
            group(NUMERICYEAR, "year"),
            oneormore(SPACEORDASH + oneof(self.DATESUFFIXES, "dateSuffix"))
        ])
        match = regex.fullmatch(pattern, value, regex.IGNORECASE)
        if not match:
            return None
        # if 'datePrefix' in match.groupdict():
            #prefixEnum = self.__getDatePrefixEnum(match.group('datePrefix'))
        if 'dateSuffix' in match.groupdict():
            suffixEnum = self.getDateSuffixEnum(match.group('dateSuffix'))
        if 'year' in match.groupdict():
            year = int(match.group('year'))
        if (suffixEnum == enums.DateSuffix.BC):
            year *= -1
        elif (suffixEnum == enums.DateSuffix.BP):
            year = self.PRESENT - year
        span = YearSpan(year, year, value)
        return span

    # e.g. "1537-13+20"
    def matchYearWithTolerance1(self, value: str) -> YearSpan:
        year = 0
        tolA = 0
        tolB = 0

        pattern = "".join([
            group(NUMERICYEAR, "year"),
            group(r"[+-]\d+", "tolA"),
            group(r"[+-]\d+", "tolB")
        ])
        match = regex.fullmatch(pattern, value, regex.IGNORECASE)
        if not match:
            return None
        if 'year' in match.groupdict():
            year = int(match.group('year'))
        if 'tolA' in match.groupdict():
            tolA = int(match.group('tolA'))
        if 'tolB' in match.groupdict():
            tolB = int(match.group('tolB'))

        span = YearSpan(year + tolA, year + tolB, value)
        return span

    # e.g. "1537±9"
    def matchYearWithTolerance2(self, value: str) -> YearSpan:
        year = 0
        tol = 0

        pattern = "".join([
            group(NUMERICYEAR, "year"),
            maybe(SPACE),
            r"±",
            group(r"\d+", "tol")
        ])
        match = regex.fullmatch(pattern, value, regex.IGNORECASE)
        if not match:
            return None
        if 'year' in match.groupdict():
            year = int(match.group('year'))
        if 'tol' in match.groupdict():
            tol = int(match.group('tol'))

        span = YearSpan(year - tol, year + tol, value)
        return span

    # e.g. 1674-75, 1672-8

    def matchYearToYear2(self, value: str) -> YearSpan:
        fromYear = None
        toYear = None
        suffixEnum = None

        pattern = "".join([
            maybe(oneof(self.DATEPREFIXES, "datePrefix") + SPACE),
            # group(NUMERICYEAR,"fromYear"),
            group(r"[+-]?\d{3,}", "fromYear"),
            oneof(self.DATESEPARATORS),
            group(r"[+-]?\d{1,2}", "toYear"),  # group(NUMERICYEAR,"toYear"),
            maybe(SPACE + oneof(self.DATESUFFIXES, "dateSuffix"))
        ])
        match = regex.fullmatch(pattern, value, regex.IGNORECASE)
        if not match:
            return None
        # if 'datePrefix' in match.groupdict():
            #prefixEnum = getDatePrefixEnum(match.group('datePrefix'))
        if 'dateSuffix' in match.groupdict():
            suffixEnum = self.getDateSuffixEnum(match.group('dateSuffix'))
        if 'fromYear' in match.groupdict():
            fromYear = int(match.group('fromYear'))
        if 'toYear' in match.groupdict():
            toYear = int(match.group('toYear'))
        if (fromYear is not None and toYear is None):
            toYear = fromYear
        elif (toYear is not None and fromYear is None):
            fromYear = toYear

        if (toYear < fromYear and suffixEnum == enums.DateSuffix.AD):
            if (toYear < 10):
                toYear = fromYear - (fromYear % 10) + toYear
            elif (toYear < 100):
                toYear = fromYear - (fromYear % 100) + toYear

        if (suffixEnum == enums.DateSuffix.BC):
            fromYear *= -1
            toYear *= -1
        elif (suffixEnum == enums.DateSuffix.BP):
            fromYear = self.PRESENT - fromYear
            toYear = self.PRESENT - toYear

        return YearSpan(fromYear, toYear, value)

    # e.g. 1674 - 1715

    def matchYearToYear(self, value: str) -> YearSpan:
        # allowable numeric years slackened to allow for ADS data
        fromYear = None
        toYear = None
        #datePrefix = None
        suffixEnum = None

        pattern = "".join([
            maybe(oneof(self.DATEPREFIXES, "datePrefix") + SPACE),
            group(r"[+-]?\d+", "fromYear"),  # group(NUMERICYEAR,"fromYear"),
            oneof(self.DATESEPARATORS),
            group(r"[+-]?\d+", "toYear"),  # group(NUMERICYEAR,"toYear"),
            maybe(SPACE + oneof(self.DATESUFFIXES, "dateSuffix"))
        ])
        match = regex.fullmatch(pattern, value, regex.IGNORECASE)
        if not match:
            return None
        # if 'datePrefix' in match.groupdict():
            #prefixEnum = getDatePrefixEnum(match.group('datePrefix'))
        if 'dateSuffix' in match.groupdict():
            suffixEnum = self.getDateSuffixEnum(match.group('dateSuffix'))
        if 'fromYear' in match.groupdict():
            fromYear = int(match.group('fromYear'))
        if 'toYear' in match.groupdict():
            toYear = int(match.group('toYear'))
        if (fromYear and toYear is None):
            toYear = fromYear
        elif (toYear and fromYear is None):
            fromYear = toYear
        if (suffixEnum == enums.DateSuffix.BC):
            fromYear *= -1
            toYear *= -1
        elif (suffixEnum == enums.DateSuffix.BP):
            fromYear = self.PRESENT - fromYear
            toYear = self.PRESENT - toYear
        return YearSpan(fromYear, toYear, value)

    def matchYearToYear2(self, value: str) -> YearSpan:
        fromYear = None
        toYear = None
        #datePrefix = None
        suffixEnum = None

        pattern = "".join([
            maybe(oneof(self.DATEPREFIXES, "datePrefix") + SPACE),
            group(r"[+-]?\d{3,}", "fromYear"),  
            oneof(self.DATESEPARATORS),
            group(r"[+-]?\d{1,2}", "toYear"),  
            maybe(SPACE + oneof(self.DATESUFFIXES, "dateSuffix"))
        ])
        match = regex.fullmatch(pattern, value, regex.IGNORECASE)
        if not match:
            return None
        # if 'datePrefix' in match.groupdict():
            #prefixEnum = getDatePrefixEnum(match.group('datePrefix'))
        if 'dateSuffix' in match.groupdict():
            suffixEnum = self.getDateSuffixEnum(match.group('dateSuffix'))
        if 'fromYear' in match.groupdict():
            fromYear = int(match.group('fromYear'))
        if 'toYear' in match.groupdict():
            toYear = int(match.group('toYear'))
        if (fromYear and toYear is None):
            toYear = fromYear
        elif (toYear and fromYear is None):
            fromYear = toYear
        if (toYear < 10):
            toYear = fromYear - (fromYear % 10) + toYear
        else:
            toYear = fromYear - (fromYear % 100) + toYear
        if (suffixEnum == enums.DateSuffix.BC):
            fromYear *= -1
            toYear *= -1
        elif (suffixEnum == enums.DateSuffix.BP):
            fromYear = self.PRESENT - fromYear
            toYear = self.PRESENT - toYear
        return YearSpan(fromYear, toYear, value)

    def matchLoneDecade(self, value: str) -> YearSpan:
        # e.g. "1950's"
        #datePrefix = None
        #dateSuffix = None
        decade = 0

        pattern = "".join([
            maybe(oneof(self.DATEPREFIXES, "datePrefix") + SPACE),
            group(r"\b[1-9]\d{1,2}0", "decade") + r"\'?s",
            maybe(SPACE + oneof(self.DATESUFFIXES, "dateSuffix"))
        ])
        match = regex.fullmatch(pattern, value, regex.IGNORECASE)
        if not match:
            return None
        # if 'datePrefix' in match.groupdict():
            #prefixEnum = getDatePrefixEnum(match.group('datePrefix'))
        # if 'dateSuffix' in match.groupdict():
            #suffixEnum = getDateSuffixEnum(match.group('dateSuffix'))
        if 'decade' in match.groupdict():
            decade = int(match.group('decade'))
        span = YearSpan(decade, decade + 9, value)
        return span

    def matchDecadeToDecade(self, value: str) -> YearSpan:
        # e.g. "1950's to 1960's"
        pattern = "".join([
            maybe(oneof(self.DATEPREFIXES, "datePrefix") + SPACE),
            group(r"\b[1-9]\d{1,2}0", "decade1") + r"\'?s",
            oneof(self.DATESEPARATORS),
            group(r"\b[1-9]\d{1,2}0", "decade2") + r"\'?s",
            maybe(SPACE + oneof(self.DATESUFFIXES, "dateSuffix"))
        ])
        match = regex.fullmatch(pattern, value, regex.IGNORECASE)
        if not match:
            return None
        # if 'datePrefix' in match.groupdict():
            #prefixEnum = self.__getDatePrefixEnum(match.group('datePrefix'))
        # if 'dateSuffix' in match.groupdict():
            #suffixEnum = self.__getDateSuffixEnum(match.group('dateSuffix'))
        if 'decade1' in match.groupdict():
            decade1 = int(match.group('decade1'))
        if 'decade2' in match.groupdict():
            decade2 = int(match.group('decade2'))
        span = YearSpan(decade1, decade2 + 9, value)
        return span

    def matchNamedPeriod(self, value: str) -> YearSpan:
        # e.g. "Medieval"
        span = None
        pattern = "".join([
            maybe(oneof(self.DATEPREFIXES, "datePrefix") + SPACE),
            oneof(self.PERIODNAMES, "periodName")
        ])
        match = regex.fullmatch(pattern, value, regex.IGNORECASE)
        if not match:
            return None
        if 'periodName' in match.groupdict():
            span = self.getNamedPeriodValue(match.group('periodName'))
        span.label = value
        return span

    def matchNamedToNamedPeriod(self, value: str) -> YearSpan:
        # e.g. "Medieval to modern"
        pattern = "".join([
            maybe(oneof(self.DATEPREFIXES, "datePrefix") + SPACE),
            oneof(self.PERIODNAMES, "periodName1"),
            oneof(self.DATESEPARATORS),
            oneof(self.PERIODNAMES, "periodName2")
        ])
        match = regex.fullmatch(pattern, value, regex.IGNORECASE)
        if not match:
            return None
        # if 'datePrefix' in match.groupdict():
            #prefixEnum = self.__getDatePrefixEnum(match.group('datePrefix'))
        if 'periodName1' in match.groupdict():
            span1 = self.getNamedPeriodValue(match.group('periodName1'))
        if 'periodName2' in match.groupdict():
            span2 = self.getNamedPeriodValue(match.group('periodName2'))
        if (span1 and span2 is None):
            span2 = span1
        elif (span2 and span1 is None):
            span1 = span2
        elif (span1 is None and span2 is None):
            span1 = YearSpan()
            span2 = YearSpan()
        span = YearSpan(span1.minYear, span2.maxYear, value)
        return span

    def matchLoneYear(self, value: str) -> YearSpan:
        # wouldnt normally allow just a number - one-off to cater for ADS data for ReMatch ingest
        suffixEnum = None
        year = 0
        pattern = "".join([
            group(NUMERICYEAR, "year"),
            maybe(r"\+"),
            maybe(SPACE + oneof(self.DATESUFFIXES, "dateSuffix"))
        ])
        match = regex.fullmatch(pattern, value, regex.IGNORECASE)
        if not match:
            return None
        if 'year' in match.groupdict():
            year = int(match.group('year'))
        if 'dateSuffix' in match.groupdict():
            suffixEnum = self.getDateSuffixEnum(match.group('dateSuffix'))
        if (suffixEnum == enums.DateSuffix.BC):
            year *= -1
        elif (suffixEnum == enums.DateSuffix.BP):
            year = self.PRESENT - year
        span = YearSpan(year, year, value)
        return span
