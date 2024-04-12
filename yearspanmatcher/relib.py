"""
=============================================================================
Project   : ARIADNEplus
Package   : yearspanmatcher
Module    : relib.py
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Summary   :
Regular expression patterns used for identifying date spans/periods within text
Uses 'regex' lib rather than 're' to support unicode categories (e.g. \p{Pd})
Imports   : regex, defaultdict, enums, YearSpan
Example   :
License   : https://github.com/cbinding/yearspans/blob/main/LICENSE.md
=============================================================================
History
22/01/2020 CFB Initially created script (ported from Javascript prototype)
05/04/2024 CFB Added type hints to function signatures
=============================================================================
"""
from collections import defaultdict # for patterns lists
import regex

if __package__ is None or __package__ == '':
    # uses current directory visibility
    from yearspan import YearSpan
    import enums  
else:
    from .yearspan import YearSpan
    from . import enums

# common regex patterns as constant strings
START = r"^"
SPACE = r"\s"
DIGIT = r"\d"
ANY = r"."
END = r"$"
NUMERICYEAR = r"[+-]?[1-9]\d{0,2}(?:\d|[\s,](?:\d{3}))*"
# note unicode property \p{Pd} covers all variants of hyphen/dash
# see https://www.fileformat.info/info/unicode/category/Pd/list.htm
DASH = r"\p{Pd}"
SPACEORDASH = r"(?:\s|\p{Pd})"
ROMAN = r"[MCDLXVI]+"

# functions for constructing regex groups
# returns: '(?:value)' or '(?P<name>value)'
def group(value: str, name: str=None, repeater: str=None) -> str:
    clean_name = (name or "").strip()
    clean_val = (value or "").strip()    
    clean_rep = (repeater or "").strip()

    if len(clean_name) > 0:
        return f"(?P<{clean_name}>{clean_val}){clean_rep}"
    else:
        return f"(?:{clean_val}){clean_rep}"

# returns True | False
def isgrouped(value: str) -> bool:
    clean_val = (value or "").strip()
    return (clean_val.startswith("(") and clean_val.endswith(")"))

# returns: '(?:value)?' or '(?P<name>value)?'
def maybe(value: str, name: str=None) -> str:
    return group(value, name, "?")

# returns: '(?:value)*' or '(?P<name>value)*'
def zeroormore(value: str, name: str=None) -> str:
    return group(value, name, "*")

# returns: '(?:value)+' or '(?P<name>value)+'
def oneormore(value: str, name: str=None) -> str:
    return group(value, name, "+")

# returns: '(?:value){n}' or '(?P<name>value){n}'
def exactly(value: str, name: str=None, n: int=1) -> str:
    return group(value, name, f"{{{n}}}")

# returns: '(?:value){n,m}' or '(?P<name>value){n,m}'
def range(value: str, name: str=None, n: int=None, m: int=None) -> str:
    return group(value, name, f"{{{n or ''},{m or ''}}}")

# Regular expression value options group e.g. where values = [value1, value2, value3]
# returns: '(?:value1|value2|value3)' or '(?P<name>value1|value2|value3)'
def oneof(values: list=[], name: str=None, repeater: str=None) -> str:
    clean_values = list(map(lambda value: (value or "").strip(), values))
    choices = '|'.join(clean_values)
    return group(choices, name, repeater)


# Get value property by matching s to item pattern
# from patterns array: [{ value: "", pattern:"" }]
# @staticmethod
def getValue(s: str, patts: list=[]):
    if not s:
        return None
    for item in patts:
        match = regex.fullmatch(item.get("pattern", ""), s, regex.IGNORECASE)
        if match:
            return item.get("value", None)
    return None


def patterns_for_key(key: str="", language: str="en") -> list:
    patterns_for_language = patterns.get(language.strip().lower(), "")
    return patterns_for_language.get(key.strip(), "")


def getDayNameEnum(s: str, language: str) -> enums.Day:
     return getValue(s, patterns_for_key("daynames", language))


def getMonthNameEnum(s: str, language: str) -> enums.Month:
    return getValue(s, patterns_for_key("monthnames", language))


def getSeasonNameEnum(s: str, language: str) -> enums.Season:
    return getValue(s, patterns_for_key("seasonnames", language))


def getOrdinalValue(s: str, language: str) -> int:
    return getValue(s, patterns_for_key("ordinals", language))


def getDatePrefixEnum(s: str, language: str) -> enums.DatePrefix:
    return getValue(s, patterns_for_key("dateprefix", language))


def getDateSuffixEnum(s: str, language: str) -> enums.DateSuffix:
    return getValue(s, patterns_for_key("datesuffix", language))


def getNamedPeriodValue(s: str, language: str) -> YearSpan:
    return getValue(s, patterns_for_key("periods", language))


# reusable multilingual regular expression pattern library
# defaultdict creates keys if they don't exist when first accessed
patterns = defaultdict(dict)

# new (29/01/24) Czech language patterns
patterns["cs"]["ordinals"] = [
    {"value": 1, "pattern": r"(?:1\.|první)"},                          # first
    {"value": 2, "pattern": r"(?:2\.|druh(?:ý|ého))"},                  # second
    {"value": 3, "pattern": r"(?:3\.|třetí)"},                          # third
    {"value": 4, "pattern": r"(?:4\.|čtvrt(?:ý|ého))"},                 # fourth
    {"value": 5, "pattern": r"(?:5\.|pát(?:ý|ého))"},                   # fifth
    {"value": 6, "pattern": r"(?:6\.|šest(?:ý|ého))"},                  # sixth
    {"value": 7, "pattern": r"(?:7\.|sedm(?:ý|ého))"},                  # seventh
    {"value": 8, "pattern": r"(?:8\.|osm(?:ý|ého))"},                   # eighth
    {"value": 9, "pattern": r"(?:9\.|devát(?:ý|ého))"},                 # ninth
    {"value": 10, "pattern": r"(?:10\.|desát(?:ý|ého))"},               # tenth
    {"value": 11, "pattern": r"(?:11\.|jedenáct(?:ý|ého))"},            # eleventh
    {"value": 12, "pattern": r"(?:12\.|dvanáct(?:ý|ého))"},             # twelfth
    {"value": 13, "pattern": r"(?:13\.|třináct(?:ý|ého))"},             # thirteenth
    {"value": 14, "pattern": r"(?:14\.|čtrnáct(?:ý|ého))"},             # fourteenth
    {"value": 15, "pattern": r"(?:15\.|patnáct(?:ý|ého))"},             # fifteenth
    {"value": 16, "pattern": r"(?:16\.|šestnáct(?:ý|ého))"},            # sixteenth
    {"value": 17, "pattern": r"(?:17\.|sedmnáct(?:ý|ého))"},            # seventeenth
    {"value": 18, "pattern": r"(?:18\.|osmnáct(?:ý|ého))"},             # eighteenth
    {"value": 19, "pattern": r"(?:19\.|devatenáct(?:ý|ého))"},          # nineteenth
    {"value": 20, "pattern": r"(?:20\.|dvacát(?:ý|ého))"}               # twentieth
]

patterns["cs"]["daynames"] = [
    # Monday
    {"value": enums.Day.MON, "pattern": r"pondělí"},
    # Tuesday
    {"value": enums.Day.TUE, "pattern": r"úterý"},
    # Wednesday
    {"value": enums.Day.WED, "pattern": r"středa"},
    # Thursday
    {"value": enums.Day.THU, "pattern": r"čtvrtek"},
    # Friday
    {"value": enums.Day.FRI, "pattern": r"pátek"},
    # Saturday
    {"value": enums.Day.SAT, "pattern": r"sobota"},
    # Sunday
    {"value": enums.Day.SUN, "pattern": r"neděle"}
]

patterns["cs"]["monthnames"] = [
    # January
    {"value": enums.Month.JAN, "pattern": r"led(en|n[ua])"},
    # February
    {"value": enums.Month.FEB, "pattern": r"únor[ua]?"},
    # March
    {"value": enums.Month.MAR, "pattern": r"brez(en|n[ua])"},
    # April
    {"value": enums.Month.APR, "pattern": r"dub(en|n[ua])"},
    # May
    {"value": enums.Month.MAY, "pattern": r"květ(en|n[ua])"},
    # June
    {"value": enums.Month.JUN, "pattern": r"červ(en|n[ua])"},
    # July
    {"value": enums.Month.JUL, "pattern": r"červen(ec|c[ie])"},
    # August
    {"value": enums.Month.AUG, "pattern": r"srp(en|n[ua])"},
    # September
    {"value": enums.Month.SEP, "pattern": r"září"},
    # October
    {"value": enums.Month.OCT, "pattern": r"říj(en|n[ua])"},
    # November
    {"value": enums.Month.NOV, "pattern": r"listopadu?"},
    # December
    {"value": enums.Month.DEC, "pattern": r"prosin(ec|c[ie])"}
]

patterns["cs"]["seasonnames"] = [
    # Spring
    {"value": enums.Season.SPRING, "pattern": r"ja(ro|ře)"},
    # Summer
    {"value": enums.Season.SUMMER, "pattern": r"létě"},
    # Autumn
    {"value": enums.Season.AUTUMN, "pattern": r"podzim"},
    # Winter
    {"value": enums.Season.WINTER, "pattern": r"zim[aě]"}
]

patterns["cs"]["dateprefix"] = [
    {"value": enums.DatePrefix.CIRCA, "pattern": r"cca"},
    {"value": enums.DatePrefix.EARLY, "pattern": r"počátek"},
    {"value": enums.DatePrefix.EARLY, "pattern": r"začátek"},
    {"value": enums.DatePrefix.MID, "pattern": r"polovina"},
    {"value": enums.DatePrefix.LATE, "pattern": r"konec"},
    {"value": enums.DatePrefix.HALF1, "pattern": r"první polovina"},
    {"value": enums.DatePrefix.HALF2, "pattern": r"druhá polovina"},
    {"value": enums.DatePrefix.QUARTER1, "pattern": r"první čtvrtina"},
    {"value": enums.DatePrefix.QUARTER2, "pattern": r"druhá čtvrtina"},
    {"value": enums.DatePrefix.QUARTER3, "pattern": r"třetí čtvrtina"},
    {"value": enums.DatePrefix.QUARTER4, "pattern": r"čtvrtá čtvrtina"}
]

patterns["cs"]["datesuffix"] = [
    # NL, AD, CE
    {"value": enums.DateSuffix.CE,
        "pattern": r"(?:našeho letopočtu|n\.?\s?l\.?|A\.?D\.?|C\.?E\.?)"},
    {"value": enums.DateSuffix.BCE,
        # BC, BCE
        "pattern": r"(?:př\.? n\.? l\.?|B\.?C\.?(?:E\.?)?)"},
    # BP
    {"value": enums.DateSuffix.BP, "pattern": r"B\.?P\.?"}
]

patterns["cs"]["dateseparator"] = [
    {"pattern": r"\p{Pd}"},
    {"pattern": r"až?"}
]

