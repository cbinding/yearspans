"""
=============================================================================
Project   : ARIADNEplus
Package   : yearspanmatcher
Module    : yearspan.py
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Summary   : YearSpan class
Imports   : N/A
Example   : span = YearSpan(43, 410, "Roman")
License   : https://github.com/cbinding/yearspans/blob/main/LICENSE.md
=============================================================================
History
18/02/2020 CFB Initially created script
=============================================================================
"""


class YearSpan(object):

    def __init__(self, minYear=None, maxYear=None, label=None):
        self.minYear = None
        self.maxYear = None
        self.label = ""

        if (minYear is not None or maxYear is not None):
            lst = [minYear, maxYear]
            self.minYear = min(filter(lambda x: x is not None, lst)) if any(
                lst) else None  # min(i for i in l if i is not None)
            self.maxYear = max(filter(lambda x: x is not None, lst)) if any(
                lst) else None  # max(i for i in l if i is not None)

        if (label):
            self.label = str(label).strip()

    # calculate duration in years (including start and end year)
    def duration(self):
        return abs(self.maxYear or 0 - self.minYear or 0) + 1

    # string representation of this instance (e.g. "0043/0410 (Roman)")
    def __str__(self):
        return f"{self.toISO8601()} ({self.label})"

    # ISO8601 string representation of this span (e.g. "0043/0410")
    def toISO8601(self):
        return f"{self.yearToISO8601(self.minYear)}/{self.yearToISO8601(self.maxYear)}"

    # JSON representation of this instance
    def toJSON(self):
        return {
            "label": self.label,
            "minYear": self.yearToISO8601(self.minYear),
            "maxYear": self.yearToISO8601(self.maxYear),
            "isoSpan": self.toISO8601()
        }

    # try to parse integer value without error
    @staticmethod
    def _tryParseInt(value):
        val = None
        if value is not None:
            try:
                val = int(value)  # , True
            except ValueError:
                val = val  # value #, False
        return val

    # ISO8601 string representation of given year span (e.g. "0043/0410")
    @staticmethod
    def spanToISO8601(minYear, maxYear) -> str:
        return f"{YearSpan.yearToISO8601(minYear)}/{YearSpan.yearToISO8601(maxYear)}"

    # convert signed numeric value (as year) to ISO8601 compatible string
    # returns a (signed) fixed length value padded with leading zeros
    # optionally adjusting returned value as 0000=1 BC, -0001=2 BC, -0002=3 BC etc.
    @staticmethod
    def yearToISO8601(value=None, minDigits=4, zeroIsBC=True) -> str:
        val = YearSpan._tryParseInt(value)
        if val is not None:
            if val <= 0 and zeroIsBC:
                val += 1
            sign = "-" if val < 0 else ""
            return f"{sign}{abs(val):0{minDigits}d}"
        else:
            return ""
