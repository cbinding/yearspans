"""
=============================================================================
Project   : ARIADNEplus
Package   : yearspanmatcher
Module    : yearspan.py
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Summary   : YearSpan class
Imports   : N/A
Example   : span = YearSpan(43, 410, "Roman", True)
    NOTE: zeroIsBCE regards input year 0 as 1 BCE (there is no year 0)
License   : https://github.com/cbinding/yearspans/blob/main/LICENSE.md
=============================================================================
History
18/02/2020 CFB Initially created script
08/04/2024 CFB Type hints added, code tidying, added zeroIsBCE property
=============================================================================
"""
class YearSpan(object):

    def __init__(self, 
        minYear: int=None, 
        maxYear: int=None, 
        label: str=None, 
        zeroIsBCE: bool=True
    ) -> None:
        # init properties with values passed in
        self.minYear = None
        self.maxYear = None
        self.label = (label or "").strip()
        self.zeroIsBCE = zeroIsBCE

        # ensure minYear and maxYear values are set up correctly,
        # regardless of how they are passed in. If only one value 
        # is passed it is used for both minYear and maxYear value
        if (minYear is not None or maxYear is not None):
            values = list(filter(lambda x: x is not None, [minYear, maxYear]))
            self.minYear = min(values)
            self.maxYear = max(values)
 

    # calculate duration in years (including start and end year)
    def duration(self) -> int:
        return abs(self.maxYear or 0 - self.minYear or 0) + 1


    # string representation of this instance (e.g. "0043/0410 (Roman)")
    def __str__(self):
        return f"{self.toISO8601()} ({self.label})"


    def __repr__(self):
        return self.__str__()


    # ISO8601 string representation of this instance (e.g. "0043/0410")
    def toISO8601(self) -> str:
        return YearSpan.spanToISO8601(
            minYear=self.minYear, 
            maxYear=self.maxYear, 
            zeroIsBCE=self.zeroIsBCE
        )        


    # JSON representation of this instance
    def toJSON(self) -> dict:
        return {
            "label": self.label,
            "minYear": self.yearToISO8601(self.minYear, zeroIsBCE=self.zeroIsBCE),
            "maxYear": self.yearToISO8601(self.maxYear, zeroIsBCE=self.zeroIsBCE),
            "isoSpan": self.toISO8601()
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


    # ISO8601 string representation of zewro-padded year span (e.g. "-0055/0410")
    @staticmethod
    def spanToISO8601(minYear: int=None, maxYear: int=None, zeroIsBCE: bool=True) -> str:
        span = YearSpan(minYear, maxYear, zeroIsBCE=zeroIsBCE)
        
        return "{minValue}/{maxValue}".format(
            minValue=YearSpan.yearToISO8601(span.minYear, zeroIsBCE=zeroIsBCE),
            maxValue=YearSpan.yearToISO8601(span.maxYear, zeroIsBCE=zeroIsBCE)
        )


    # convert signed numeric value (as year) to ISO8601 compatible string value.
    # Returns a (signed) year padded with leading zeros if shorter than 4 digits,
    # optionally adjusting returned value to represent that there is no year zero
    # (so "0001" = 1 CE, "0000" = 1 BCE, "-0001" = 2 BCE, "-0002" = 3 BCE etc.)
    @staticmethod
    def yearToISO8601(year=None, minDigits:int=4, zeroIsBCE: bool=True) -> str:
        if year is not None:
            value = YearSpan._tryParseInt(year)
            if value < 0 and zeroIsBCE: value += 1
            sign = "-" if value < 0 else ""
            return f"{sign}{abs(value):0{minDigits}d}"
        else:
            return ""