# Welsh language patterns
patterns["cy"]["ordinals"] = [
    {"value": 1, "pattern": r"(?:1af|cyntaf)"},                 # first
    {"value": 2, "pattern": r"(?:2il|ail)"},                    # second
    {"value": 3, "pattern": r"(?:3[ey]dd|tryd[ye]dd)"},         # third
    {"value": 4, "pattern": r"(?:4ydd|pedw(?:ery|are)dd)"},       # fourth
    {"value": 5, "pattern": r"(?:5ed|[bp]umed)"},               # fifth
    {"value": 6, "pattern": r"(?:6ed|chweched)"},               # sixth
    {"value": 7, "pattern": r"(?:7fed|seithfed)"},              # seventh
    {"value": 8, "pattern": r"(?:8fed|wythfed)"},               # eighth
    {"value": 9, "pattern": r"(?:9fed|nawfed)"},                # ninth
    {"value": 10, "pattern": r"(?:10fed|degfed)"},               # tenth
    {"value": 11, "pattern": r"(?:11eg|unfed ar ddeg)"},         # eleventh
    {"value": 12, "pattern": r"(?:12fed|d?deuddegfed)"},         # twelfth
    {"value": 13, "pattern": r"(?:13ed|trydydd ar ddeg)"},       # thirteenth
    {"value": 14, "pattern": r"(?:14ed|pedwerydd ar ddeg)"},     # fourteenth
    {"value": 15, "pattern": r"(?:15fed|[bp]ymthegfed)"},        # fifteenth
    {"value": 16, "pattern": r"(?:16eg|unfed ar bymtheg)"},      # sixteenth
    {"value": 17, "pattern": r"(?:17eg|ail ar bymtheg)"},        # seventeenth
    {"value": 18, "pattern": r"(?:18fed|deunawfed)"},            # eighteenth
    {"value": 19, "pattern": r"(?:19eg|pedwerydd ar bymtheg)"},  # nineteenth
    {"value": 20, "pattern": r"(?:20fed|ugeinfed)"},             # twentieth
    {"value": 21, "pattern": r"(?:21ain|unfed ar hugain)"},      # twenty first
    # twenty second
    {"value": 22, "pattern": r"(?:22ain|ail ar hugain)"},
    {"value": 23, "pattern": r"(?:23ain|trydydd ar hugain)"},    # twenty third
    # twenty fourth
    {"value": 24, "pattern": r"(?:24ain|pedwerydd ar hugain)"},
    {"value": 25, "pattern": r"(?:25ain|pumed ar hugain)"},      # twenty fifth
    {"value": 26, "pattern": r"(?:26ain|chweched ar hugain)"},   # twenty sixth
    # twenty seventh
    {"value": 27, "pattern": r"(?:27ain|seithfed ar hugain)"},
    # twenty eighth
    {"value": 28, "pattern": r"(?:28ain|wythfed ar hugain)"},
    {"value": 29, "pattern": r"(?:29ain|nawfed ar hugain)"},     # twenty ninth
    {"value": 30, "pattern": r"(?:30ain|degfed ar hugain)"},     # thirtieth
    # thirty first
    {"value": 31, "pattern": r"(?:31ain|unfed ar ddeg ar hugain)"}
]

patterns["cy"]["daynames"] = [
    # Monday
    {"value": enums.Day.MON, "pattern": r"(?:(?:Dd?|n)ydd\s)?Llun"},
    # Tuesday
    {"value": enums.Day.TUE, "pattern": r"(?:(?:Dd?|n)ydd\s)?[MF]awrth"},
    # Wednesday
    {"value": enums.Day.WED, "pattern": r"(?:(?:Dd?|n)ydd\s)?[MF]ercher"},
    # Thursday
    {"value": enums.Day.THU, "pattern": r"(?:(?:Dd?|n)ydd\s)?Iau"},
    {"value": enums.Day.FRI,
        "pattern": r"(?:(?:Dd?|n)ydd\s)?(?:G|Ng)?wener"},  # Friday
    # Saturday
    {"value": enums.Day.SAT, "pattern": r"(?:(?:Dd?|n)ydd\s)?Sadwrn"},
    # Sunday
    {"value": enums.Day.SUN, "pattern": r"(?:(?:Dd?|n)ydd\s)?Sul"}
]

patterns["cy"]["monthnames"] = [
    # January
    {"value": enums.Month.JAN, "pattern": r"Ion(?:\.|awr)?"},
    # February
    {"value": enums.Month.FEB, "pattern": r"Chwef(?:\.|ror)?"},
    # March
    {"value": enums.Month.MAR, "pattern": r"Maw(?:\.|rth)?"},
    # April
    {"value": enums.Month.APR, "pattern": r"Ebr(?:\.|ill)?"},
    {"value": enums.Month.MAY, "pattern": r"Mai"},                          # May
    {"value": enums.Month.JUN,
        "pattern": r"Meh(?:\.|efin)?"},                # June
    {"value": enums.Month.JUL,
        "pattern": r"Gorff(?:\.|ennaf)?"},             # July
    {"value": enums.Month.AUG, "pattern": r"Awst"},                         # August
    {"value": enums.Month.SEP, "pattern": r"Medi"},                         # September
    # October
    {"value": enums.Month.OCT, "pattern": r"Hyd(?:\.|ref)?"},
    # November
    {"value": enums.Month.NOV, "pattern": r"Tach(?:\.|wedd)?"},
    # December
    {"value": enums.Month.DEC, "pattern": r"Rhag(?:\.|fyr)?"}
]

patterns["cy"]["seasonnames"] = [
    {"value": enums.Season.SPRING,
        "pattern": r"(?:G|Ng)?wanwyn"},            # Spring
    {"value": enums.Season.SUMMER, "pattern": r"Haf"},                      # Summer
    {"value": enums.Season.AUTUMN, "pattern": r"Hydref"},                   # Autumn
    {"value": enums.Season.WINTER,
        "pattern": r"(?:C|G|Ng|Ch|Ngh)?aeaf"}      # Winter
]

patterns["cy"]["dateprefix"] = [
    {"value": enums.DatePrefix.CIRCA, "pattern": r"circa"},
    {"value": enums.DatePrefix.CIRCA, "pattern": r"tua'r"},
    {"value": enums.DatePrefix.CIRCA, "pattern": r"oddeuta"},
    {"value": enums.DatePrefix.CIRCA, "pattern": r"o gwmpas"},
    {"value": enums.DatePrefix.EARLY,
        "pattern": r"(?:gynnar|d?dechrau(?:'r)?)"},
    {"value": enums.DatePrefix.MID, "pattern": r"canol(?:\sy)?"},
    {"value": enums.DatePrefix.LATE,
        "pattern": r"(?:tua\s)?d?diwedd(?:\syr?)?"},
    {"value": enums.DatePrefix.HALF1, "pattern": r"hanner cyntaf(?:\sy)?"},
    {"value": enums.DatePrefix.HALF2, "pattern": r"ail hanner(?:\sy)?"},
    {"value": enums.DatePrefix.QUARTER1,
        "pattern": r"chwarter (?:1|cynt)af(?:\sy)?"},
    {"value": enums.DatePrefix.QUARTER2,
        "pattern": r"[2a]il chwarter(?:\sy)?"},
    {"value": enums.DatePrefix.QUARTER3,
        "pattern": r"(?:3|tryd)ydd chwarter(?:\sy)?"},
    {"value": enums.DatePrefix.QUARTER4,
        "pattern": r"(?:(?:4|pedwer)ydd chwarter|chwarter olaf)(?:\sy)?"},
    {"pattern": r"o"},                # from
    {"pattern": r"cyn"},              # before
    {"pattern": r"yn(\systod)?"},     # During
    {"pattern": r"(ar ôl|er)"},       # post | after | since
    {"pattern": r"(tan|erbyn)"}       # until | by
]

patterns["cy"]["datesuffix"] = [
    # OC, AD, CE
    {"value": enums.DateSuffix.CE,
        "pattern": r"(?:O\.?C\.?|A\.?D\.?|C\.?E\.?)"},
    {"value": enums.DateSuffix.BCE,
        # CC, CCC, BC, BCE
        "pattern": r"(?:(?:C\.?){2,3}|(?:cal\.?\s)?B\.?C\.?(?:E\.?)?)"},
    # BP CP
    {"value": enums.DateSuffix.BP, "pattern": r"[BC]\.?P\.?"}
]

patterns["cy"]["dateseparator"] = [
    {"pattern": r"\p{Pd}"},
    {"pattern": r"(?:hyd|tan|neu|i|a|a'r)"}
]

# experimental only - not connected to datespan work
patterns["cy"]["directions"] = [
    {"value": enums.Direction.N, "pattern": r"Gogledd"},
    {"value": enums.Direction.NE, "pattern": fr"Gogledd{SPACEORDASH}Ddwyrain"},
    {"value": enums.Direction.E, "pattern": r"Dwyrain"},
    {"value": enums.Direction.SE, "pattern": fr"De{SPACEORDASH}Ddwyrain"},
    {"value": enums.Direction.S, "pattern": r"De"},
    {"value": enums.Direction.SW, "pattern": fr"De{SPACEORDASH}Orllewin"},
    {"value": enums.Direction.W, "pattern": r"Gorllewin"},
    {"value": enums.Direction.NW, "pattern": fr"Gogledd{SPACEORDASH}Orllewin"}
]

# German language patterns
patterns["de"]["ordinals"] = [
    {"value": 1, "pattern": r"(?:1\.|erstes?)"},                  # first
    {"value": 2, "pattern": r"(?:2\.|zweiten?)"},               # second
    {"value": 3, "pattern": r"(?:3\.|drittes?)"},                 # third
    {"value": 4, "pattern": r"(?:4\.|viertes?)"},                 # fourth
    {"value": 5, "pattern": r"(?:5\.|fünftes?)"},                 # fifth
    {"value": 6, "pattern": r"(?:6\.|sechstes?)"},                # sixth
    {"value": 7, "pattern": r"(?:7\.|siebtes?)"},                 # seventh
    {"value": 8, "pattern": r"(?:8\.|achtes?)"},                  # eighth
    {"value": 9, "pattern": r"(?:9\.|neuntes?)"},                 # ninth
    {"value": 10, "pattern": r"(?:10\.|zehntes?)"},                # tenth
    {"value": 11, "pattern": r"(?:11\.|elftes?)"},                 # eleventh
    {"value": 12, "pattern": r"(?:12\.|zwölftes?)"},               # twelfth
    {"value": 13, "pattern": r"(?:13\.|dreizehntes?)"},            # thirteenth
    {"value": 14, "pattern": r"(?:14\.|vierzehntes?)"},            # fourteenth
    {"value": 15, "pattern": r"(?:15\.|fünfzehntes?)"},            # fifteenth
    {"value": 16, "pattern": r"(?:16\.|sechzehntes?)"},            # sixteenth
    # seventeenth
    {"value": 17, "pattern": r"(?:17\.|siebzehntes?)"},
    {"value": 18, "pattern": r"(?:18\.|achtzehntes?)"},            # eighteenth
    {"value": 19, "pattern": r"(?:19\.|neunzehntes?)"},            # nineteenth
    {"value": 20, "pattern": r"(?:20\.|zwanzigstes?)"},            # twentieth
    # twenty first
    {"value": 21, "pattern": r"(?:21\.|einundzwanzigstes?)"},
    # twenty second
    {"value": 22, "pattern": r"(?:22\.|zweiundzwanzigstes?)"},
    # twenty third
    {"value": 23, "pattern": r"(?:23\.|dreiundzwanzigstes?)"},
    # twenty fourth
    {"value": 24, "pattern": r"(?:24\.|vierundzwanzigstes?)"},
    # twenty fifth
    {"value": 25, "pattern": r"(?:25\.|fünfundzwanzigstes?)"},
    # twenty sixth
    {"value": 26, "pattern": r"(?:26\.|sechsundzwanzigstes?)"},
    # twenty seventh
    {"value": 27, "pattern": r"(?:27\.|siebenundzwanzigstes?)"},
    # twenty eighth
    {"value": 28, "pattern": r"(?:28\.|achtundzwanzigstes?)"},
    # twenty ninth
    {"value": 29, "pattern": r"(?:29\.|neunundzwanzigstes?)"},
    {"value": 30, "pattern": r"(?:30\.|dreißigstes?)"},            # thirtieth
    # thirty first
    {"value": 31, "pattern": r"(?:31\.|Dreißig zuerst|einunddreißigsten)"}
]

patterns["de"]["daynames"] = [
    {"value": enums.Day.MON, "pattern": r"Mo(?:\.|ntag)?"},         # Monday
    {"value": enums.Day.TUE, "pattern": r"Di(?:\.|enstag)?"},       # Tuesday
    {"value": enums.Day.WED, "pattern": r"Mi(?:\.|ttwoch)?"},       # Wednesday
    {"value": enums.Day.THU, "pattern": r"Do(?:\.|nnerstag)?"},     # Thursday
    {"value": enums.Day.FRI, "pattern": r"Fr(?:\.|eitag)?"},        # Friday
    {"value": enums.Day.SAT, "pattern": r"Sa(?:\.|mstag)?"},        # Saturday
    {"value": enums.Day.SUN, "pattern": r"So(?:\.|nntag)"}          # Sunday
]

