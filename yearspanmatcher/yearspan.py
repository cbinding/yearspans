"""
=============================================================================
Project   : ARIADNEplus
Package   : yearspanmatcher
Module    : yearspan.py
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Summary   : YearSpan class
Imports   : enums, util
Example   :
License   : https://creativecommons.org/licenses/by/4.0/ [CC BY 4.0]
=============================================================================
History
18/02/2020 CFB Initially created script
=============================================================================
"""
from . import enums
from . import util
        
class YearSpan(object):
    
    def __init__(self, minYear=None, maxYear=None, label=None):
        self.minYear = None
        self.maxYear = None
        self.label = ""

        if (minYear is not None or maxYear is not None):
            lst = [minYear, maxYear]
            self.minYear = min(filter(lambda x: x is not None, lst)) if any(lst) else None # min(i for i in l if i is not None)
            self.maxYear = max(filter(lambda x: x is not None, lst)) if any(lst) else None # max(i for i in l if i is not None)

        if(label):
            self.label = str(label).strip()


    # duration in years (includes start and end year)
    def duration(self):
        return abs(self.maxYear or 0 - self.minYear or 0) + 1

    def __str__(self):
        return f"{self.toISO8601span()} ({self.label})"
    
    def toISO8601span(self):
        return f"{self.toISO8601year(self.minYear)}/{self.toISO8601year(self.maxYear)}"

    # convert signed numeric value (as year) to ISO8601 compatible string
    # returns a (signed) fixed length value padded with leading zeros
    # optionally adjusting returned value as 0000=1 BC, -0001=2 BC, -0002=3 BC etc.
    @staticmethod
    def toISO8601year(value=None, minDigits=4, zeroIsBC=True):
        val = util.tryParseInt(value)
        if val is not None:
            if val <= 0 and zeroIsBC:
                val += 1       
            sign = "-" if val < 0 else ""
            return f"{sign}{abs(val):0{minDigits}d}"
        else:
            return ""
    