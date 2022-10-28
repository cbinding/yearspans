# =============================================================================
# Package   : yearspans
# Module    : yearspanmatcher_base.py
# Version   : Draft 0.1
# Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
# Contact   : ceri.binding@southwales.ac.uk
# Project   : ReMatch
# Summary   : YearSpanMatcherBase - abstract class for concrete language specific
# Require   :
# Imports   : abc, enums, relib, yearspan
# Example   :
# License   : http://creativecommons.org/publicdomain/zero/1.0/ [CC0]
# =============================================================================
# History
# 14/02/2020 CFB Initially created script
# =============================================================================
import abc      # for Abstract Base Classes
#import regex
from . import enums  # Useful enumerations for use in ReMatch
from . import relib  # Regular Expressions pattern library and associated functionality
#from relib import maybe, oneof, group, zeroormore, oneormore, SPACE, SPACEORDASH, NUMERICYEAR
from .yearspan import YearSpan


class YearSpanMatcherBase(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, language="en", present=2000):

        self.LANGUAGE = language  # default overridden in concrete classes
        # for use in calculating BP dates; may be overridden (sometimes BP refers to 1950)
        self.PRESENT = present

        # restrict to language specific patterns
        self.patterns = relib.patterns[language]
        # ["EARLY", "MID", "LATE", "etc."]
        self.DATEPREFIXES = list(
            map(lambda item: item['pattern'], self.patterns["dateprefix"]))
        # ["AD", "BC", "BP", "etc."]
        self.DATESUFFIXES = list(
            map(lambda item: item['pattern'], self.patterns["datesuffix"]))
        # ["to", "-", "and", "etc."]
        self.DATESEPARATORS = list(
            map(lambda item: item['pattern'], self.patterns["dateseparator"]))
        # ["Monday", "Tuesday", "etc."]
        self.DAYNAMES = list(
            map(lambda item: item['pattern'], self.patterns["daynames"]))
        # ["January", "February", "etc."]
        self.MONTHNAMES = list(
            map(lambda item: item['pattern'], self.patterns["monthnames"]))
        # ["Spring", "Summer", "etc."]
        self.SEASONNAMES = list(
            map(lambda item: item['pattern'], self.patterns["seasonnames"]))
        # ["one", "two", "three", "etc."]
        self.CARDINALS = list(
            map(lambda item: item['pattern'], self.patterns["cardinals"]))
        # ["first", "second", "third", "etc."]
        self.ORDINALS = list(
            map(lambda item: item['pattern'], self.patterns["ordinals"]))
        # ["Elizabethan", "Victorian", "etc."]
        self.PERIODNAMES = list(
            map(lambda item: item['pattern'], self.patterns["periodnames"]))

    def getDayNameEnum(self, s: str) -> enums.Day:
        value = relib.getValue(s, self.patterns["daynames"])
        if (value is None):
            value = Day.NONE
        return value

    def getMonthNameEnum(self, s: str) -> enums.Month:
        value = relib.getValue(s, self.patterns["monthnames"])
        if (value is None):
            value = Month.NONE
        return value

    def getSeasonNameEnum(self, s: str) -> enums.Season:
        value = relib.getValue(s, self.patterns["seasonnames"])
        if (value is None):
            value = Season.NONE
        return value

    def getCardinalValue(self, s: str) -> int:  # Cardinal:
        value = relib.getValue(s, self.patterns["cardinals"])
        if (value is None):
            value = 0
        return value

    def getOrdinalValue(self, s: str) -> int:  # Ordinal:
        value = relib.getValue(s, self.patterns["ordinals"])
        if (value is None):
            value = 0
        return value

    def getDatePrefixEnum(self, s: str) -> enums.DatePrefix:
        value = relib.getValue(s, self.patterns["dateprefix"])
        if (value is None):
            value = enums.DatePrefix.NONE
        return value

    def getDateSuffixEnum(self, s: str) -> enums.DateSuffix:
        return relib.getValue(s, self.patterns["datesuffix"])
        if (value is None):
            value = enums.DateSuffix.NONE
        return value

    def getNamedPeriodValue(self, s: str) -> YearSpan:
        value = relib.getValue(s, self.patterns["periodnames"])
        if (value is None):
            value = YearSpan()
        return value

    def match(self, value: str) -> YearSpan:
        span = None
        cleanValue = (value or "").strip()
        if not span:
            span = self.matchMonthYear(cleanValue)
        if not span:
            span = self.matchSeasonYear(cleanValue)
        if not span:
            span = self.matchCardinalCentury(cleanValue)
        if not span:
            span = self.matchOrdinalCentury(cleanValue)
        if not span:
            span = self.matchCardinalToCardinalCentury(cleanValue)
        if not span:
            span = self.matchOrdinalToOrdinalCentury(cleanValue)
        if not span:
            span = self.matchOrdinalMillennium(cleanValue)
        if not span:
            span = self.matchOrdinalToOrdinalMillennium(cleanValue)
        if not span:
            span = self.matchYearWithPrefix(cleanValue)
        if not span:
            span = self.matchYearWithSuffix(cleanValue)
        if not span:
            span = self.matchYearToYear2(cleanValue)
        if not span:
            span = self.matchYearToYear(cleanValue)
        if not span:
            span = self.matchLoneDecade(cleanValue)
        if not span:
            span = self.matchDecadeToDecade(cleanValue)
        if not span:
            span = self.matchNamedPeriod(cleanValue)
        if not span:
            span = self.matchNamedToNamedPeriod(cleanValue)
        if not span:
            span = self.matchLoneYear(cleanValue)
        if span:
            span.label = cleanValue
        return span

    @abc.abstractmethod
    def matchMonthYear(self, value):
        return

    @abc.abstractmethod
    def matchSeasonYear(self, value):
        return

    @abc.abstractmethod
    def matchOrdinalCentury(self, value):
        return

    @abc.abstractmethod
    def matchOrdinalToOrdinalCentury(self, value):
        return

    @abc.abstractmethod
    def matchOrdinalMillennium(self, value):
        return

    @abc.abstractmethod
    def matchOrdinalToOrdinalMillennium(self, value):
        return

    @abc.abstractmethod
    def matchYearWithPrefix(self, value):
        return

    @abc.abstractmethod
    def matchYearWithSuffix(self, value):
        return

    @abc.abstractmethod
    def matchYearToYear(self, value):
        return

    @abc.abstractmethod
    def matchLoneDecade(self, value):
        return

    @abc.abstractmethod
    def matchDecadeToDecade(self, value):
        return

    @abc.abstractmethod
    def matchNamedPeriod(self, value):
        return

    @abc.abstractmethod
    def matchNamedToNamedPeriod(self, value):
        return

    @abc.abstractmethod
    def matchLoneYear(self, value):
        return

    # ported from RxMatcher.cs 10/02/20 CFB
    def getCenturyYearSpan(self, centuryNo, datePrefix=None, dateSuffix=None):
        span = YearSpan()
        # adjust boundaries if E/M/L qualifier is present using
        # (invented) boundaries: EARLY=1-40, MID=30-70, LATE=60-100
        if dateSuffix == enums.DateSuffix.BC:
            span.minYear = centuryNo * -100
            if datePrefix == enums.DatePrefix.HALF1:
                span.maxYear = span.minYear + 50
            elif datePrefix == enums.DatePrefix.HALF2:
                span.minYear += 50
                span.maxYear = span.minYear + 49
            elif datePrefix == enums.DatePrefix.EARLY:
                span.maxYear = span.minYear + 40
            elif datePrefix == enums.DatePrefix.MID:
                span.minYear += 30
                span.maxYear = span.minYear + 40
            elif datePrefix == enums.DatePrefix.LATE:
                span.minYear += 60
                span.maxYear = span.minYear + 39
            elif datePrefix == enums.DatePrefix.THIRD1:
                span.maxYear = span.minYear + 33
            elif datePrefix == enums.DatePrefix.THIRD2:
                span.minYear += 33
                span.maxYear = span.minYear + 33
            elif datePrefix == enums.DatePrefix.THIRD3:
                span.minYear += 66
                span.maxYear = span.minYear + 33
            elif datePrefix == enums.DatePrefix.QUARTER1:
                span.maxYear = span.minYear + 25
            elif datePrefix == enums.DatePrefix.QUARTER2:
                span.minYear += 25
                span.maxYear = span.minYear + 25
            elif datePrefix == enums.DatePrefix.QUARTER3:
                span.minYear += 50
                span.maxYear = span.minYear + 25
            elif datePrefix == enums.DatePrefix.QUARTER4:
                span.minYear += 75
                span.maxYear = span.minYear + 24
            else:  # There is no year zero...
                span.maxYear = span.minYear + 99
        elif dateSuffix == enums.DateSuffix.BP:
            span.minYear = self.PRESENT - (centuryNo * 100) + 1
            if datePrefix == enums.DatePrefix.HALF1:
                span.maxYear = span.minYear + 50
            elif datePrefix == enums.DatePrefix.HALF2:
                span.minYear += 50
                span.maxYear = span.minYear + 49
            elif datePrefix == enums.DatePrefix.EARLY:
                span.maxYear = span.minYear + 40
            elif datePrefix == enums.DatePrefix.MID:
                span.minYear += 30
                span.maxYear = span.minYear + 40
            elif datePrefix == enums.DatePrefix.LATE:
                span.minYear += 60
                span.maxYear = span.minYear + 39
            elif datePrefix == enums.DatePrefix.THIRD1:
                span.maxYear = span.minYear + 33
            elif datePrefix == enums.DatePrefix.THIRD2:
                span.minYear += 33
                span.maxYear = span.minYear + 33
            elif datePrefix == enums.DatePrefix.THIRD3:
                span.minYear += 66
                span.maxYear = span.minYear + 33
            elif datePrefix == enums.DatePrefix.QUARTER1:
                span.maxYear = span.minYear + 25
            elif datePrefix == enums.DatePrefix.QUARTER2:
                span.minYear += 25
                span.maxYear = span.minYear + 25
            elif datePrefix == enums.DatePrefix.QUARTER3:
                span.minYear += 50
                span.maxYear = span.minYear + 25
            elif datePrefix == enums.DatePrefix.QUARTER4:
                span.minYear += 75
                span.maxYear = span.minYear + 24
            else:  # There is no year zero...
                span.maxYear = span.minYear + 99
        else:  # AD, CE or NONE
            span.minYear = (centuryNo * 100) - 99
            if datePrefix == enums.DatePrefix.HALF1:
                span.maxYear = span.minYear + 49
            elif datePrefix == enums.DatePrefix.HALF2:
                span.minYear += 49
                span.maxYear = span.minYear + 50
            elif datePrefix == enums.DatePrefix.EARLY:
                span.maxYear = span.minYear + 39
            elif datePrefix == enums.DatePrefix.MID:
                span.minYear += 29
                span.maxYear = span.minYear + 40
            elif datePrefix == enums.DatePrefix.LATE:
                span.minYear += 59
                span.maxYear = span.minYear + 40
            elif datePrefix == enums.DatePrefix.THIRD1:
                span.maxYear = span.minYear + 33
            elif datePrefix == enums.DatePrefix.THIRD2:
                span.minYear += 33
                span.maxYear = span.minYear + 33
            elif datePrefix == enums.DatePrefix.THIRD3:
                span.minYear += 66
                span.maxYear = span.minYear + 33
            elif datePrefix == enums.DatePrefix.QUARTER1:
                span.maxYear = span.minYear + 24
            elif datePrefix == enums.DatePrefix.QUARTER2:
                span.minYear += 24
                span.maxYear = span.minYear + 25
            elif datePrefix == enums.DatePrefix.QUARTER3:
                span.minYear += 49
                span.maxYear = span.minYear + 25
            elif datePrefix == enums.DatePrefix.QUARTER4:
                span.minYear += 74
                span.maxYear = span.minYear + 25
            else:
                span.maxYear = span.minYear + 99
        # TODO: not currently accounting for earlymid, or midlate
        return span

    # ported from RxMatcher.cs 10/02/20 CFB

    def getMillenniumYearSpan(self, millenniumNo, datePrefix=None, dateSuffix=None):
        span = YearSpan()

        # adjust boundaries if E/M/L qualifier is present using
        # (invented) boundaries: EARLY=1-40, MID=30-70, LATE=60-100
        if dateSuffix == enums.DateSuffix.BC:
            span.minYear = (millenniumNo * -1000)

            if datePrefix == enums.DatePrefix.HALF1:
                span.maxYear = span.minYear + 500
            elif datePrefix == enums.DatePrefix.HALF2:
                span.minYear += 500
                span.maxYear = span.minYear + 499
            elif datePrefix == enums.DatePrefix.EARLY:
                span.maxYear = span.minYear + 400
            elif datePrefix == enums.DatePrefix.MID:
                span.minYear += 300
                span.maxYear = span.minYear + 400
            elif datePrefix == enums.DatePrefix.LATE:
                span.minYear += 600
                span.maxYear = span.minYear + 399
            elif datePrefix == enums.DatePrefix.THIRD1:
                span.maxYear = span.minYear + 333
            elif datePrefix == enums.DatePrefix.THIRD2:
                span.minYear += 333
                span.maxYear = span.minYear + 333
            elif datePrefix == enums.DatePrefix.THIRD3:
                span.minYear += 666
                span.maxYear = span.minYear + 333
            elif datePrefix == enums.DatePrefix.QUARTER1:
                span.maxYear = span.minYear + 250
            elif datePrefix == enums.DatePrefix.QUARTER2:
                span.minYear += 250
                span.maxYear = span.minYear + 250
            elif datePrefix == enums.DatePrefix.QUARTER3:
                span.minYear += 500
                span.maxYear = span.minYear + 250
            elif datePrefix == enums.DatePrefix.QUARTER4:
                span.minYear += 750
                span.maxYear = span.minYear + 249
            else:  # There is no year zero...
                span.maxYear = span.minYear + 999
        elif dateSuffix == enums.DateSuffix.BP:
            span.minYear = self.PRESENT - (millenniumNo * 1000) + 1
            if datePrefix == enums.DatePrefix.HALF1:
                span.maxYear = span.minYear + 500
            elif datePrefix == enums.DatePrefix.HALF2:
                span.minYear += 500
                span.maxYear = span.minYear + 499
            elif datePrefix == enums.DatePrefix.EARLY:
                span.maxYear = span.minYear + 400
            elif datePrefix == enums.DatePrefix.MID:
                span.minYear += 300
                span.maxYear = span.minYear + 400
            elif datePrefix == enums.DatePrefix.LATE:
                span.minYear += 600
                span.maxYear = span.minYear + 399
            elif datePrefix == enums.DatePrefix.THIRD1:
                span.maxYear = span.minYear + 333
            elif datePrefix == enums.DatePrefix.THIRD2:
                span.minYear += 333
                span.maxYear = span.minYear + 333
            elif datePrefix == enums.DatePrefix.THIRD3:
                span.minYear += 666
                span.maxYear = span.minYear + 333
            elif datePrefix == enums.DatePrefix.QUARTER1:
                span.maxYear = span.minYear + 250
            elif datePrefix == enums.DatePrefix.QUARTER2:
                span.minYear += 250
                span.maxYear = span.minYear + 250
            elif datePrefix == enums.DatePrefix.QUARTER3:
                span.minYear += 500
                span.maxYear = span.minYear + 250
            elif datePrefix == enums.DatePrefix.QUARTER4:
                span.minYear += 750
                span.maxYear = span.minYear + 249
            else:  # There is no year zero...
                span.maxYear = span.minYear + 999
        else:  # AD, CE or NONE
            span.minYear = (millenniumNo * 1000) - 999
            if datePrefix == enums.DatePrefix.HALF1:
                span.maxYear = span.minYear + 499
            elif datePrefix == enums.DatePrefix.HALF2:
                span.minYear += 499
                span.maxYear = span.minYear + 500
            elif datePrefix == enums.DatePrefix.EARLY:
                span.maxYear = span.minYear + 399
            elif datePrefix == enums.DatePrefix.MID:
                span.minYear += 299
                span.maxYear = span.minYear + 400
            elif datePrefix == enums.DatePrefix.LATE:
                span.minYear += 599
                span.maxYear = span.minYear + 400
            elif datePrefix == enums.DatePrefix.THIRD1:
                span.maxYear = span.minYear + 333
            elif datePrefix == enums.DatePrefix.THIRD2:
                span.minYear += 333
                span.maxYear = span.minYear + 333
            elif datePrefix == enums.DatePrefix.THIRD3:
                span.minYear += 666
                span.maxYear = span.minYear + 333
            elif datePrefix == enums.DatePrefix.QUARTER1:
                span.maxYear = span.minYear + 249
            elif datePrefix == enums.DatePrefix.QUARTER2:
                span.minYear += 249
                span.maxYear = span.minYear + 250
            elif datePrefix == enums.DatePrefix.QUARTER3:
                span.minYear += 499
                span.maxYear = span.minYear + 250
            elif datePrefix == enums.DatePrefix.QUARTER4:
                span.minYear += 749
                span.maxYear = span.minYear + 250
            else:
                span.maxYear = span.minYear + 999
        # TODO: not currently accounting for intermediates - earlymid, or midlate
        return span