patterns["de"]["monthnames"] = [
    {"value": enums.Month.JAN, "pattern": r"J[aä]n(?:\.|uar)?"},      # January
    {"value": enums.Month.FEB,
        "pattern": r"Feb(?:\.|ruar)?"},        # February
    {"value": enums.Month.MAR, "pattern": r"März"},                 # March
    {"value": enums.Month.APR, "pattern": r"Apr(?:\.|il)?"},          # April
    {"value": enums.Month.MAY, "pattern": r"Mai"},                  # May
    {"value": enums.Month.JUN, "pattern": r"Juni"},                 # June
    {"value": enums.Month.JUL, "pattern": r"Juli"},                 # July
    {"value": enums.Month.AUG, "pattern": r"Aug(?:\.|ust)?"},         # August
    {"value": enums.Month.SEP,
        "pattern": r"Sept(?:\.|ember)?"},      # Spetember
    {"value": enums.Month.OCT, "pattern": r"Okt(?:\.|ober)?"},        # October
    {"value": enums.Month.NOV,
        "pattern": r"Nov(?:\.|ember)?"},       # November
    {"value": enums.Month.DEC,
        "pattern": r"Dez(?:\.|ember)?"}        # December
]

patterns["de"]["seasonnames"] = [
    {"value": enums.Season.SPRING, "pattern": r"Frühling"},             # Spring
    {"value": enums.Season.SUMMER, "pattern": r"Sommer"},               # Summer
    {"value": enums.Season.AUTUMN, "pattern": r"Herbst"},               # Autumn
    {"value": enums.Season.WINTER, "pattern": r"Winter"}                # Winter
]

patterns["de"]["dateprefix"] = [
    {"value": enums.DatePrefix.CIRCA, "pattern": r"zirca"},
    {"value": enums.DatePrefix.CIRCA, "pattern": r"ca\.?"},
    {"value": enums.DatePrefix.CIRCA, "pattern": r"um"},
    {"value": enums.DatePrefix.CIRCA, "pattern": r"etwa"},
    {"value": enums.DatePrefix.EARLY,
        "pattern": r"frühe[ns]"},             # early
    {"value": enums.DatePrefix.MID, "pattern": r"Mitte des"},               # mid
    {"value": enums.DatePrefix.LATE,
        "pattern": r"(?:späte[ns]|ende des)"},    # late
    {"value": enums.DatePrefix.HALF1, "pattern": r"erste hälfte des"},      # first half
    {"value": enums.DatePrefix.HALF2,
        "pattern": r"Zweiten? hälfte des"},   # second half
    {"value": enums.DatePrefix.QUARTER1,
        "pattern": r"Erstes Viertel des"},   # first quarter
    {"value": enums.DatePrefix.QUARTER2,
        "pattern": r"Zweites Viertel des"},  # second quarter
    {"value": enums.DatePrefix.QUARTER3,
        "pattern": r"Drittes Viertel des"},  # third quarter
    {"value": enums.DatePrefix.QUARTER4,
        "pattern": r"(?:Viertes|letztes) Viertel des"},  # fourth quarter
    {"pattern": r"anfang"},               # beginning of
    {"pattern": r"(?:ab|von|aus (?:dem)?)"},  # from (the)
    {"pattern": r"vor"},                  # before
    {"pattern": r"(?:im|wurde)"},           # During " was in
    {"pattern": r"(?:nach|seit)"},          # post " after " since
    {"pattern": r"bis"}                   # until " by " to
]


#r"n(\.|a(.?|ch)?)(\sChr(\.?|istus)?)"

patterns["de"]["datesuffix"] = [
    {"value": enums.DateSuffix.CE,
        "pattern": r"(?:n(?:\.|a(?:.?|ch)?)?(?:\sChr(?:\.|istus)?)|A\.?D\.?|C\.?E\.?)"},
    {"value": enums.DateSuffix.BCE,
        "pattern": r"(?:v(?:\.|or)?(?:\sChr(?:\.|istus)?)?|v\.u\.Z\.|(?:cal\.?\s)?B\.?C\.?(?:E\.?)?)"},
    {"value": enums.DateSuffix.BP, "pattern": r"B\.?P\.?"}
]

patterns["de"]["dateseparator"] = [
    {"pattern": r"\p{Pd}"},
    {"pattern": r"bi[st]"},
    {"pattern": r"und"},
    {"pattern": r"oder"}
]

patterns["de"]["directions"] = [
    {"value": enums.Direction.N, "pattern": r"Norden"},
    {"value": enums.Direction.NE, "pattern": r"Nordosten"},
    {"value": enums.Direction.E, "pattern": r"Osten"},
    {"value": enums.Direction.SE, "pattern": r"Süd-Ost"},
    {"value": enums.Direction.S, "pattern": r"Süden"},
    {"value": enums.Direction.SW, "pattern": fr"Südwesten"},
    {"value": enums.Direction.W, "pattern": r"Westen"},
    {"value": enums.Direction.NW, "pattern": fr"Nordwest"}
]

# English language patterns
patterns["en"]["ordinals"] = [
    # 1st, first
    {"value": 1, "pattern": r"(?:1|fir)st"},
    # 2nd, second
    {"value": 2, "pattern": r"(?:2|seco)nd"},
    # 3rd, third
    {"value": 3, "pattern": r"(?:3|thi)rd"},
    # 4th, fourth
    {"value": 4, "pattern": r"(?:4|four)th"},
    # 5th, fifth
    {"value": 5, "pattern": r"(?:5|fif)th"},
    # 6th, sixth
    {"value": 6, "pattern": r"(?:6|six)th"},
    # 7th, seventh
    {"value": 7, "pattern": r"(?:7|seven)th"},
    # 8th, eighth
    {"value": 8, "pattern": r"(?:8|eigh)th"},
    # 9th, ninth
    {"value": 9, "pattern": r"(?:9|nin)th"},
    # 10th, tenth
    {"value": 10, "pattern": r"(?:10|ten)th"},
    # 11th, eleventh
    {"value": 11, "pattern": r"(?:11|eleven)th"},
    # 12th, twelfth
    {"value": 12, "pattern": r"(?:12|twelf)th"},
    # 13th, thirteenth
    {"value": 13, "pattern": r"(?:13|thirteen)th"},
    # 14th, fourteenth
    {"value": 14, "pattern": r"(?:14|fourteen)th"},
    # 15th, fifteenth
    {"value": 15, "pattern": r"(?:15|fifteen)th"},
    # 16th, sixteenth
    {"value": 16, "pattern": r"(?:16|sixteen)th"},
    # 17th, seventeenth
    {"value": 17, "pattern": r"(?:17|seventeen)th"},
    # 18th, eighteenth
    {"value": 18, "pattern": r"(?:18|eighteen)th"},
    # 19th, nineteenth
    {"value": 19, "pattern": r"(?:19|nineteen)th"},
    # 20th, twentieth
    {"value": 20, "pattern": r"(?:20|twentie)th"},
    # 21st, twenty first
    {"value": 21, "pattern": fr"(?:21|twenty{SPACEORDASH}fir)st"},
    # 22nd, twenty second
    {"value": 22, "pattern": fr"(?:22|twenty{SPACEORDASH}seco)nd"},
    # 23rd, twenty third
    {"value": 23, "pattern": fr"(?:23|twenty{SPACEORDASH}thi)rd"},
    # 24th, twenty fourth
    {"value": 24, "pattern": fr"(?:24|twenty{SPACEORDASH}four)th"},
    # 25th, twenty fifth
    {"value": 25, "pattern": fr"(?:25|twenty{SPACEORDASH}fif)th"},
    # 26th, twenty sixth
    {"value": 26, "pattern": fr"(?:26|twenty{SPACEORDASH}six)th"},
    # 27th, twenty seventh
    {"value": 27, "pattern": fr"(?:27|twenty{SPACEORDASH}seven)th"},
    # 28th, twenty eighth
    {"value": 28, "pattern": fr"(?:28|twenty{SPACEORDASH}eigh)th"},
    # 29th, twenty ninth
    {"value": 29, "pattern": fr"(?:29|twenty{SPACEORDASH}nin)th"},
    # 30th, thirtieth
    {"value": 30, "pattern": fr"(?:30|thirtie)th"},
    # 31st, thirty first
    {"value": 31, "pattern": fr"(?:31|thirty{SPACEORDASH}fir)st"}
]

patterns["en"]["daynames"] = [
    # Mon, Mon., Monday
    {"value": enums.Day.MON, "pattern": r"Mon(?:\.|day)?"},
    # Tue, Tue., Tues, Tues., Tuesday
    {"value": enums.Day.TUE, "pattern": r"Tue(?:\.|s\.?|sday)?"},
    # Wed, Wed., Wednesday
    {"value": enums.Day.WED, "pattern": r"Wed(?:\.|nesday)?"},
    # Thu, Thu., Thur, Thur., Thurs, Thursday
    {"value": enums.Day.THU, "pattern": r"Thu(?:\.|rs?\.?|sday)?"},
    # Fri, Fri., Friday
    {"value": enums.Day.FRI, "pattern": r"Fri(?:\.|day)?"},
    # Sat, Sat., Saturday
    {"value": enums.Day.SAT, "pattern": r"Sat(?:\.|urday)?"},
    # Sun, Sun., Sunday
    {"value": enums.Day.SUN, "pattern": r"Sun(?:\.|day)?"}
]

patterns["en"]["monthnames"] = [
    # Jan, Jan., January
    {"value": enums.Month.JAN, "pattern": r"Jan(?:\.|uary)?"},
    # Feb, Feb., February
    {"value": enums.Month.FEB, "pattern": r"Feb(?:\.|ruary)?"},
    # Mar, Mar., March
    {"value": enums.Month.MAR, "pattern": r"Mar(?:\.|ch)?"},
    # Apr, Apr., April
    {"value": enums.Month.APR, "pattern": r"Apr(?:\.|il)?"},
    {"value": enums.Month.MAY, "pattern": r"May"},                      # May
    # Jun, Jun., June
    {"value": enums.Month.JUN, "pattern": r"Jun[\.e]?"},
    # Jul, Jul., July
    {"value": enums.Month.JUL, "pattern": r"Jul[\.y]?"},
    # Aug, Aug., August
    {"value": enums.Month.AUG, "pattern": r"Aug(?:\.|ust)?"},
    # Sep, Sep., Sept, Sept., September
    {"value": enums.Month.SEP, "pattern": r"Sep(?:t?\.?|tember)?"},
    # Oct, Oct., October
    {"value": enums.Month.OCT, "pattern": r"Oct(?:\.|ober)?"},
    # Nov, Nov., November
    {"value": enums.Month.NOV, "pattern": r"Nov(?:\.|ember)?"},
    # Dec, Dec., December
    {"value": enums.Month.DEC, "pattern": r"Dec(?:\.|ember)?"}
]

patterns["en"]["seasonnames"] = [
    {"value": enums.Season.SPRING,
        "pattern": r"Spring(?:time)?"},        # Spring
    {"value": enums.Season.SUMMER,
        "pattern": r"Summer(?:time)?"},        # Summer
    {"value": enums.Season.AUTUMN,
        "pattern": r"(?:Autumn|Fall)"},        # Autumn
    {"value": enums.Season.WINTER,
        "pattern": r"Winter(?:time)?"}         # Winter
]

