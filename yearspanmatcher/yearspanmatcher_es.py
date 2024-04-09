"""
=============================================================================
Project   : ARIADNEplus
Package   : yearspanmatcher
Module    : yearspanmatcher_es.py
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Summary   : YearSpan matcher (Spanish)
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
from .relib import maybe, oneof, group, zeroormore, oneormore, SPACE, SPACEORDASH, NUMERICYEAR, patterns
from .yearspan import YearSpan
from .yearspanmatcher_en import YearSpanMatcherEN


class YearSpanMatcherES(YearSpanMatcherEN):

    def __init__(self) -> None:
        super(YearSpanMatcherEN, self).__init__("es")
        self.MILLENNIUM = r"milenio"
        self.CENTURY = r"siglo"

    def matchMonthYear(self, value: str) -> YearSpan:
        year = 0

        pattern = "".join([
            maybe(oneof(self.DATEPREFIXES, "datePrefix") + SPACE),
            oneof(self.MONTHNAMES, "monthName"),
            SPACE,
            maybe(r"de\s"),
            group(NUMERICYEAR, "year"),
            SPACE,
            oneof(self.DATESUFFIXES, "dateSuffix")
        ])
        match = regex.fullmatch(pattern, value, regex.IGNORECASE)

        if not match:
            return None

        if "year" in match.groupdict():
            year = int(match.group("year"))
        if "dateSuffix" in match.groupdict():
            suffixEnum = self.getDateSuffixEnum(match.group('dateSuffix'))
            if (suffixEnum == enums.DateSuffix.BC):
                year *= -1
            elif (suffixEnum == enums.DateSuffix.BP):
                year = self.present - year
        span = YearSpan(year, year, value)
        return span

    def matchLoneDecade(self, value: str) -> YearSpan:
        # e.g. la década de 1950"
        decade = 0

        pattern = "".join([
            maybe(oneof(self.DATEPREFIXES, "datePrefix") + SPACE),
            r"la década de",
            SPACE,
            group(r"[1-9]\d{1,2}0", "decade")
        ])
        match = regex.fullmatch(pattern, value, regex.IGNORECASE)
        if not match:
            return None
        if 'decade' in match.groupdict():
            decade = int(match.group('decade'))
        span = YearSpan(decade, decade + 9, value)
        return span

    def matchDecadeToDecade(self, value: str) -> YearSpan:
        # e.g. "finales de la década de 1950 hasta finales de la década de 1960"
        decade1 = 0
        decade2 = 0

        pattern = "".join([
            maybe(oneof(self.DATEPREFIXES, "datePrefix1") + SPACE),
            r"la década de" + SPACE,
            group(r"[1-9]\d{1,2}0", "decade1"),
            oneof(self.DATESEPARATORS),
            maybe(oneof(self.DATEPREFIXES, "datePrefix2") + SPACE),
            r"la década de" + SPACE,
            group(r"[1-9]\d{1,2}0", "decade2")
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

    def matchCardinalCentury(self, value: str) -> YearSpan:
        # e.g. "early 11C AD"
        prefixEnum = None
        suffixEnum = None
        centuryNo = 0

        pattern = "".join([
            maybe(oneof(self.DATEPREFIXES, "datePrefix") + SPACE),
            r"siglo\s",
            oneof(self.CARDINALS, "cardinal"),
            zeroormore(SPACE + oneof(self.DATESUFFIXES, "dateSuffix"))
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

    def matchOrdinalCentury(self, value: str) -> YearSpan:
        # e.g. "early 11th century AD"
        prefixEnum = None
        suffixEnum = None
        centuryNo = 0

        pattern = "".join([
            maybe(oneof(self.DATEPREFIXES, "datePrefix") + SPACE),
            r"siglo\s",
            oneof(self.ORDINALS, "ordinal"),
            zeroormore(SPACE + oneof(self.DATESUFFIXES, "dateSuffix"))
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
        # e.g. "principios del siglo XII a finales del siglo XI a.C."
        prefixEnum1 = None
        prefixEnum2 = None
        suffixEnum = None
        fromCenturyNo = 0
        toCenturyNo = 0
        pattern = "".join([
            maybe(oneof(self.DATEPREFIXES, "datePrefix1") + SPACE),
            r"siglo\s",
            oneof(self.ORDINALS, "fromOrdinal"),
            oneof(self.DATESEPARATORS),
            maybe(oneof(self.DATEPREFIXES, "datePrefix2") + SPACE),
            r"siglo\s",
            oneof(self.ORDINALS, "toOrdinal"),
            zeroormore(SPACE + oneof(self.DATESUFFIXES, "dateSuffix"))
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
            SPACE,
            "milenio",
            zeroormore(SPACE + oneof(self.DATESUFFIXES, "dateSuffix"))
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
            SPACEORDASH,
            r"milenio",
            zeroormore(SPACE + oneof(self.DATESUFFIXES, "dateSuffix"))
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
