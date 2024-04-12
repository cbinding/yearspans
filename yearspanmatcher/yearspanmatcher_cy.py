"""
=============================================================================
Project   : ARIADNEplus
Package   : yearspanmatcher
Module    : yearspanmatcher_cy.py
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Summary   : YearSpanMatcherCY (Welsh)
Imports   : regex, enums, relib, yearspan, YearSpanMatcherEN
Example   : 
License   : https://github.com/cbinding/yearspans/blob/main/LICENSE.md
=============================================================================
History
14/02/2020 CFB Initially created script
=============================================================================
"""
import regex
#from . import enums
#from .relib import maybe, oneof, oneof, group, zeroormore, oneormore, SPACEORDASH, NUMERICYEAR, patterns
#from .yearspan import YearSpan
#from .yearspanmatcher_en import YearSpanMatcherEN

if __package__ is None or __package__ == '':
    # uses current directory visibility
    import enums
    from relib import maybe, oneof, group, zeroormore, oneormore, SPACEORDASH, NUMERICYEAR  
    from yearspan import YearSpan
    from yearspanmatcher_en import YearSpanMatcherEN
else:  
    from . import enums 
    from .yearspan import YearSpan    
    from .relib import maybe, oneof, group, zeroormore, oneormore, SPACEORDASH, NUMERICYEAR
    from .yearspanmatcher_en import YearSpanMatcherEN


class YearSpanMatcherCY(YearSpanMatcherEN):

    def __init__(self, present: int=2000, periodo_authority_id: str="") -> None:
        super(YearSpanMatcherEN, self).__init__(
            language="cy", 
            periodo_authority_id=periodo_authority_id
        )
        self.CENTURY = "ganrif"
        self.MILLENNIUM = "mileniwm"

    def matchLoneDecade(self, value: str) -> YearSpan:
        # e.g. "1950au"
        #datePrefix = None
        #dateSuffix = None
        decade = 0

        pattern = r"\s*".join([
            maybe(oneof(self.DATEPREFIXES, "datePrefix")),
            group(r"\b[1-9]\d{1,2}0", "decade") + "au",
            maybe(oneof(self.DATESUFFIXES, "dateSuffix"))
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
        # e.g. "1950au i 1960au"
        pattern = r"\s*".join([
            maybe(oneof(self.DATEPREFIXES, "datePrefix")),
            group(r"\b[1-9]\d{1,2}0", "decade1") + "au",
            oneof(self.DATESEPARATORS),
            group(r"\b[1-9]\d{1,2}0", "decade2") + "au",
            maybe(oneof(self.DATESUFFIXES, "dateSuffix"))
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

    def matchOrdinalMillennium(self, value: str) -> YearSpan:
        # e.g. "diwedd y mileniwm cyntaf OC"
        prefixEnum = None
        suffixEnum = None
        millenniumNo = 0

        pattern = r"\s*".join([
            maybe(oneof(self.DATEPREFIXES, "datePrefix")),
            self.MILLENNIUM,
            oneof(self.ORDINALS, "ordinal"),
            maybe(oneof(self.DATESUFFIXES, "dateSuffix"))
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

if __name__ == "__main__":
    span = YearSpanMatcherCY().match("dechrau'r 11eg ganrif OC")
    print(span)