patterns["en"]["dateprefix"] = [
    {"value": enums.DatePrefix.CIRCA, "pattern": r"(?:circa|ca?\.?|≈)"},
    {"value": enums.DatePrefix.CIRCA, "pattern": r"around"},
    {"value": enums.DatePrefix.CIRCA, "pattern": r"about"},
    {"value": enums.DatePrefix.CIRCA, "pattern": r"approx(?:\.|imately)?"},
    {"value": enums.DatePrefix.EARLY, "pattern": r"early"},
    {"value": enums.DatePrefix.EARLYMID,
        "pattern": fr"early{SPACEORDASH}mid(?:dle)?"},
    {"value": enums.DatePrefix.MID, "pattern": r"mid(?:dle)?"},
    {"value": enums.DatePrefix.MIDLATE,
        "pattern": fr"mid(?:dle)?{SPACEORDASH}later?"},
    {"value": enums.DatePrefix.LATE, "pattern": r"later?"},
    {"value": enums.DatePrefix.HALF1, "pattern": r"(?:1|fir)st half(?:\sof)?"},
    {"value": enums.DatePrefix.HALF2,
        "pattern": r"(?:2|seco)nd half(?:\sof)?"},
    {"value": enums.DatePrefix.QUARTER1,
        "pattern": r"(?:1|fir)st quarter(?:\sof)?"},
    {"value": enums.DatePrefix.QUARTER2,
        "pattern": r"(?:2|seco)nd quarter(?:\sof)?"},
    {"value": enums.DatePrefix.QUARTER3,
        "pattern": r"(?:3|thi)rd quarter(?:\sof)?"},
    {"value": enums.DatePrefix.QUARTER4,
        "pattern": r"(?:(?:4|four)th|last) quarter(?:\sof)?"},
    {"pattern": r"(?:beginning|start|end) of(?:\sthe)?"},
    {"pattern": r"(?:from|until)(?:\sthe)?"},
    {"pattern": r"(?:before|pre|prior to)(?:\sthe)?"},
    {"pattern": r"(?:in|during)(?:\sthe)?"},
    {"pattern": r"(?:post|after|since)(?:\sthe)?"}
]

patterns["en"]["datesuffix"] = [
    {"value": enums.DateSuffix.CE, "pattern": r"(?:A\.?D\.?|C\.?E\.?)"},
    {"value": enums.DateSuffix.BCE,
        "pattern": r"(?:cal\.?\s)?B\.?C\.?(?:E\.?)?"},
    {"value": enums.DateSuffix.BP, "pattern": r"B\.?P\.?"}
]

patterns["en"]["dateseparator"] = [
    {"pattern": r"\p{Pd}"},
    {"pattern": r"/"},
    {"pattern": r"to"},
    {"pattern": r"or"},
    {"pattern": r"and"},
    {"pattern": r"until"}
]

# experimental only - not connected to datespan work
# chemical element names - not actually used yet
# list derived from https:#www.lenntech.com"periodic"symbol"symbol.htm
# todo - unique identifier values - enum chemical element number?
patterns["en"]["elementnames"] = [
    {"pattern": r"Ac(?:tinium)?"},
    {"pattern": r"(?:Ag|Silver)"},
    {"pattern": r"Al(?:umini?um)"},
    {"pattern": r"Am(?:ericium)?"},
    {"pattern": r"Ar(?:gon)?"},
    {"pattern": r"(?:As|Arsenic)"},
    {"pattern": r"(?:At|Astatine)"},
    {"pattern": r"(?:Au|Gold)"},
    {"pattern": r"Ba(?:rium)?"},
    {"pattern": r"Bo(?:ron)?"},
    {"pattern": r"Be(?:ryllium)?"},
    {"pattern": r"(?:Bh|Bohrium)"},
    {"pattern": r"Bi(?:smuth)?"},
    {"pattern": r"(?:Bk|Berkelium)"},
    {"pattern": r"Br(?:omine)?"},
    {"pattern": r"Ca(?:lcium)?"},
    {"pattern": r"(?:Cd|Cadmium)"},
    {"pattern": r"(?:C|arbon)?"},
    {"pattern": r"(?:Ce|rium)?"}
]

# experimental only - not connected to datespan work
patterns["en"]["directions"] = [
    {"value": enums.Direction.N, "pattern": r"North"},
    {"value": enums.Direction.NE, "pattern": fr"North{SPACEORDASH}East"},
    {"value": enums.Direction.E, "pattern": r"East"},
    {"value": enums.Direction.SE, "pattern": fr"South{SPACEORDASH}East"},
    {"value": enums.Direction.S, "pattern": r"South"},
    {"value": enums.Direction.SW, "pattern": fr"South{SPACEORDASH}West"},
    {"value": enums.Direction.W, "pattern": r"West"},
    {"value": enums.Direction.NW, "pattern": fr"North{SPACEORDASH}West"}
]


# Spanish patterns
patterns["es"]["ordinals"] = [
    # first
    {"value": 1, "pattern": r"(?:1\s?°|I|primer[oa]?)"},
    # second
    {"value": 2, "pattern": r"(?:2\s?°|II|2do|segund[oa])"},
    # third
    {"value": 3, "pattern": r"(?:3\s?°|III|3ro|tercer[oa]?)"},
    # fourth
    {"value": 4, "pattern": r"(?:4\s?°|IV|4to|cuart[oa])"},
    # fifth    
    {"value": 5, "pattern": r"(?:5\s?°|V|5to|quint[oa])"},              
    # sixth
    {"value": 6, "pattern": r"(?:6\s?°|VI|6to|sext[oa])"},
    # seventh
    {"value": 7, "pattern": r"(?:7\s?°|VII|7mo|séptim[oa])"},
    # eighth
    {"value": 8, "pattern": r"(?:8\s?°|VIII|8vo|octav[oa])"},
    # ninth
    {"value": 9, "pattern": r"(?:9\s?°|IX|9no|noven[oa])"},
    # tenth
    {"value": 10, "pattern": r"(?:10\s?°|X|10mo|décim[oa])"},
    # eleventh
    {"value": 11, "pattern": r"(?:11\s?°|XI|11mo|undécim[oa])"},
    # twelfth
    {"value": 12, "pattern": r"(?:12\s?°|XII|12mo|duodécim[oa])"},
    # thirteenth
    {"value": 13, "pattern": r"(?:13\s?°|XIII|13ro|decimotercer[oa])"},
    # fourteenth
    {"value": 14, "pattern": r"(?:14\s?°|XIV|14to|decimocuart[oa])"},
    # fifteenth
    {"value": 15, "pattern": r"(?:15\s?°|XV|15to|decimoquint[oa])"},
    # sixteenth
    {"value": 16, "pattern": r"(?:16\s?°|XVI|16to|decimosext[oa])"},
    # seventeenth
    {"value": 17, "pattern": r"(?:17\s?°|XVII|17mo|decimoséptim[oa])"},
    # eighteenth
    {"value": 18, "pattern": r"(?:18\s?°|XVIII|18vo|decimoctav[oa])"},
    # nineteenth
    {"value": 19, "pattern": r"(?:19\s?°|XIX|19no|decimonoven[oa])"},
    # twentieth
    {"value": 20, "pattern": r"(?:20\s?°|XX|20mo|vigésim[oa])"},
    # twenty first
    {"value": 21, "pattern": r"(?:21\s?°|XXI|21ro|vigésimoprimer[oa])"},
    # twenty second
    {"value": 22, "pattern": r"(?:22\s?°|XXII|22do|vigésimosegund[oa])"},
    # twenty third
    {"value": 23, "pattern": r"(?:23\s?°|XXIII|23ro|vigésimotercer[oa])"},
    # twenty fourth
    {"value": 24, "pattern": r"(?:24\s?°|XXIV|24to|vigésimocuart[oa])"},
    # twenty fifth
    {"value": 25, "pattern": r"(?:25\s?°|XXV|25to|vigésimoquint[oa])"},
    # twenty sixth
    {"value": 26, "pattern": r"(?:26\s?°|XXVI|26to|vigésimosext[oa])"},
    # twenty seventh
    {"value": 27, "pattern": r"(?:27\s?°|XXVII|27mo|vigésimoséptim[oa])"},
    # twenty eighth
    {"value": 28, "pattern": r"(?:28\s?°|XXVIII|28vo|vigésimooctav[oa])"},
    # twenty ninth
    {"value": 29, "pattern": r"(?:29\s?°|XXIX|29no|vigésimonoven[oa])"},
    # thirtieth
    {"value": 30, "pattern": r"(?:30\s?°|XXX|30mo|trigésim[oa])"},
    # thirty first
    {"value": 31, "pattern": r"(?:31\s?°|XXXI|31ro|trigésimoprimer[oa])"}
]

patterns["es"]["daynames"] = [
    {"value": enums.Day.MON, "pattern": r"(?:L|Lun|lunes)\b"},      # Monday
    {"value": enums.Day.TUE, "pattern": r"(?:M|Mar|martes)\b"},     # Tuesday
    {"value": enums.Day.WED, "pattern": r"(?:X|Mie|miércoles)\b"},  # Wednesday
    {"value": enums.Day.THU, "pattern": r"(?:J|Jue|jueves)\b"},     # Thursday
    {"value": enums.Day.FRI, "pattern": r"(?:V|Vie|viernes)\b"},    # Friday
    {"value": enums.Day.SAT, "pattern": r"(?:S|Sáb|sábado)\b"},     # Saturday
    {"value": enums.Day.SUN, "pattern": r"(?:D|Dom|domingo)\b"}     # Sunday
]

patterns["es"]["monthnames"] = [
    {"value": enums.Month.JAN, "pattern": r"Enero"},            # January
    {"value": enums.Month.FEB, "pattern": r"Feb(?:\.|rero)?"},    # February
    {"value": enums.Month.MAR, "pattern": r"Marzo"},            # March
    {"value": enums.Month.APR, "pattern": r"Abr(?:\.|il)?"},      # April
    {"value": enums.Month.MAY, "pattern": r"Mayo"},             # May
    {"value": enums.Month.JUN, "pattern": r"Jun(?:\.|io)?"},      # June
    {"value": enums.Month.JUL, "pattern": r"Jul(?:\.|io)?"},      # July
    {"value": enums.Month.AUG, "pattern": r"Agosto"},           # August
    {"value": enums.Month.SEP, "pattern": r"Sept(?:\.|iembre)?"},  # September
    {"value": enums.Month.OCT, "pattern": r"Oct(?:\.|ubre)?"},    # October
    {"value": enums.Month.NOV, "pattern": r"Nov(?:\.|iembre)?"},  # November
    {"value": enums.Month.DEC, "pattern": r"Dic(?:\.|iembre)?"}   # December
]

patterns["es"]["seasonnames"] = [
    {"value": enums.Season.SPRING, "pattern": r"Primavera"},    # Spring
    {"value": enums.Season.SUMMER, "pattern": r"Verano"},       # Summer
    {"value": enums.Season.AUTUMN, "pattern": r"Otoño"},        # Autumn
    {"value": enums.Season.WINTER, "pattern": r"Invierno"}      # Winter
]

patterns["es"]["dateprefix"] = [
    {"value": enums.DatePrefix.CIRCA, "pattern": r"hacia"},
    {"value": enums.DatePrefix.CIRCA, "pattern": r"aprox(?:\.|imadamente)?"},
    {"value": enums.DatePrefix.CIRCA, "pattern": r"aproximadamente"},
    {"value": enums.DatePrefix.CIRCA, "pattern": r"Alrededor de(?:l año)?"},
    {"value": enums.DatePrefix.EARLY,
        "pattern": r"(?:principios|inicio) del?"},  # beginning of
    {"value": enums.DatePrefix.MID, "pattern": r"Mediados del?"},
    {"value": enums.DatePrefix.LATE, "pattern": r"Finales del?"},  # end of
    {"value": enums.DatePrefix.HALF1, "pattern": r"Primera mitad del?"},
    {"value": enums.DatePrefix.HALF2, "pattern": r"Segunda mitad del?"},
    {"value": enums.DatePrefix.QUARTER1, "pattern": r"Primer cuarto del?"},
    {"value": enums.DatePrefix.QUARTER2, "pattern": r"Segundo cuarto del?"},
    {"value": enums.DatePrefix.QUARTER3, "pattern": r"Tercer trimestre del?"},
    {"value": enums.DatePrefix.QUARTER4, "pattern": r"Cuarto cuarto del?"},
    {"pattern": r"de"},                       # from
    {"pattern": r"antes de"},                 # before
    {"pattern": r"durante"},                  # During
    {"pattern": r"(?:post|después de|desde)"},  # post / after / since
    {"pattern": r"(?:hasta|para)"}              # until / by
]

patterns["es"]["datesuffix"] = [
    {"value": enums.DateSuffix.CE,
        "pattern": r"(?:d[.\s]?C\.?|A\.?D\.?|C\.?E\.?)"},
    {"value": enums.DateSuffix.BCE,
        "pattern": r"(?:a[.\s]?C\.?|antes de Cristo|(?:cal\.?\s)?B\.?C\.?(?:E\.?)?)"},
    {"value": enums.DateSuffix.BP, "pattern": r"B\.?P\.?"}
]

