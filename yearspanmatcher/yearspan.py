"""
=============================================================================
Project   : ARIADNEplus
Package   : yearspanmatcher
Module    : yearspan.py
Classes   : YearSpan
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Summary   : YearSpan class
Imports   : Allen (enum)
Example   : span = YearSpan(43, 410, "Roman")
License   : https://github.com/cbinding/yearspans/blob/main/LICENSE.md
=============================================================================
History
18/02/2020 CFB Initially created script
09/04/2024 CFB Added type hints, zeroIsBCE, property getters and setters
=============================================================================
"""
from __future__ import annotations # to refer to YearSpan in static methods

if __package__ is None or __package__ == '':
    # uses current directory visibility
    from enums import Allen # for relationship between YearSpan instances
else:
    from .enums import Allen 


class YearSpan(object):

    def __init__(self, 
        minYear: int=None, 
        maxYear: int=None, 
        label: str=None, 
        zeroIsBCE: bool=True # regard year 0 as 1 BCE (there is no year 0)
    ) -> None:
        # init properties with values passed in
        self.minYear = minYear
        self.maxYear = maxYear
        self.label = label
        self.zeroIsBCE = zeroIsBCE

        # ensure minYear and maxYear values are ordered correctly,
        # regardless of how they were passed in. If only one value 
        # is passed it is used for both minYear and maxYear values
        if (minYear is not None or maxYear is not None):
            values = list(filter(lambda x: x is not None, [minYear, maxYear]))
            self.minYear = min(values)
            self.maxYear = max(values)
    

    # minYear property getter and setter
    @property
    def minYear(self) -> int: return self._minYear

    @minYear.setter
    def minYear(self, value: int):
        self._minYear = value


    # maxYear property getter and setter
    @property
    def maxYear(self) -> int: return self._maxYear

    @maxYear.setter
    def maxYear(self, value: int):
        self._maxYear = value


    # zeroIsBCE property getter and setter
    @property
    def zeroIsBCE(self) -> bool: return self._zeroIsBCE
    
    @zeroIsBCE.setter
    def zeroIsBCE(self, value: bool):
        self._zeroIsBCE = value


    # label property getter and setter
    @property
    def label(self) -> str:
        if(len(self._label or "")) == 0:
            return self.toISO8601()
        else:
            return self._label

    # returns sensible label if not set
    @label.setter
    def label(self, value: str):
        self._label = (value or "").strip()


    # calculate duration in whole years (including start and end year)
    def duration(self) -> int:
        return abs((self.maxYear or 0) - (self.minYear or 0)) + 1


    # string representation of this instance (e.g. "0043/0410 (Roman)")
    def __str__(self):
        return f"{self.toISO8601()} ({self.label})"


    def __repr__(self):
        return self.__str__()


    def __eq__(self, other: self.__class__):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False


    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))


    # ISO8601 string representation of this instance (e.g. "0043/0410")
    def toISO8601(self) -> str:
        return YearSpan.spanToISO8601(
            minYear=self.minYear, 
            maxYear=self.maxYear, 
            zeroIsBCE=self.zeroIsBCE
        )        


    # JSON representation of this instance (as python dict)
    def toJSON(self) -> dict:
        return {
            "label": self.label,
            "minYear": self.yearToISO8601(self.minYear, zeroIsBCE=self.zeroIsBCE),
            "maxYear": self.yearToISO8601(self.maxYear, zeroIsBCE=self.zeroIsBCE),
            "isoSpan": self.toISO8601(),
            "duration": self.duration()
        }


    # try to parse integer value without throwing error
    @staticmethod
    def _tryParseInt(value):
        val = None
        if value is not None:
            try:
                val = int(value)
            except ValueError:
                val = val
        return val


    # ISO8601 string representation of zero-padded year span (e.g. "-0055/0410")
    @staticmethod
    def spanToISO8601(minYear: int=None, maxYear: int=None, zeroIsBCE: bool=True) -> str:
        span = YearSpan(minYear=minYear, maxYear=maxYear, zeroIsBCE=zeroIsBCE)
        
        return "{minValue}/{maxValue}".format(
            minValue=YearSpan.yearToISO8601(span.minYear, zeroIsBCE=zeroIsBCE),
            maxValue=YearSpan.yearToISO8601(span.maxYear, zeroIsBCE=zeroIsBCE)
        )


    # convert signed numeric value (as year) to ISO8601 compatible string value.
    # Returns a (signed) year padded with leading zeros if shorter than 4 digits,
    # optionally adjusting returned value to represent that there is no year zero
    # (so 1 ="0001" = 1 CE, 0 = "-0001" = 1 BCE, -1 = "-0002" = 2 BCE etc.)
    @staticmethod
    def yearToISO8601(year=None, minDigits:int=4, zeroIsBCE: bool=True) -> str:
        if year is not None:
            value = YearSpan._tryParseInt(year)
            if value < 0 and zeroIsBCE: value += 1
            sign = "-" if value < 0 else ""
            return f"{sign}{abs(value):0{minDigits}d}"
        else:
            return ""

    
    # Allen relationships between YearSpan instances
    # is spanA before spanB?
    @staticmethod
    def spanBefore(spanA: YearSpan, spanB: YearSpan) -> bool: 	
        return (spanA.maxYear < spanB.minYear)

    # is spanA after spanB?
    @staticmethod
    def spanAfter(spanA: YearSpan, spanB: YearSpan) -> bool: 	
        return YearSpan.spanBefore(spanB, spanA)

    # does spanA meet spanB?
    @staticmethod
    def spanMeets(spanA: YearSpan, spanB: YearSpan) -> bool: 	
        return (spanA.maxYear == spanB.minYear)

    # is spanA met by spanB?
    @staticmethod
    def spanMetBy(spanA: YearSpan, spanB: YearSpan) -> bool: 	
        return YearSpan.spanMeets(spanB, spanA)

    # does spanA overlap spanB?
    @staticmethod
    def spanOverlaps(spanA: YearSpan, spanB: YearSpan) -> bool:
        return (spanA.minYear < spanB.minYear
            and spanA.maxYear > spanB.minYear
            and spanA.maxYear < spanB.maxYear)	

    # is spanA overlapped by spanB?
    @staticmethod
    def spanOverlappedBy(spanA: YearSpan, spanB: YearSpan) -> bool: 	
        return YearSpan.spanOverlaps(spanB, spanA)

    # does spanA start spanB?
    @staticmethod
    def spanStarts(spanA: YearSpan, spanB: YearSpan) -> bool: 	
        return (spanA.minYear == spanB.minYear 
            and spanA.maxYear < spanB.maxYear)

    # is spanA started by spanB?
    @staticmethod
    def spanStartedBy(spanA: YearSpan, spanB: YearSpan) -> bool: 	
        return YearSpan.spanStarts(spanB, spanA)  

    # does spanA finish spanB?
    @staticmethod
    def spanFinishes(spanA: YearSpan, spanB: YearSpan) -> bool: 	
        return (spanA.maxYear == spanB.maxYear 
		    and spanA.minYear > spanB.minYear)

    # is spanA finished by spanB?
    @staticmethod
    def spanFinishedBy(spanA: YearSpan, spanB: YearSpan) -> bool: 	
        return YearSpan.spanFinishes(spanB, spanA) 

    # is spanA within spanB?
    @staticmethod
    def spanWithin(spanA: YearSpan, spanB: YearSpan) -> bool: 	  
        return (spanA.minYear > spanB.minYear 
			and spanA.maxYear < spanB.maxYear)

    # does spanA contain spanB?
    @staticmethod
    def spanContains(spanA: YearSpan, spanB: YearSpan) -> bool: 	
        return YearSpan.spanWithin(spanB, spanA)

    # is spanA equal to spanB?
    @staticmethod
    def spanEquals(spanA: YearSpan, spanB: YearSpan) -> bool: 	
        return (spanA.minYear == spanB.minYear 
			and spanA.maxYear == spanB.maxYear)

    # get Allen relationship between 2 YearSpan instances
    @staticmethod
    def spanRelationship(spanA: YearSpan, spanB: YearSpan) -> Allen: 	
        rel = None
        
        if (YearSpan.spanBefore(spanA, spanB)): 
            rel = Allen.BEFORE
        elif (YearSpan.spanAfter(spanA, spanB)): 
            rel = Allen.AFTER
        elif (YearSpan.spanMeets(spanA, spanB)):
            rel = Allen.MEETS
        elif (YearSpan.spanMetBy(spanA, spanB)):
            rel = Allen.METBY
        elif (YearSpan.spanOverlaps(spanA, spanB)): 
            rel = Allen.OVERLAPS
        elif (YearSpan.spanOverlappedBy(spanA, spanB)): 
            rel = Allen.OVERLAPPEDBY
        elif (YearSpan.spanStarts(spanA, spanB)): 
            rel = Allen.STARTS
        elif (YearSpan.spanStartedBy(spanA, spanB)): 
            rel = Allen.STARTEDBY
        elif (YearSpan.spanFinishes(spanA, spanB)): 
            rel = Allen.FINISHES
        elif (YearSpan.spanFinishedBy(spanA, spanB)): 
            rel = Allen.FINISHEDBY
        elif (YearSpan.spanWithin(spanA, spanB)): 
            rel = Allen.WITHIN
        elif (YearSpan.spanContains(spanA, spanB)): 
            rel = Allen.CONTAINS
        elif (YearSpan.spanEquals(spanA, spanB)): 
            rel = Allen.EQUALS
        return rel

if __name__ == "__main__":
    span = YearSpan(-50,48,"test period")
    print(span)