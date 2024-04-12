"""
=============================================================================
Project   : ARIADNEplus
Package   : yearspanmatcher
Module    : yearspanmatcher_it.py
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Summary   : YearSpan matcher (Italian)
Imports   : regex, enums, relib, yearspan
Example   :
License   : https://github.com/cbinding/yearspans/blob/main/LICENSE.md
=============================================================================
History
14/02/2020 CFB Initially created script
=============================================================================
"""
import regex
#from . import enums
#from .relib import maybe, oneof, group, zeroormore, oneormore, SPACEORDASH, NUMERICYEAR, patterns
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

class YearSpanMatcherIT(YearSpanMatcherEN):

    def __init__(self, present: int=2000, periodo_authority_id="p0qhb66") -> None:
        super(YearSpanMatcherEN, self).__init__(
            language="it", 
            periodo_authority_id=periodo_authority_id
        )
        self.MILLENNIUM = r"millennio"
        self.CENTURY = r"sec(\.|olo)"

    def matchLoneDecade(self, value: str) -> YearSpan:
        # e.g. "primi anni 1850"
        decade = 0

        pattern = r"\s*".join([
            maybe(oneof(self.DATEPREFIXES, "datePrefix")),
            "anni",
            group(r"[1-9]\d{1,2}0", "decade"),
            maybe(oneof(self.DATESUFFIXES, "dateSuffix"))
        ])
        match = regex.fullmatch(pattern, value, regex.IGNORECASE)
        if not match:
            return None
        if 'decade' in match.groupdict():
            decade = int(match.group('decade'))
        span = YearSpan(decade, decade + 9, value)
        return span

    def matchDecadeToDecade(self, value: str) -> YearSpan:
        # e.g. "inizio del 1850 alla fine del 1860"
        pattern = r"\s*".join([
            maybe(oneof(self.DATEPREFIXES, "datePrefix1")),
            group(r"\b[1-9]\d{1,2}0", "decade1"),
            oneof(self.DATESEPARATORS),
            maybe(oneof(self.DATEPREFIXES, "datePrefix2")),
            group(r"\b[1-9]\d{1,2}0", "decade2"),
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


if __name__ == "__main__":
    span = YearSpanMatcherIT().match("Inizio dell'XI secolo d.C.")
    print(span)