patterns["es"]["dateseparator"] = [
    {"pattern": r"(?:\p{Pd}|\/|hasta|a(?:\sla)?|y|o)"}  
]

patterns["es"]["directions"] = [
    {"value": enums.Direction.N, "pattern": r"Norte"},
    {"value": enums.Direction.NE, "pattern": r"Noreste"},
    {"value": enums.Direction.E, "pattern": r"Este"},
    {"value": enums.Direction.SE, "pattern": r"Sureste"},
    {"value": enums.Direction.S, "pattern": r"Sur"},
    {"value": enums.Direction.SW, "pattern": fr"Sur oeste"},
    {"value": enums.Direction.W, "pattern": r"Oeste"},
    {"value": enums.Direction.NW, "pattern": fr"Noroeste"}
]

# French patterns
patterns["fr"]["ordinals"] = [
    # zeroth
    {"value": 0, "pattern": r"zéro[iï]ème"},
    # first
    {"value": 1, "pattern": r"(?:(?:1|I)er?|premi(?:er|ère))"},
    # second
    {"value": 2, "pattern": r"(?:(?:2|II)(?:e|ème)|deuxième|seconde?)"},
    # third
    {"value": 3, "pattern": r"(?:(?:3|III)(?:e|ème)|troisième)"},
    # fourth
    {"value": 4, "pattern": r"(?:(?:4|IV)(?:e|ème)|quatrième)"},
    # fifth
    {"value": 5, "pattern": r"(?:(?:5|V)(?:e|ème)|cinquième)"},
    # sixth
    {"value": 6, "pattern": r"(?:(?:6|VI)(?:e|ème)|sixième)"},
    # seventh
    {"value": 7, "pattern": r"(?:(?:7|VII)(?:e|ème)|septième)"},
    # eighth
    {"value": 8, "pattern": r"(?:(?:8|VIII)(?:e|ème)|huitième)"},
    # ninth
    {"value": 9, "pattern": r"(?:(?:9|IX)(?:e|ème)|neuvième)"},
    # tenth
    {"value": 10, "pattern": r"(?:(?:10|X)(?:e|ème)|dixième)"},
    # eleventh
    {"value": 11, "pattern": r"(?:(?:11|XI)(?:e|ème)|onzième)"},
    # twelfth
    {"value": 12, "pattern": r"(?:(?:12|XII)(?:e|ème)|douzième)"},
    # thirteenth
    {"value": 13, "pattern": r"(?:(?:13|XIII)(?:e|ème)|treizième)"},
    # fourteenth
    {"value": 14, "pattern": r"(?:(?:14|XIV)(?:e|ème)|quatorzième)"},
    # fifteenth
    {"value": 15, "pattern": r"(?:(?:15|XV)(?:e|ème)|quinzième)"},
    # sixteenth
    {"value": 16, "pattern": r"(?:(?:16|XVI)(?:e|ème)|seizième)"},
    # seventeenth
    {"value": 17,
        "pattern": fr"(?:(?:17|XVII)(?:e|ème)|dix{SPACEORDASH}septième)"},
    # eighteenth
    {"value": 18,
        "pattern": fr"(?:(?:18|XVIII)(?:e|ème)|dix{SPACEORDASH}huitième)"},
    # nineteenth
    {"value": 19,
        "pattern": fr"(?:(?:19|XIX)(?:e|ème)|dix{SPACEORDASH}neuvième)"},
    # twentieth
    {"value": 20, "pattern": r"(?:(?:20|XX)(?:e|ème)|vingtième)"},
    # twenty first
    {"value": 21, "pattern": r"(?:(?:21|XXI)(?:e|ème)|vingt et unième)"},
    # twenty second
    {"value": 22,
        "pattern": fr"(?:(?:22|XXII)(?:e|ème)|vingt{SPACEORDASH}deuxième)"},
    # twenty third
    {"value": 23,
        "pattern": fr"(?:(?:23|XXIII)(?:e|ème)|vingt{SPACEORDASH}troisième)"},
    # twenty fourth
    {"value": 24,
        "pattern": fr"(?:(?:24|XXIV)(?:e|ème)|vingt{SPACEORDASH}quatrième)"},
    # twenty fifth
    {"value": 25,
        "pattern": fr"(?:(?:25|XXV)(?:e|ème)|vingt{SPACEORDASH}cinquième)"},
    # twenty sixth
    {"value": 26,
        "pattern": fr"(?:(?:26|XXVI)(?:e|ème)|vingt{SPACEORDASH}sixième)"},
    # twenty seventh
    {"value": 27,
        "pattern": fr"(?:(?:27|XXVII)(?:e|ème)|vingt{SPACEORDASH}septième)"},
    # twenty eighth
    {"value": 28,
        "pattern": fr"(?:(?:28|XXVIII)(?:e|ème)|vingt{SPACEORDASH}huitième)"},
    # twenty ninth
    {"value": 29,
        "pattern": fr"(?:(?:29|XXIX)(?:e|ème)|vingt{SPACEORDASH}neuvième)"},
    # thirtieth
    {"value": 30, "pattern": r"(?:(?:30|XXX)(?:e|ème)|trentième)"},
    # thirty first
    {"value": 31, "pattern": r"(?:(?:31|XXXI)(?:e|ème)|trent et unième)"}
]

patterns["fr"]["daynames"] = [
    {"value": enums.Day.MON, "pattern": r"lun(?:\.|di)?"},      # Monday
    {"value": enums.Day.TUE, "pattern": r"mar(?:\.|di)?"},      # Tuesday
    {"value": enums.Day.WED, "pattern": r"mer(?:\.|credi)?"},   # Wednesday
    {"value": enums.Day.THU, "pattern": r"jeu(?:\.|di)?"},      # Thursday
    {"value": enums.Day.FRI, "pattern": r"ven(?:\.|dredi)?"},   # Friday
    {"value": enums.Day.SAT, "pattern": r"sam(?:\.|edi)?"},     # Saturday
    {"value": enums.Day.SUN, "pattern": r"dim(?:\.|anche)?"}     # Sunday
]

patterns["fr"]["monthnames"] = [
    {"value": enums.Month.JAN, "pattern": r"Janv(?:\.|ier)?"},    # January
    {"value": enums.Month.FEB, "pattern": r"Févr(?:\.|ier)?"},    # February
    {"value": enums.Month.MAR, "pattern": r"Mars"},             # March
    {"value": enums.Month.APR, "pattern": r"Avr(?:\.|il)?"},      # April
    {"value": enums.Month.MAY, "pattern": r"Mai"},              # May
    {"value": enums.Month.JUN, "pattern": r"Juin"},             # June
    {"value": enums.Month.JUL, "pattern": r"Juill(?:\.|et)?"},    # July
    {"value": enums.Month.AUG, "pattern": r"Août"},             # August
    {"value": enums.Month.SEP, "pattern": r"Sept(?:\.|embre)?"},  # September
    {"value": enums.Month.OCT, "pattern": r"Oct(?:\.|obre)?"},    # October
    {"value": enums.Month.NOV, "pattern": r"Nov(?:\.|embre)?"},   # November
    {"value": enums.Month.DEC, "pattern": r"Déc(?:\.|embre)?"}    # December
]

patterns["fr"]["seasonnames"] = [
    {"value": enums.Season.SPRING, "pattern": r"printemps"},    # Spring
    {"value": enums.Season.SUMMER, "pattern": r"été"},          # Summer
    {"value": enums.Season.AUTUMN, "pattern": r"automne"},      # Autumn
    {"value": enums.Season.WINTER, "pattern": r"hiver"}         # Winter
]

patterns["fr"]["dateprefix"] = [
    {"value": enums.DatePrefix.CIRCA, "pattern": r"environ"},
    {"value": enums.DatePrefix.CIRCA, "pattern": r"vers(?:\sle)?"},
    {"value": enums.DatePrefix.CIRCA, "pattern": r"circa"},
    {"value": enums.DatePrefix.EARLY,
        "pattern": r"(?:le\s)?(?:début(?:\sd[ue])?|ancien)"},
    {"value": enums.DatePrefix.MID,
        "pattern": r"(?:le\s)?(?:milieu d[ue]|moyen)"},
    {"value": enums.DatePrefix.LATE,
        "pattern": r"(?:la\s)?(fin(?:\sd[ue])?|récent)"},
    {"value": enums.DatePrefix.HALF1,
        "pattern": r"(?:Première|1er?) moitié d[ue]"},
    {"value": enums.DatePrefix.HALF2,
        "pattern": r"(?:Deuxième|seconde?|2e) moitié d[ue]"},
    {"value": enums.DatePrefix.THIRD1,
        "pattern": r"(?:Première|1er?) tiers d[ue]"},          # 1st third
    {"value": enums.DatePrefix.THIRD2,
        "pattern": r"(?:Deuxième|seconde?|2e) tiers d[ue]"},   # 2nd third
    {"value": enums.DatePrefix.THIRD3,
        "pattern": r"(?:troisième|dernier|3e) tiers d[ue]"},   # last third
    {"value": enums.DatePrefix.QUARTER1,
        "pattern": r"(?:Première|1er?) quart d[ue]"},          # 1st quarter
    {"value": enums.DatePrefix.QUARTER2,
        "pattern": r"(?:Deuxième|seconde?|2e) quart d[ue]"},   # 2nd quarter
    {"value": enums.DatePrefix.QUARTER3,
        "pattern": r"(?:Troisième|3e) quart d[ue]"},           # 3rd quarter
    {"value": enums.DatePrefix.QUARTER4,
        "pattern": r"(?:Quatrième|dernier|4e) quart d[ue]"},   # last quarter
    # pre, post, before, after, during " since
    {"pattern": r"(?:avant|av\.|apr[eè]s|apr?\.|en|depuis)"}
]

patterns["fr"]["datesuffix"] = [
    {
        "value": enums.DateSuffix.CE,
        "pattern": oneof([
            r"apr(?:[eè]s|\.)?\s(?:J[ée]sus[-\s]Christ|J\.?[-\s]?C\.?)",
            r"J\.?C\.?",
            r"A\.?D\.?",
            r"C\.?E\.?"
        ])
    },
    {
        "value": enums.DateSuffix.BCE,
        "pattern": oneof([
            r"av(?:ant|\.)?(?:\s(J[ée]sus[-\s]Christ|J\.?[-\s]?C\.?))?",
            r"(?:cal\.?\s)?B\.?C\.?(E\.?)?"
        ])
    },
    {"value": enums.DateSuffix.BP, "pattern": r"B\.?P\.?"}
]

patterns["fr"]["dateseparator"] = [
    {"pattern": r"\p{Pd}"},
    {"pattern": r"/"},
    {"pattern": r"à"},
    {"pattern": r"au"},
    {"pattern": r"et"},
    {"pattern": r"ou"}
]

patterns["fr"]["directions"] = [
    {"value": enums.Direction.N, "pattern": r"Nord"},
    {"value": enums.Direction.NE, "pattern": fr"Nord{SPACEORDASH}Est"},
    {"value": enums.Direction.E, "pattern": r"Est"},
    {"value": enums.Direction.SE, "pattern": fr"Sud{SPACEORDASH}Est"},
    {"value": enums.Direction.S, "pattern": r"Sud"},
    {"value": enums.Direction.SW, "pattern": fr"Sud{SPACEORDASH}Ouest"},
    {"value": enums.Direction.W, "pattern": r"Ouest"},
    {"value": enums.Direction.NW, "pattern": fr"Nord{SPACEORDASH}Ouest"}
]

