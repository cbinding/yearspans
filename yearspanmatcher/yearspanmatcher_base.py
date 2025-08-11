"""
=============================================================================
Project   : ARIADNEplus
Package   : yearspanmatcher
Module    : yearspanmatcher_base.py
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Summary   : YearSpanMatcherBase - abstract class for concrete language specific
Imports   : abc, enums, relib, yearspan
Example   :
License   : https://github.com/cbinding/yearspans/blob/main/LICENSE.md
=============================================================================
History
14/02/2020 CFB Initially created script
12/04/2024 CFB Added Perio.do support
=============================================================================
"""
import abc           # for Abstract Base Classes

from .PeriodoData import PeriodoData
from . import enums
from .yearspan import YearSpan
from . import relib


class YearSpanMatcherBase(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, language: str="en", present: int=2000, periodo_authority_id: str="") -> None:

        self.language = language.strip().lower()  # default language overridden in concrete classes
        # for use in calculating BP dates; may be overridden (sometimes BP refers to 1950)
        self.present = present
        self.periodo_authority_id = (periodo_authority_id or "").strip()

        # 12/08/2024 override to use period names from Perio.do data instead
        if(self.periodo_authority_id != ""):
            pd = PeriodoData()
            # list from Perio.do [{id, uri, label, language, minYear, maxYear}]
            periods_from_periodo = pd.get_period_list(self.periodo_authority_id) 
            # filter to specified language 
            #lex = f"http://lexvo.org/id/iso639-1/{self.language}"
            periods_for_language = list(filter(lambda p: p.get("language", "") == self.language, periods_from_periodo))
            # convert to [{id, value, pattern}, {id, value, pattern}]   
            # Note: perio.do year values already account for zeroIsBCE, 
            # so here we don't want to make any additional adjustments      
            relib.patterns[self.language]["periods"] = list(map(lambda p: {
                    "id": p.get("uri", p.get("id", "")),
                    "value": YearSpan(minYear=p.get("minYear", None), maxYear=p.get("maxYear", None), zeroIsBCE=False),
                    "pattern": p.get("label", "") 
                }, periods_for_language))            
            #print(periods_for_language[0:5])

        def get_pattern(item) -> str: return item.get("pattern", "") 

        # ["EARLY", "MID", "LATE", "etc."]        
        self.DATEPREFIXES = list(map(get_pattern, relib.patterns_for_key("dateprefix", self.language)))
        # ["AD", "BC", "BP", "etc."]
        self.DATESUFFIXES = list(map(get_pattern, relib.patterns_for_key("datesuffix", self.language)))
        # ["to", "-", "and", "etc."]
        self.DATESEPARATORS = list(map(get_pattern, relib.patterns_for_key("dateseparator", self.language)))
        # ["Monday", "Tuesday", "etc."]
        self.DAYNAMES = list(map(get_pattern, relib.patterns_for_key("daynames", self.language)))
        # ["January", "February", "etc."]
        self.MONTHNAMES = list(map(get_pattern, relib.patterns_for_key("monthnames", self.language)))
        # ["Spring", "Summer", "etc."]
        self.SEASONNAMES = list(map(get_pattern, relib.patterns_for_key("seasonnames", self.language)))
        # ["one", "two", "three", "etc."]
        self.CARDINALS = list(map(get_pattern, relib.patterns_for_key("cardinals", self.language)))
        # ["first", "second", "third", "etc."]
        self.ORDINALS = list(map(get_pattern, relib.patterns_for_key("ordinals", self.language)))
        # ["Elizabethan", "Victorian", "etc."]
        self.PERIODNAMES = list(map(get_pattern, relib.patterns_for_key("periods", self.language)))
    
    
    def getDayNameEnum(self, s: str) -> enums.Day | None:
        return relib.getDayNameEnum(s, self.language)
        

    def getMonthNameEnum(self, s: str) -> enums.Month | None:
        return relib.getMonthNameEnum(s, self.language)
       

    def getSeasonNameEnum(self, s: str) -> enums.Season | None:
        return relib.getSeasonNameEnum(s, self.language)
        

    #def getCardinalValue(self, s: str) -> int:
        #return relib.getCardinalValue(s, self.language)
        

    def getOrdinalValue(self, s: str) -> int | None:
        return relib.getOrdinalValue(s, self.language)
        

    def getDatePrefixEnum(self, s: str) -> enums.DatePrefix | None:
        return relib.getDatePrefixEnum(s, self.language)
        

    def getDateSuffixEnum(self, s: str) -> enums.DateSuffix | None:
        return relib.getDateSuffixEnum(s, self.language)
        

    def getNamedPeriodValue(self, s: str) -> YearSpan | None:
        return relib.getNamedPeriodValue(s, self.language)

            
    def match(self, value: str) -> YearSpan | None:
        cleanValue = (value or "").strip()

        # try named periods first, if no match then try other patterns
        span = self.matchNamedPeriod(cleanValue)
        if span is None:
            span = self.matchNamedToNamedPeriod(cleanValue)
        if span is None:
            span = self.matchMonthYear(cleanValue)
        if span is None:
            span = self.matchSeasonYear(cleanValue)
        if span is None:
            span = self.matchCardinalCentury(cleanValue)
        if span is None:
            span = self.matchOrdinalCentury(cleanValue)
        if span is None:
            span = self.matchCardinalToCardinalCentury(cleanValue)
        if span is None:
            span = self.matchOrdinalToOrdinalCentury(cleanValue)
        if span is None:
            span = self.matchOrdinalMillennium(cleanValue)
        if span is None:
            span = self.matchOrdinalToOrdinalMillennium(cleanValue)
        if span is None:
            span = self.matchYearWithPrefix(cleanValue)
        if span is None:
            span = self.matchYearWithSuffix(cleanValue)
        if span is None:
            span = self.matchYearWithTolerance1(cleanValue)
        if span is None:
            span = self.matchYearWithTolerance2(cleanValue)
        if span is None:
            span = self.matchYearToYear2(cleanValue)
        if span is None:
            span = self.matchYearToYear(cleanValue)
        if span is None:
            span = self.matchLoneDecade(cleanValue)
        if span is None:
            span = self.matchDecadeToDecade(cleanValue)
        if span is None:
            span = self.matchLoneYear(cleanValue)
        if span is not None:
            span.label = cleanValue
        return span


    @abc.abstractmethod
    def matchMonthYear(self, value: str) -> YearSpan | None:
        return None


    @abc.abstractmethod
    def matchSeasonYear(self, value: str) -> YearSpan | None:
        return None


    @abc.abstractmethod
    def matchOrdinalCentury(self, value: str) -> YearSpan | None:
        return None


    @abc.abstractmethod
    def matchOrdinalToOrdinalCentury(self, value: str) -> YearSpan | None:
        return None


    @abc.abstractmethod
    def matchCardinalCentury(self, value: str) -> YearSpan | None:
        return None
    

    @abc.abstractmethod
    def matchCardinalToCardinalCentury(self, value: str) -> YearSpan | None:
        return None


    @abc.abstractmethod
    def matchOrdinalMillennium(self, value: str) -> YearSpan | None:
        return None


    @abc.abstractmethod
    def matchOrdinalToOrdinalMillennium(self, value: str) -> YearSpan | None:
        return None


    @abc.abstractmethod
    def matchYearWithPrefix(self, value: str) -> YearSpan | None:
        return None


    @abc.abstractmethod
    def matchYearWithSuffix(self, value: str) -> YearSpan | None:
        return None


    @abc.abstractmethod
    def matchYearWithTolerance1(self, value: str) -> YearSpan | None:
        return None
    

    @abc.abstractmethod
    def matchYearWithTolerance2(self, value: str) -> YearSpan | None:
        return None


    @abc.abstractmethod
    def matchYearToYear(self, value: str) -> YearSpan | None:
        return None


    @abc.abstractmethod
    def matchYearToYear2(self, value: str) -> YearSpan | None:
        return None


    @abc.abstractmethod
    def matchLoneDecade(self, value: str) -> YearSpan | None:
        return None


    @abc.abstractmethod
    def matchDecadeToDecade(self, value: str) -> YearSpan | None:
        return None


    @abc.abstractmethod
    def matchNamedPeriod(self, value: str) -> YearSpan | None:
        return None


    @abc.abstractmethod
    def matchNamedToNamedPeriod(self, value: str) -> YearSpan | None:
        return None


    @abc.abstractmethod
    def matchLoneYear(self, value: str) -> YearSpan | None:
        return None


    # ported from RxMatcher.cs 10/02/20 CFB
    def getCenturyYearSpan(self, centuryNo: int, datePrefix=None, dateSuffix=None) -> YearSpan:
        minYear = 0
        maxYear = 0

        # adjust boundaries if E/M/L qualifier is present using
        # (invented) boundaries: EARLY=1-40, MID=30-70, LATE=60-100
        if dateSuffix == enums.DateSuffix.BCE:
            minYear = centuryNo * -100
            if datePrefix == enums.DatePrefix.HALF1:
                maxYear = minYear + 50
            elif datePrefix == enums.DatePrefix.HALF2:
                minYear += 50
                maxYear = minYear + 49
            elif datePrefix == enums.DatePrefix.EARLY:
                maxYear = minYear + 40
            elif datePrefix == enums.DatePrefix.MID:
                minYear += 30
                maxYear = minYear + 40
            elif datePrefix == enums.DatePrefix.LATE:
                minYear += 60
                maxYear = minYear + 39
            elif datePrefix == enums.DatePrefix.THIRD1:
                maxYear = minYear + 33
            elif datePrefix == enums.DatePrefix.THIRD2:
                minYear += 33
                maxYear = minYear + 33
            elif datePrefix == enums.DatePrefix.THIRD3:
                minYear += 66
                maxYear = minYear + 33
            elif datePrefix == enums.DatePrefix.QUARTER1:
                maxYear = minYear + 25
            elif datePrefix == enums.DatePrefix.QUARTER2:
                minYear += 25
                maxYear = minYear + 25
            elif datePrefix == enums.DatePrefix.QUARTER3:
                minYear += 50
                maxYear = minYear + 25
            elif datePrefix == enums.DatePrefix.QUARTER4:
                minYear += 75
                maxYear = minYear + 24
            else:  # There is no year zero...
                maxYear = minYear + 99
        elif dateSuffix == enums.DateSuffix.BP:
            minYear = self.present - (centuryNo * 100) + 1
            if datePrefix == enums.DatePrefix.HALF1:
                maxYear = minYear + 50
            elif datePrefix == enums.DatePrefix.HALF2:
                minYear += 50
                maxYear = minYear + 49
            elif datePrefix == enums.DatePrefix.EARLY:
                maxYear = minYear + 40
            elif datePrefix == enums.DatePrefix.MID:
                minYear += 30
                maxYear = minYear + 40
            elif datePrefix == enums.DatePrefix.LATE:
                minYear += 60
                maxYear = minYear + 39
            elif datePrefix == enums.DatePrefix.THIRD1:
                maxYear = minYear + 33
            elif datePrefix == enums.DatePrefix.THIRD2:
                minYear += 33
                maxYear = minYear + 33
            elif datePrefix == enums.DatePrefix.THIRD3:
                minYear += 66
                maxYear = minYear + 33
            elif datePrefix == enums.DatePrefix.QUARTER1:
                maxYear = minYear + 25
            elif datePrefix == enums.DatePrefix.QUARTER2:
                minYear += 25
                maxYear = minYear + 25
            elif datePrefix == enums.DatePrefix.QUARTER3:
                minYear += 50
                maxYear = minYear + 25
            elif datePrefix == enums.DatePrefix.QUARTER4:
                minYear += 75
                maxYear = minYear + 24
            else:  # There is no year zero...
                maxYear = minYear + 99
        else:  # AD, CE or NONE
            minYear = (centuryNo * 100) - 99
            if datePrefix == enums.DatePrefix.HALF1:
                maxYear = minYear + 49
            elif datePrefix == enums.DatePrefix.HALF2:
                minYear += 49
                maxYear = minYear + 50
            elif datePrefix == enums.DatePrefix.EARLY:
                maxYear = minYear + 39
            elif datePrefix == enums.DatePrefix.MID:
                minYear += 29
                maxYear = minYear + 40
            elif datePrefix == enums.DatePrefix.LATE:
                minYear += 59
                maxYear = minYear + 40
            elif datePrefix == enums.DatePrefix.THIRD1:
                maxYear = minYear + 33
            elif datePrefix == enums.DatePrefix.THIRD2:
                minYear += 33
                maxYear = minYear + 33
            elif datePrefix == enums.DatePrefix.THIRD3:
                minYear += 66
                maxYear = minYear + 33
            elif datePrefix == enums.DatePrefix.QUARTER1:
                maxYear = minYear + 24
            elif datePrefix == enums.DatePrefix.QUARTER2:
                minYear += 24
                maxYear = minYear + 25
            elif datePrefix == enums.DatePrefix.QUARTER3:
                minYear += 49
                maxYear = minYear + 25
            elif datePrefix == enums.DatePrefix.QUARTER4:
                minYear += 74
                maxYear = minYear + 25
            else:
                maxYear = minYear + 99
        # TODO: not currently accounting for earlymid, or midlate

        return YearSpan(minYear, maxYear)


    # ported from RxMatcher.cs 10/02/20 CFB

    def getMillenniumYearSpan(self, millenniumNo: int, datePrefix=None, dateSuffix=None) -> YearSpan:
        minYear = 0
        #maxYear = 0
        
        # adjust boundaries if E/M/L qualifier is present using
        # (invented) boundaries: EARLY=1-40, MID=30-70, LATE=60-100
        if dateSuffix == enums.DateSuffix.BCE:
            minYear = (millenniumNo * -1000)

            if datePrefix == enums.DatePrefix.HALF1:
                maxYear = minYear + 500
            elif datePrefix == enums.DatePrefix.HALF2:
                minYear += 500
                maxYear = minYear + 499
            elif datePrefix == enums.DatePrefix.EARLY:
                maxYear = minYear + 400
            elif datePrefix == enums.DatePrefix.MID:
                minYear += 300
                maxYear = minYear + 400
            elif datePrefix == enums.DatePrefix.LATE:
                minYear += 600
                maxYear = minYear + 399
            elif datePrefix == enums.DatePrefix.THIRD1:
                maxYear = minYear + 333
            elif datePrefix == enums.DatePrefix.THIRD2:
                minYear += 333
                maxYear = minYear + 333
            elif datePrefix == enums.DatePrefix.THIRD3:
                minYear += 666
                maxYear = minYear + 333
            elif datePrefix == enums.DatePrefix.QUARTER1:
                maxYear = minYear + 250
            elif datePrefix == enums.DatePrefix.QUARTER2:
                minYear += 250
                maxYear = minYear + 250
            elif datePrefix == enums.DatePrefix.QUARTER3:
                minYear += 500
                maxYear = minYear + 250
            elif datePrefix == enums.DatePrefix.QUARTER4:
                minYear += 750
                maxYear = minYear + 249
            else:  # There is no year zero...
                maxYear = minYear + 999
        elif dateSuffix == enums.DateSuffix.BP:
            minYear = self.present - (millenniumNo * 1000) + 1
            if datePrefix == enums.DatePrefix.HALF1:
                maxYear = minYear + 500
            elif datePrefix == enums.DatePrefix.HALF2:
                minYear += 500
                maxYear = minYear + 499
            elif datePrefix == enums.DatePrefix.EARLY:
                maxYear = minYear + 400
            elif datePrefix == enums.DatePrefix.MID:
                minYear += 300
                maxYear = minYear + 400
            elif datePrefix == enums.DatePrefix.LATE:
                minYear += 600
                maxYear = minYear + 399
            elif datePrefix == enums.DatePrefix.THIRD1:
                maxYear = minYear + 333
            elif datePrefix == enums.DatePrefix.THIRD2:
                minYear += 333
                maxYear = minYear + 333
            elif datePrefix == enums.DatePrefix.THIRD3:
                minYear += 666
                maxYear = minYear + 333
            elif datePrefix == enums.DatePrefix.QUARTER1:
                maxYear = minYear + 250
            elif datePrefix == enums.DatePrefix.QUARTER2:
                minYear += 250
                maxYear = minYear + 250
            elif datePrefix == enums.DatePrefix.QUARTER3:
                minYear += 500
                maxYear = minYear + 250
            elif datePrefix == enums.DatePrefix.QUARTER4:
                minYear += 750
                maxYear = minYear + 249
            else:  # There is no year zero...
                maxYear = minYear + 999
        else:  # AD, CE or NONE
            minYear = (millenniumNo * 1000) - 999
            if datePrefix == enums.DatePrefix.HALF1:
                maxYear = minYear + 499
            elif datePrefix == enums.DatePrefix.HALF2:
                minYear += 499
                maxYear = minYear + 500
            elif datePrefix == enums.DatePrefix.EARLY:
                maxYear = minYear + 399
            elif datePrefix == enums.DatePrefix.MID:
                minYear += 299
                maxYear = minYear + 400
            elif datePrefix == enums.DatePrefix.LATE:
                minYear += 599
                maxYear = minYear + 400
            elif datePrefix == enums.DatePrefix.THIRD1:
                maxYear = minYear + 333
            elif datePrefix == enums.DatePrefix.THIRD2:
                minYear += 333
                maxYear = minYear + 333
            elif datePrefix == enums.DatePrefix.THIRD3:
                minYear += 666
                maxYear = minYear + 333
            elif datePrefix == enums.DatePrefix.QUARTER1:
                maxYear = minYear + 249
            elif datePrefix == enums.DatePrefix.QUARTER2:
                minYear += 249
                maxYear = minYear + 250
            elif datePrefix == enums.DatePrefix.QUARTER3:
                minYear += 499
                maxYear = minYear + 250
            elif datePrefix == enums.DatePrefix.QUARTER4:
                minYear += 749
                maxYear = minYear + 250
            else:
                maxYear = minYear + 999
        # TODO: not currently accounting for intermediates e.g. earlymid, or midlate
        return YearSpan(minYear, maxYear)