# Italian patterns
patterns["it"]["ordinals"] = [
    {"value": 1, "pattern": r"(?:1\s?[°º]|I|primo)"},             # first
    {"value": 2, "pattern": r"(?:2\s?[°º]|II|secondo)"},           # second
    {"value": 3, "pattern": r"(?:3\s?[°º]|III|terzo)"},             # third
    {"value": 4, "pattern": r"(?:4\s?[°º]|IV|quarto)"},            # fourth
    {"value": 5, "pattern": r"(?:5\s?[°º]|V|quinto)"},            # fifth
    {"value": 6, "pattern": r"(?:6\s?[°º]|VI|sesto)"},             # sixth
    {"value": 7, "pattern": r"(?:7\s?[°º]|VII|settimo)"},           # seventh
    {"value": 8, "pattern": r"(?:8\s?[°º]|VIII|ottavo)"},            # eighth
    {"value": 9, "pattern": r"(?:9\s?[°º]|IX|nono)"},              # ninth
    {"value": 10, "pattern": r"(?:10\s?[°º]|X|decimo)"},           # tenth
    {"value": 11, "pattern": r"(?:11\s?[°º]|XI|undicesimo)"},       # eleventh
    {"value": 12, "pattern": r"(?:12\s?[°º]|XII|dodicesimo)"},       # twelfth
    # thirteenth
    {"value": 13, "pattern": r"(?:13\s?[°º]|XIII|tredicesimo)"},
    # fourteenth
    {"value": 14, "pattern": r"(?:14\s?[°º]|XIV|quattordicesimo)"},
    {"value": 15, "pattern": r"(?:15\s?[°º]|XV|quindicesimo)"},     # fifteenth
    # sixteenth
    {"value": 16, "pattern": r"(?:16\s?[°º]|XVI|sedicesimo)"},
    # seventeenth
    {"value": 17, "pattern": r"(?:17\s?[°º]|XVII|diciassettesimo)"},
    # eighteenth
    {"value": 18, "pattern": r"(?:18\s?[°º]|XVIII|diciottesimo)"},
    # nineteenth
    {"value": 19, "pattern": r"(?:19\s?[°º]|XIX|diciannovesimo)"},
    {"value": 20, "pattern": r"(?:20\s?[°º]|XX|ventesimo)"},        # twentieth
    # twenty first
    {"value": 21, "pattern": r"(?:21\s?[°º]|XXI|ventunesimo)"},
    # twenty second
    {"value": 22, "pattern": r"(?:22\s?[°º]|XXII|ventiduesima)"},
    # twenty third
    {"value": 23, "pattern": r"(?:23\s?[°º]|XXIII|ventitreesimo)"},
    # twenty fourth
    {"value": 24, "pattern": r"(?:24\s?[°º]|XXIV|ventiquattresimo)"},
    # twenty fifth
    {"value": 25, "pattern": r"(?:25\s?[°º]|XXV|venticinquesimo)"},
    # twenty sixth
    {"value": 26, "pattern": r"(?:26\s?[°º]|XXVI|ventiseiesimo)"},
    # twenty seventh
    {"value": 27, "pattern": r"(?:27\s?[°º]|XXVII|ventisettesimo)"},
    # twenty eighth
    {"value": 28, "pattern": r"(?:28\s?[°º]|XXVIII|ventotto)"},
    # twenty ninth
    {"value": 29, "pattern": r"(?:29\s?[°º]|XXIX|ventinovesimo)"},
    # thirtieth
    {"value": 30, "pattern": r"(?:30\s?[°º]|XXX|trentesimo)"},
    # thirty first
    {"value": 31, "pattern": r"(?:31\s?[°º]|XXXI|trentunesima)"}
]

patterns["it"]["daynames"] = [
    {"value": enums.Day.MON, "pattern": r"un(?:\.|edì)?"},        # Monday
    {"value": enums.Day.TUE, "pattern": r"mar(?:\.|tedì)?"},      # Tuesday
    {"value": enums.Day.WED, "pattern": r"mer(?:\.|coledì)?"},    # Wednesday
    {"value": enums.Day.THU, "pattern": r"gio(?:\.|vedì)?"},      # Thursday
    {"value": enums.Day.FRI, "pattern": r"ven(?:\.|erdì)?"},      # Friday
    {"value": enums.Day.SAT, "pattern": r"sab(?:\.|ato)?"},       # Saturday
    {"value": enums.Day.SUN, "pattern": r"do(?:\.|menica)?"}      # Sunday
]

patterns["it"]["monthnames"] = [
    {"value": enums.Month.JAN, "pattern": r"Genn(?:\.|aio)?"},    # January
    {"value": enums.Month.FEB, "pattern": r"Febbr(?:\.|aio)?"},   # February
    {"value": enums.Month.MAR, "pattern": r"Mar(?:\.|zo)?"},      # March
    {"value": enums.Month.APR, "pattern": r"Apr(?:\.|ile)?"},     # April
    {"value": enums.Month.MAY, "pattern": r"Magg(?:\.|io)?"},     # May
    {"value": enums.Month.JUN, "pattern": r"Giu(?:\.|gno)?"},     # June
    {"value": enums.Month.JUL, "pattern": r"Lug(?:\.|lio)?"},     # July
    {"value": enums.Month.AUG, "pattern": r"Ag(?:\.|osto)?"},     # August
    {"value": enums.Month.SEP, "pattern": r"Sett(?:\.|embre)?"},  # September
    {"value": enums.Month.OCT, "pattern": r"Ott(?:\.|obre)?"},    # October
    {"value": enums.Month.NOV, "pattern": r"Nov(?:\.|embre)?"},   # November
    {"value": enums.Month.DEC, "pattern": r"Dic(?:\.|embre)?"}    # December
]

patterns["it"]["seasonnames"] = [
    {"value": enums.Season.SPRING, "pattern": r"Primavera"},    # Spring
    {"value": enums.Season.SUMMER, "pattern": r"Estate"},       # Summer
    {"value": enums.Season.AUTUMN, "pattern": r"Autunno"},      # Autumn
    {"value": enums.Season.WINTER, "pattern": r"Inverno"}       # Winter
]

patterns["it"]["dateprefix"] = [
    {"value": enums.DatePrefix.CIRCA, "pattern": r"(?:circa al|ca\.?)"},
    {"value": enums.DatePrefix.CIRCA, "pattern": r"Intorno a(?:l'?)?"},
    {"value": enums.DatePrefix.EARLY,
        "pattern": r"(?:inizio(?:\sdell?'?)?|Prima Età|Prim[io])"},
    {"value": enums.DatePrefix.MID, "pattern": r"(?:Metà del|Medio|Mezzo)"},
    {"value": enums.DatePrefix.LATE,
        "pattern": r"(?:Tarda Età|fine(?:\sdell?'?)?|Fino al)"},
    {"value": enums.DatePrefix.HALF1,
        "pattern": r"(?:1\s?[°º]|prima) metà del"},
    {"value": enums.DatePrefix.HALF2,
        "pattern": r"(?:2\s?[°º]|seconda) metà del"},
    {"value": enums.DatePrefix.QUARTER1,
        "pattern": r"(?:1\s?[°º]|primo) (?:quarto|trimestre)(\sdel)?"},
    {"value": enums.DatePrefix.QUARTER2,
        "pattern": r"(?:2\s?[°º]|secondo) (?:quarto|trimestre)(\sdel)?"},
    {"value": enums.DatePrefix.QUARTER3,
        "pattern": r"(?:3\s?[°º]|terzo) (?:quarto|trimestre)(\sdel)?"},
    {"value": enums.DatePrefix.QUARTER4,
        "pattern": r"(?:4\s?[°º]|quarto|ultimo) (?:quarto|trimestre)(\sdel)?"},
    {"pattern": r"tra(?:\slo)?"},             # between / between the
    {"pattern": r"in"},                      # from
    {"pattern": r"dal"},                      # from
    {"pattern": r"prima(?:\sdell?'?)?"},      # before
    {"pattern": r"nel"},                      # during
    {"pattern": r"(?:post|dopo il|dal)"},       # post " after " since
    {"pattern": r"(?:fino al|entro il)"}        # until " by
]

patterns["it"]["datesuffix"] = [
    {"value": enums.DateSuffix.CE, "pattern": r"(?:d\.?C\.?|C\.?E\.?)"},
    {"value": enums.DateSuffix.BCE,
        "pattern": r"(?:a\.?C\.?|(?:cal\.?\s)?B\.?C\.?(?:E\.?)?)"},
    {"value": enums.DateSuffix.BP, "pattern": r"B\.?P\.?"}
]

patterns["it"]["dateseparator"] = [
    {"pattern": r"\p{Pd}"},
    {"pattern": r"/"},
    {"pattern": r"a"},
    {"pattern": r"all(?:a|')"},
    {"pattern": r"ed?\slo"},
    {"pattern": r"e"}
]

patterns["it"]["directions"] = [
    {"value": enums.Direction.N, "pattern": r"Nord"},
    {"value": enums.Direction.NE, "pattern": fr"Nord{SPACEORDASH}Est"},
    {"value": enums.Direction.E, "pattern": r"Est"},
    {"value": enums.Direction.SE, "pattern": fr"Sud{SPACEORDASH}Est"},
    {"value": enums.Direction.S, "pattern": r"Sud"},
    {"value": enums.Direction.SW, "pattern": fr"Sud{SPACEORDASH}Ovest"},
    {"value": enums.Direction.W, "pattern": r"Ovest"},
    {"value": enums.Direction.NW, "pattern": fr"Nord{SPACEORDASH}Ovest"}
]

# Dutch patterns
patterns["nl"]["ordinals"] = [
    {"value": 1, "pattern": r"(?:1e|eerste)"},              # first
    {"value": 2, "pattern": r"(?:2e|tweede)"},              # second
    {"value": 3, "pattern": r"(?:3e|derde)"},               # third
    {"value": 4, "pattern": r"(?:4e|vierde)"},              # fourth
    {"value": 5, "pattern": r"(?:5e|vijfe)"},               # fifth
    {"value": 6, "pattern": r"(?:6e|zesde)"},               # sixth
    {"value": 7, "pattern": r"(?:7e|zevende)"},             # seventh
    {"value": 8, "pattern": r"(?:8(?:st)?e|achtse)"},         # eighth
    {"value": 9, "pattern": r"(?:9d?e|negende)"},           # ninth
    {"value": 10, "pattern": r"(?:10e|tiende)"},             # tenth
    {"value": 11, "pattern": r"(?:11e|elfde)"},              # eleventh
    {"value": 12, "pattern": r"(?:12e|twaalfde)"},           # twelfth
    {"value": 13, "pattern": r"(?:13e|dertiende)"},          # thirteenth
    {"value": 14, "pattern": r"(?:14e|veertiende)"},         # fourteenth
    {"value": 15, "pattern": r"(?:15e|vijftiende)"},         # fifteenth
    {"value": 16, "pattern": r"(?:16e|zestiende)"},          # sixteenth
    {"value": 17, "pattern": r"(?:17e|zeventiende)"},        # seventeenth
    {"value": 18, "pattern": r"(?:18e|achttiende)"},         # eighteenth
    {"value": 19, "pattern": r"(?:19e|negentiende)"},        # nineteenth
    {"value": 20, "pattern": r"(?:20e|twintigste)"},         # twentieth
    {"value": 21, "pattern": r"(?:21e|eenentwintigste)"},    # twenty first
    {"value": 22, "pattern": r"(?:22e|tweeëntwintigste)"},   # twenty second
    {"value": 23, "pattern": r"(?:23e|drieëntwintig)"},      # twenty third
    {"value": 24, "pattern": r"(?:24e|vierentwintig)"},      # twenty fourth
    {"value": 25, "pattern": r"(?:25e|vijfentwintig)"},      # twenty fifth
    {"value": 26, "pattern": r"(?:26e|zesentwintig)"},       # twenty sixth
    {"value": 27, "pattern": r"(?:27e|zevenentwintig)"},     # twenty seventh
    {"value": 28, "pattern": r"(?:28e|achtentwintig)"},      # twenty eighth
    {"value": 29, "pattern": r"(?:29ste|negenentwintig)"},   # twenty ninth
    {"value": 30, "pattern": r"(?:30e|dertigste)"},          # thirtieth
    {"value": 31, "pattern": r"(?:31e|eenendertigste)"}    # thirty first
]

patterns["nl"]["daynames"] = [
    {"value": enums.Day.MON, "pattern": r"ma(?:\.|andag)?"},        # Monday
    {"value": enums.Day.TUE, "pattern": r"di(?:\.|nsdag)?"},        # Tuesday
    {"value": enums.Day.WED, "pattern": r"woe(?:\.|nsdag)?"},       # Wednesday
    {"value": enums.Day.THU, "pattern": r"don(?:\.|derdag)?"},      # Thursday
    {"value": enums.Day.FRI, "pattern": r"vrij(?:\.|dag)?"},        # Friday
    {"value": enums.Day.SAT, "pattern": r"zat(?:\.|erdag)?"},       # Saturday
    {"value": enums.Day.SUN, "pattern": r"zon(?:\.|dag)?"}          # Sunday
]

patterns["nl"]["monthnames"] = [
    {"value": enums.Month.JAN, "pattern": r"Jan(?:\.|uari)?"},        # January
    {"value": enums.Month.FEB,
        "pattern": r"Feb(?:\.|ruari)?"},       # February
    {"value": enums.Month.MAR, "pattern": r"Maart"},                # March
    {"value": enums.Month.APR, "pattern": r"Apr(?:\.|il)?"},          # April
    {"value": enums.Month.MAY, "pattern": r"Mei"},                  # May
    {"value": enums.Month.JUN, "pattern": r"Juni"},                 # June
    {"value": enums.Month.JUL, "pattern": r"Juli"},                 # July
    {"value": enums.Month.AUG, "pattern": r"Aug(?:\.|ustus)?"},       # August
    {"value": enums.Month.SEP,
        "pattern": r"Sept(?:\.|ember)?"},      # September
    {"value": enums.Month.OCT, "pattern": r"O[kc]t(?:\.|ober)?"},     # October
    {"value": enums.Month.NOV,
        "pattern": r"Nov(?:\.|ember)?"},       # November
    {"value": enums.Month.DEC,
        "pattern": r"Dec(?:\.|ember)?"}        # December
]

patterns["nl"]["seasonnames"] = [
    {"value": enums.Season.SPRING, "pattern": r"Lente"},        # Spring
    {"value": enums.Season.SUMMER, "pattern": r"Zomer"},        # Summer
    {"value": enums.Season.AUTUMN, "pattern": r"Herfst"},       # Autumn
    {"value": enums.Season.WINTER, "pattern": r"Winter"}        # Winter
]

patterns["nl"]["dateprefix"] = [
    {"value": enums.DatePrefix.CIRCA, "pattern": r"ongeveer"},
    {"value": enums.DatePrefix.CIRCA, "pattern": r"ca\.?"},
    {"value": enums.DatePrefix.EARLY, "pattern": r"(?:Vroege?|begin)"},
    {"value": enums.DatePrefix.MID, "pattern": r"Midden"},
    {"value": enums.DatePrefix.LATE, "pattern": r"(?:Eind|Laat|late)"},
    {"value": enums.DatePrefix.HALF1, "pattern": r"Eerste helft"},
    {"value": enums.DatePrefix.HALF2, "pattern": r"Tweede helft"},
    {"value": enums.DatePrefix.QUARTER1, "pattern": r"Eerste kwartier"},
    {"value": enums.DatePrefix.QUARTER2, "pattern": r"Tweede kwartaal"},
    {"value": enums.DatePrefix.QUARTER3, "pattern": r"Derde kwartaal"},
    {"value": enums.DatePrefix.QUARTER4, "pattern": r"Vierde kwart"},
    {"pattern": r"eind"},         # end of
    {"pattern": r"vanaf"},        # from
    {"pattern": r"voor"},         # before
    {"pattern": r"in"},           # During
    {"pattern": r"(?:na|sinds)"},   # post " after " since
    {"pattern": r"(?:tot|tegen)"}   # until " by
]

patterns["nl"]["datesuffix"] = [
    {"value": enums.DateSuffix.CE,
        "pattern": r"(?:na?\.?\s?(?:Christus|Chr\.?)|A\.?D\.?|C\.?E\.?)"},
    {"value": enums.DateSuffix.BCE,
        "pattern": r"(?:(?:voor|vóór|v\.?)\s?(?:Christus|Chr\.?|c\.?)|(?:cal\.?\s)?B\.?C\.?(E\.?)?)"},
    {"value": enums.DateSuffix.BP,
        "pattern": r"(?:(?:år\s)?före nutid|B\.?P\.?)"}
]

patterns["nl"]["dateseparator"] = [
    {"pattern": r"\p{Pd}"},
    {"pattern": r"/"},
    {"pattern": r"tot"},
    {"pattern": r"en"},
    {"pattern": r"of"}
]

patterns["nl"]["directions"] = [
    {"value": enums.Direction.N, "pattern": r"Noorden"},
    {"value": enums.Direction.NE, "pattern": fr"Noord{SPACEORDASH}Oost"},
    {"value": enums.Direction.E, "pattern": r"Oosten"},
    {"value": enums.Direction.SE, "pattern": fr"Zuid{SPACEORDASH}Oost"},
    {"value": enums.Direction.S, "pattern": r"Zuiden"},
    {"value": enums.Direction.SW, "pattern": fr"Zuid{SPACEORDASH}West"},
    {"value": enums.Direction.W, "pattern": r"West"},
    {"value": enums.Direction.NW, "pattern": fr"Noord{SPACEORDASH}West"}
]

# Norwegian patterns
patterns["no"]["ordinals"] = [
    {"value": 1, "pattern": r"(?:1\.?|f?ørste?)"},          # first
    {"value": 2, "pattern": r"(?:2\.?|an(?:nen|na|net|dre))"},  # second
    {"value": 3, "pattern": r"(?:3\.?|tredje)"},            # third
    {"value": 4, "pattern": r"(?:4\.?|fjerde)"},            # fourth
    {"value": 5, "pattern": r"(?:5\.?|femte)"},             # fifth
    {"value": 6, "pattern": r"(?:6\.?|sjette)"},            # sixth
    {"value": 7, "pattern": r"(?:7\.?|syvende|sjuende)"},   # seventh
    {"value": 8, "pattern": r"(?:8\.?|åttende)"},           # eighth
    {"value": 9, "pattern": r"(?:9\.?|niende)"},            # ninth
    {"value": 10, "pattern": r"(?:10\.?|tiende)"},           # tenth
    {"value": 11, "pattern": r"(?:11\.?|ellevte)"},          # eleventh
    {"value": 12, "pattern": r"(?:12\.?|tolvte)"},           # twelfth
    {"value": 13, "pattern": r"(?:13\.?|trettende)"},        # thirteenth
    {"value": 14, "pattern": r"(?:14\.?|fjortende)"},        # fourteenth
    {"value": 15, "pattern": r"(?:15\.?|femtende)"},         # fifteenth
    {"value": 16, "pattern": r"(?:16\.?|sekstende)"},        # sixteenth
    {"value": 17, "pattern": r"(?:17\.?|syttende)"},         # seventeenth
    {"value": 18, "pattern": r"(?:18\.?|attende)"},          # eighteenth
    {"value": 19, "pattern": r"(?:19\.?|nittende)"},         # nineteenth
    {"value": 20, "pattern": r"(?:20\.?|tyvende|tjuende)"},  # twentieth
    {"value": 21, "pattern": r"(?:21\.?|tjueførste?)"},      # twenty first
    {"value": 22, "pattern": r"(?:22\.?|tjue sekund)"},      # twenty second
    {"value": 23, "pattern": r"(?:23\.?|tjuetredje)"},       # twenty third
    {"value": 24, "pattern": r"(?:24\.?|tjuefjerde)"},       # twenty fourth
    {"value": 25, "pattern": r"(?:25\.?|tjuefemte)"},        # twenty fifth
    {"value": 26, "pattern": r"(?:26\.?|tjuesjette)"},       # twenty sixth
    {"value": 27, "pattern": r"(?:27\.?|tjuesyvende)"},      # twenty seventh
    {"value": 28, "pattern": r"(?:28\.?|tjueåtte)"},         # twenty eighth
    {"value": 29, "pattern": r"(?:29\.?|tjueniende)"},       # twenty ninth
    {"value": 30, "pattern": r"(?:30\.?|tretti)"},           # thirtieth
    {"value": 31, "pattern": r"(?:11\.?|trettiførste?)"}     # thirty first
]

patterns["no"]["daynames"] = [
    {"value": enums.Day.MON, "pattern": r"m(?:å|aa?)n(?:dag)?"},  # Monday
    {"value": enums.Day.TUE, "pattern": r"t(?:y|ir)s(?:dag)?"},   # Tuesday
    {"value": enums.Day.WED, "pattern": r"ons(?:dag)?"},        # Wednesday
    {"value": enums.Day.THU, "pattern": r"tors(?:dag)?"},       # Thursday
    {"value": enums.Day.FRI, "pattern": r"fre(?:dag)?"},        # Friday
    {"value": enums.Day.SAT, "pattern": r"l(?:au|ø)(?:r|dag)?"},  # Saturday
    {"value": enums.Day.SUN, "pattern": r"søn(?:dag)?"},        # Sunday
    {"pattern": r"i forgårs"},        # Day before yesterday
    {"pattern": r"i går"},            # Yesterday
    {"pattern": r"i dag"},            # Today
    {"pattern": r"i morgen"},         # Tomorrow
    {"pattern": r"i overmorgen"}      # Day after tomorrow
]

patterns["no"]["monthnames"] = [
    {"value": enums.Month.JAN, "pattern": r"jan(?:uar)?"},    # January
    {"value": enums.Month.FEB, "pattern": r"feb(?:r|ruar)?"},  # February
    {"value": enums.Month.MAR, "pattern": r"mars?"},        # March
    {"value": enums.Month.APR, "pattern": r"apr(?:il)?"},     # April
    {"value": enums.Month.MAY, "pattern": r"mai"},          # May
    {"value": enums.Month.JUN, "pattern": r"juni?"},        # June
    {"value": enums.Month.JUL, "pattern": r"juli?"},        # July
    {"value": enums.Month.AUG, "pattern": r"aug(?:ust)?"},    # August
    {"value": enums.Month.SEP, "pattern": r"sept(?:ember)?"},  # September
    {"value": enums.Month.OCT, "pattern": r"okt(?:ober)?"},   # October
    {"value": enums.Month.NOV, "pattern": r"nov(?:ember)?"},  # November
    {"value": enums.Month.DEC, "pattern": r"des(?:ember)?"}   # December
]

patterns["no"]["seasonnames"] = [
    {"value": enums.Season.SPRING, "pattern": r"(?:på\s)?vår(?:en)?(?:\sI)?"},
    {"value": enums.Season.SUMMER, "pattern": r"(?:på\s)?sommer(?:en)?"},
    {"value": enums.Season.AUTUMN, "pattern": r"(?:på\s)?høst(?:en)?"},
    {"value": enums.Season.WINTER, "pattern": r"(?:på\s)?vinter(?:en)?"},
    {"pattern": r"mørketiden"},               # dark time
    {"pattern": r"(?:på\s)?vinterhalvåret"},    # winter half
    {"pattern": r"(?:på\s)?sommerhalvåret"}     # summer half
]

patterns["no"]["dateprefix"] = [
    {"value": enums.DatePrefix.CIRCA, "pattern": r"cir[ck]a"},
    {"value": enums.DatePrefix.CIRCA, "pattern": r"ca\.?"},
    {"value": enums.DatePrefix.CIRCA, "pattern": r"rundt"},
    {"value": enums.DatePrefix.CIRCA, "pattern": r"omtrent"},
    {"value": enums.DatePrefix.EARLY,
        "pattern": r"(?:[eäæ]ldre|eldste|tidl?[ei]g(?:\spå)?|begynnelsen av)"},
    {"value": enums.DatePrefix.MID,
        "pattern": r"(?:midt(en)?(\sdet)?|mellom)(?:\sav(\sdet)?)?"},
    {"value": enums.DatePrefix.LATE,
        "pattern": r"(?:Yngre|sei?n\p{Pd}?|slutten av|sent|hø[gy]\p{Pd}?)"},
    # first half (of the)
    {"value": enums.DatePrefix.HALF1,
        "pattern": r"f?ørste halvdel(?:\sav(?:\sdet)?)?"},
    {"value": enums.DatePrefix.HALF2,
        # second half (of the)
        "pattern": r"(?:andre|annen) halvdel(?:\sav(?:\sdet)?)?"},
    # first quarter (of the)
    {"value": enums.DatePrefix.QUARTER1,
        "pattern": r"f?ørste kvartal(?:\sav(?:\sdet)?)?"},
    # second quarter (of the)
    {"value": enums.DatePrefix.QUARTER2,
        "pattern": r"andre kvartal(?:\sav(?:\sdet)?)?"},
    # third quarter (of the)
    {"value": enums.DatePrefix.QUARTER3,
        "pattern": r"tredje kvartal(?:\sav(?:\sdet)?)?"},
    # fourth|last quarter (of the)
    {"value": enums.DatePrefix.QUARTER4,
        "pattern": r"(?:fjerde|siste) kvartal(?:\sav(?:\sdet)?)?"},
    {"pattern": r"inngangen til"},                    # beginning of
    {"pattern": r"(?:I\s)?begynnelsen av(?:\sdet)?"},     # beginning of
    {"pattern": r"slutten av(?:\sdet)?"},               # end of
    {"pattern": r"fr(?:å|aa?)"},                        # from
    {"pattern": r"f[oø]r"},                           # before
    {"pattern": r"(?:I|på)"},                           # in
    {"pattern": r"(?:I\s)?løpet av"},                   # During
    {"pattern": r"(?:etter|siden)"},                    # post " after " since
    {"pattern": r"(?:inn)?til"}                       # until " by
]

patterns["no"]["datesuffix"] = [
    {"value": enums.DateSuffix.CE,
        "pattern": r"(?:e\.\s?Kr\.?|A\.?D\.?|C\.?E\.?)"},
    {"value": enums.DateSuffix.BCE,
        "pattern": r"(?:før nåtid|f\.\s?Kr\.?|fvt\.?|(?:cal\.?\s)?B\.?C\.?(?:E\.?)?)"},
    {"value": enums.DateSuffix.BP, "pattern": r"B\.?P\.?"}
]

patterns["no"]["dateseparator"] = [
    {"pattern": r"\p{Pd}"},
    {"pattern": r"/"},
    {"pattern": r"til"},
    {"pattern": r"og"},
    {"pattern": r"och"},
    {"pattern": r"eller"}
]

patterns["no"]["century"] = [
    {"pattern": r"århundre"}
]

patterns["no"]["millennium"] = [
    {"pattern": r"årtusen"}
]

patterns["no"]["directions"] = [
    {"value": enums.Direction.N, "pattern": r"Nord"},
    {"value": enums.Direction.NE, "pattern": fr"Nord{SPACEORDASH}Øst"},
    {"value": enums.Direction.E, "pattern": r"Øst"},
    {"value": enums.Direction.SE, "pattern": r"Sørøst"},
    {"value": enums.Direction.S, "pattern": r"Sør"},
    {"value": enums.Direction.SW, "pattern": r"Sørvest"},
    {"value": enums.Direction.W, "pattern": r"Vest"},
    {"value": enums.Direction.NW, "pattern": fr"Nord{SPACEORDASH}vest"}
]

# 12th century = 1100-tallet, 12. århundre , 12. århundre f.Kr. (f.Kr. =BC e.Kr. = AD) Femte århundre e.Kr.
# Swedish patterns
patterns["sv"]["ordinals"] = [
    {"value": 1, "pattern": r"(?:1\:\s?a|första)"},         # first
    {"value": 2, "pattern": r"(?:2\:\s?a|andra)"},          # second
    {"value": 3, "pattern": r"(?:3\:\s?e|tredje)"},         # third
    {"value": 4, "pattern": r"(?:4\:\s?e|fjärde)"},         # fourth
    {"value": 5, "pattern": r"(?:5\:\s?e|femte)"},          # fifth
    {"value": 6, "pattern": r"(?:6\:\s?e|sjätte)"},         # sixth
    {"value": 7, "pattern": r"(?:7\:\s?e|sjunde)"},         # seventh
    {"value": 8, "pattern": r"(?:8\:\s?e|åttonde)"},        # eighth
    {"value": 9, "pattern": r"(?:9\:\s?e|nionde)"},         # ninth
    {"value": 10, "pattern": r"(?:10\:\s?e|tionde)"},        # tenth
    {"value": 11, "pattern": r"(?:11\:\s?e|elfte)"},         # eleventh
    {"value": 12, "pattern": r"(?:12\:\s?e|tolfte)"},        # twelfth
    {"value": 13, "pattern": r"(?:13\:\s?e|trettonde)"},     # thirteenth
    {"value": 14, "pattern": r"(?:14\:\s?e|fjortonde)"},     # fourteenth
    {"value": 15, "pattern": r"(?:15\:\s?e|femtonde)"},      # fifteenth
    {"value": 16, "pattern": r"(?:16\:\s?e|sextonde)"},      # sixteenth
    {"value": 17, "pattern": r"(?:17\:\s?e|sjuttonde)"},     # seventeenth
    {"value": 18, "pattern": r"(?:18\:\s?e|artonde)"},       # eighteenth
    {"value": 19, "pattern": r"(?:19\:\s?e|nittonde)"},      # nineteenth
    {"value": 20, "pattern": r"(?:20\:\s?e|tjugonde)"},      # twentieth
    {"value": 21, "pattern": r"(?:21\:\s?e|tjugoförsta)"},   # twenty first
    {"value": 22, "pattern": r"(?:22\:\s?e|tjugoandra)"},    # twenty second
    {"value": 23, "pattern": r"(?:23\:\s?e|tjugotredje)"},   # twenty third
    {"value": 24, "pattern": r"(?:24\:\s?e|tjugofjärde)"},   # twenty fourth
    {"value": 25, "pattern": r"(?:25\:\s?e|tjugofemte)"},    # twenty fifth
    {"value": 26, "pattern": r"(?:26\:\s?e|tjugosjätte)"},   # twenty sixth
    {"value": 27, "pattern": r"(?:27\:\s?e|tjugosjunde)"},   # twenty seventh
    {"value": 28, "pattern": r"(?:28\:\s?e|tjugoåttonde)"},  # twenty eighth
    {"value": 29, "pattern": r"(?:29\:\s?e|tjugonionde)"},   # twenty ninth
    {"value": 30, "pattern": r"(?:30\:\s?e|trettionde)"},    # thirtieth
    {"value": 31, "pattern": r"(?:31\:\s?e|trettioförsta)"}  # thirty first
]

patterns["sv"]["daynames"] = [
    {"value": enums.Day.MON, "pattern": r"Mån(?:\.|dag)?"},     # Monday
    {"value": enums.Day.TUE, "pattern": r"Tis(?:\.|dag)?"},     # Tuesday
    {"value": enums.Day.WED, "pattern": r"Ons(?:\.|dag)?"},     # Wednesday
    {"value": enums.Day.THU, "pattern": r"Tors(?:\.|dag)?"},    # Thursday
    {"value": enums.Day.FRI, "pattern": r"Fre(?:\.|dag)?"},     # Friday
    {"value": enums.Day.SAT, "pattern": r"Lör(?:\.|dag)?"},     # Saturday
    {"value": enums.Day.SUN, "pattern": r"Sön(?:\.|dag)?"}     # Sunday
]

patterns["sv"]["monthnames"] = [
    {"value": enums.Month.JAN, "pattern": r"Jan(?:\.|uari)?"},    # January
    {"value": enums.Month.FEB, "pattern": r"Febr(?:\.|uari)?"},   # February
    {"value": enums.Month.MAR, "pattern": r"Mars"},             # March
    {"value": enums.Month.APR, "pattern": r"April"},            # April
    {"value": enums.Month.MAY, "pattern": r"Maj"},              # May
    {"value": enums.Month.JUN, "pattern": r"Juni"},             # June
    {"value": enums.Month.JUL, "pattern": r"Juli"},             # July
    {"value": enums.Month.AUG, "pattern": r"Aug(?:\.|usti)?"},    # August
    {"value": enums.Month.SEP, "pattern": r"Sept(?:\.|ember)?"},  # September
    {"value": enums.Month.OCT, "pattern": r"Okt(?:\.|ober)?"},    # October
    {"value": enums.Month.NOV, "pattern": r"Nov(?:\.|ember)?"},   # November
    {"value": enums.Month.DEC, "pattern": r"Dec(?:\.|ember)?"}   # December
]

patterns["sv"]["seasonnames"] = [
    {"value": enums.Season.SPRING, "pattern": r"Vår"},          # Spring
    {"value": enums.Season.SUMMER, "pattern": r"Sommar"},       # Summer
    {"value": enums.Season.AUTUMN, "pattern": r"Höst"},         # Autumn
    {"value": enums.Season.WINTER, "pattern": r"Vintern?"},    # Winter
    {"pattern": r"vinterhalvåret"},                             # Winter half
    {"pattern": r"Sommarhalvåret"}                             # Summer half
]

patterns["sv"]["dateprefix"] = [
    {"value": enums.DatePrefix.CIRCA, "pattern": r"cirka"},                 # circa
    {"value": enums.DatePrefix.CIRCA, "pattern": r"ungefär"},
    {"value": enums.DatePrefix.CIRCA, "pattern": r"runt"},
    {"value": enums.DatePrefix.EARLY,
        "pattern": r"(?:tidigt|början av)"},  # early
    {"value": enums.DatePrefix.MID, "pattern": r"Mitten av"},               # middle
    {"value": enums.DatePrefix.LATE,
        "pattern": r"(?:Sen[ta]?|sentida|Slutet av)"},  # late
    {"value": enums.DatePrefix.HALF1, "pattern": r"Första hälften av"},     # first half
    {"value": enums.DatePrefix.HALF2,
        "pattern": r"Andra halvan"},          # second half
    {"value": enums.DatePrefix.QUARTER1,
        "pattern": r"första kvartalet"},   # first quarter
    {"value": enums.DatePrefix.QUARTER2,
        "pattern": r"andra kvartalet"},    # second quarter
    {"value": enums.DatePrefix.QUARTER3,
        "pattern": r"tredje kvartalet"},   # third quarter
    {"value": enums.DatePrefix.QUARTER4,
        "pattern": r"fjärde kvartalet"},   # fourth quarter
    {"pattern": r"slutet av(?:\sdet)?"},    # end of
    {"pattern": r"från"},                 # from
    {"pattern": r"före"},                 # before
    {"pattern": r"under"},                # During " in
    {"pattern": r"(?:post|etter|sedan)"},  # post " after " since
    {"pattern": r"(?:fram till|uppåt)"}   # until " by
]

patterns["sv"]["datesuffix"] = [
    {"value": enums.DateSuffix.CE,
        "pattern": r"(?:(?:Efter|e\.?\s?)(?:Kristus|Kr\.?|K\.?)|A\.?D\.?)"},
    {"value": enums.DateSuffix.BCE,
        "pattern": r"(?:(?:före|f\.?\s?)(?:Kristus|Kr\.?|K\.?)|(?:(?:cal\.?\s)?B\.?C\.?))"},
    {"value": enums.DateSuffix.BP,
        "pattern": r"(?:(?:år\s)?före nutid|B\.?P\.?)"},
    {"value": enums.DateSuffix.CE,
        "pattern": r"(?:(?:Efter|Enligt) vår tideräkning|(?:e\.?)?v\.?t\.?|C\.?E\.?)"},
    {"value": enums.DateSuffix.BCE,
        "pattern": r"(?:Före vår tideräkning|f\.?v\.?t\.?|B\.?C\.?E\.?)"}
]

patterns["sv"]["dateseparator"] = [
    {"pattern": r"\p{Pd}"},
    {"pattern": r"/"},
    {"pattern": r"till"},
    {"pattern": r"och"},
    {"pattern": r"e"}
]

patterns["sv"]["directions"] = [
    {"value": enums.Direction.N, "pattern": r"Norr"},
    {"value": enums.Direction.NE, "pattern": r"Nordost"},
    {"value": enums.Direction.E, "pattern": r"öst"},
    {"value": enums.Direction.SE, "pattern": r"Sydost"},
    {"value": enums.Direction.S, "pattern": r"söder"},
    {"value": enums.Direction.SW, "pattern": r"Sydväst"},
    {"value": enums.Direction.W, "pattern": r"väst"},
    {"value": enums.Direction.NW, "pattern": r"nordväst"}
]
