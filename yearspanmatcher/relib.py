# =============================================================================
# Package   : yearspans
# Module    : relib.py
# Version   : Draft 0.1
# Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
# Contact   : ceri.binding@southwales.ac.uk
# Project   : ReMatch
# Summary   :
# regular expression patterns used for identifying date spans/periods within text
# using 'regex' lib rather than 're', to support unicode categories (e.g. \p{Pd}) 
# Imports   : regex, defaultdict, enums, YearSpan
# Example   :
# License   : http://creativecommons.org/publicdomain/zero/1.0/ [CC0]
# =============================================================================
# History
# 22/01/2020 CFB Initially created script (ported from Javascript prototype)
# =============================================================================
#import os.path
#import sys
from collections import defaultdict 
import regex
from . import enums
from .yearspan import YearSpan

# common regex patterns as constant strings
START = r"^"
SPACE = r"\s"
DIGIT = r"\d"
ANY = r"."
END = r"$"
NUMERICYEAR = r"[+-]?[1-9]\d{0,2}(?:\d|[\s,](?:\d{3}))*"
# note unicode property \p{Pd} covers all variants of hyphen/dash
# see https://www.fileformat.info/info/unicode/category/Pd/list.htm
SPACEORDASH = r"(?:\s|\p{Pd})"
ROMAN = r"[MCDLXVI]+"
#SEPARATOR_EN = r"(\s?\p{Pd}\s?|/|\s(to|or|and|until)(\sthe)?\s)"


# Regular expression grouping and repeaters
# returns: '(?:value)' or '(?P<name>value)'
def group(value, name=None, repeat=None):
    newvalue = value
    if(name and str(name).strip() != ""):
        newvalue = f"(?P<{name}>{value})"
    else:
        newvalue = f"(?:{value})"
    if repeat:
        newvalue += repeat
    return newvalue

# returns: true | false
def isgrouped(value):
    return (value.startswith("(") and value.endswith(")"))


# returns: '(?:value)?' or '(?P<name>value)?'
def maybe(value, name=None):
    return group(value, name, "?") 


# returns: '(?:value)*' or '(?P<name>value)*'
def zeroormore(value, name=None):
    return group(value, name, "*") 


# returns: '(?:value)+' or '(?P<name>value)+'
def oneormore(value, name=None):
    return group(value, name, "+")


# returns: '(?:value){n}' or '(?P<name>value){n}'
def exactly(value, name=None, n=1):
    return group(value, name, f"{{{n}}}") 


# returns: '(?:value){n,m}' or '(?P<name>value){n,m}'
def range(value, name=None, n=None, m=None):
    return group(value, name, f"{{{n or ''},{m or ''}}}")  


# Regular expression value options
# returns: '(?:value1|value2|value3)' or '(?P<name>value1|value2|value3)'
def oneof(values, name=None):
    choices = '|'.join(values)
    return group(choices, name)


# Regular expression pattern options
# returns: '(?:patt1|patt2|patt3)' or '(?P<name>patt1|patt2|patt3)'
def oneofp(items, name=None):
    patterns = list(map(lambda item: item['pattern'], items))
    return oneof(patterns, name)


# Get value property by matching s to item pattern
# from patterns array: [{ value: "", pattern:""}]
#@staticmethod
def getValue(s: str, patts):
    if not s:
        return None
    for item in patts:
        match = regex.fullmatch(item['pattern'], s, regex.IGNORECASE)
        if match and "value" in item:
            return item['value']            
    else:
        return None

def getDayNameEnum(s, language) -> enums.Day:
    return getValue(s, patterns[language]["daynames"])


def getMonthNameEnum(s, language) -> enums.Month:
    return getValue(s, patterns[language]["monthnames"])


def getSeasonNameEnum(s, language) -> enums.Season:
    return getValue(s, patterns[language]["seasonnames"])


def getCardinalValue(s, language) -> int: 
    return getValue(s, patterns[language]["cardinals"])


def getOrdinalValue(s, language) -> int: 
    return getValue(s, patterns[language]["ordinals"])


def getDatePrefixEnum(s, language) -> enums.DatePrefix:
    return getValue(s, patterns[language]["dateprefix"])


def getDateSuffixEnum(s, language) -> enums.DateSuffix:
    return getValue(s, patterns[language]["datesuffix"])


def getNamedPeriodValue(s, language):
    return getValue(s, patterns[language]["periodnames"])

# reusable multilingual regular expression pattern library
# defaultdict creates keys if they don't exist when first accessed
patterns = defaultdict(dict)

# Welsh language patterns
patterns["cy"]["cardinals"] = [
    {"value": 1, "pattern": r"(?:1|un)"},
    {"value": 2, "pattern": r"(?:2|dau|dwy)"},
    {"value": 3, "pattern": r"(?:3|tri|tair)"},
    {"value": 4, "pattern": r"(?:4|ped(wa|ai)r)"},
    {"value": 5, "pattern": r"(?:5|pump?)"},
    {"value": 6, "pattern": r"(?:6|chwe(ch)?)"},
    {"value": 7, "pattern": r"(?:7|saith)"},
    {"value": 8, "pattern": r"(?:8|wyth)"},
    {"value": 9, "pattern": r"(?:9|naw)"},
    {"value": 10, "pattern": r"(?:10|deg)"},
    {"value": 11, "pattern": r"(?:11|un (ar ddeg|deg un))"},
    {"value": 12, "pattern": r"(?:12|deuddeg|un deg dau)"},
    {"value": 13, "pattern": r"(?:13|tri ar ddeg|un deg tri)"},
    {"value": 14, "pattern": r"(?:14|pedwar ar ddeg|un deg pedwar)"},
    {"value": 15, "pattern": r"(?:15|pymtheg|un deg pump)"},
    {"value": 16, "pattern": r"(?:16|un ar bymtheg|un deg chwech)"},
    {"value": 17, "pattern": r"(?:17|dau ar bymtheg|un deg saith)"},
    {"value": 18, "pattern": r"(?:18|deunaw|un deg wyth)"},
    {"value": 19, "pattern": r"(?:19|pedwar ar bymtheg|un deg nau)"},
    {"value": 20, "pattern": r"(?:20|ugain|dau ddeg)"},
    {"value": 21, "pattern": r"(?:21|un ar hugain|dau ddeg un)"},
    {"value": 22, "pattern": r"(?:22|dau ar hugain|dau ddeg dau)"},
    {"value": 23, "pattern": r"(?:23|tri ar hugain|dau ddeg tri)"},
    {"value": 24, "pattern": r"(?:24|pedwar ar hugain|dau ddeg pedwar)"},
    {"value": 25, "pattern": r"(?:25|pump ar hugain|dau ddeg pump)"},
    {"value": 26, "pattern": r"(?:26|chwech ar hugain|dau ddeg chwech)"},
    {"value": 27, "pattern": r"(?:27|saith ar hugain|dau ddeg saith)"},
    {"value": 28, "pattern": r"(?:28|wyth ar hugain|dau ddeg wyth)"},
    {"value": 29, "pattern": r"(?:29|naw ar hugain|dau ddeg naw)"},
    {"value": 30, "pattern": r"(?:30|deg ar hugain|tri deg)"},
    {"value": 31, "pattern": r"(?:31|un ar ddeg ar hugain|tri deg un)"}
]

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
    {"value": 22, "pattern": r"(?:22ain|ail ar hugain)"},        # twenty second
    {"value": 23, "pattern": r"(?:23ain|trydydd ar hugain)"},    # twenty third
    {"value": 24, "pattern": r"(?:24ain|pedwerydd ar hugain)"},  # twenty fourth
    {"value": 25, "pattern": r"(?:25ain|pumed ar hugain)"},      # twenty fifth
    {"value": 26, "pattern": r"(?:26ain|chweched ar hugain)"},   # twenty sixth
    {"value": 27, "pattern": r"(?:27ain|seithfed ar hugain)"},   # twenty seventh
    {"value": 28, "pattern": r"(?:28ain|wythfed ar hugain)"},    # twenty eighth
    {"value": 29, "pattern": r"(?:29ain|nawfed ar hugain)"},     # twenty ninth
    {"value": 30, "pattern": r"(?:30ain|degfed ar hugain)"},     # thirtieth
    {"value": 31, "pattern": r"(?:31ain|unfed ar ddeg ar hugain)"}   # thirty first
]

patterns["cy"]["daynames"] = [
    {"value": enums.Day.MON, "pattern": r"(?:(?:Dd?|n)ydd\s)?Llun"},            # Monday
    {"value": enums.Day.TUE, "pattern": r"(?:(?:Dd?|n)ydd\s)?[MF]awrth"},       # Tuesday
    {"value": enums.Day.WED, "pattern": r"(?:(?:Dd?|n)ydd\s)?[MF]ercher"},      # Wednesday
    {"value": enums.Day.THU, "pattern": r"(?:(?:Dd?|n)ydd\s)?Iau"},             # Thursday
    {"value": enums.Day.FRI, "pattern": r"(?:(?:Dd?|n)ydd\s)?(?:G|Ng)?wener"},  # Friday
    {"value": enums.Day.SAT, "pattern": r"(?:(?:Dd?|n)ydd\s)?Sadwrn"},          # Saturday
    {"value": enums.Day.SUN, "pattern": r"(?:(?:Dd?|n)ydd\s)?Sul"}              # Sunday
]

patterns["cy"]["monthnames"] = [
    {"value": enums.Month.JAN, "pattern": r"Ion(?:\.|awr)?"},                 # January
    {"value": enums.Month.FEB, "pattern": r"Chwef(?:\.|ror)?"},               # February
    {"value": enums.Month.MAR, "pattern": r"Maw(?:\.|rth)?"},                 # March
    {"value": enums.Month.APR, "pattern": r"Ebr(?:\.|ill)?"},                 # April
    {"value": enums.Month.MAY, "pattern": r"Mai"},                          # May
    {"value": enums.Month.JUN, "pattern": r"Meh(?:\.|efin)?"},                # June
    {"value": enums.Month.JUL, "pattern": r"Gorff(?:\.|ennaf)?"},             # July
    {"value": enums.Month.AUG, "pattern": r"Awst"},                         # August
    {"value": enums.Month.SEP, "pattern": r"Medi"},                         # September
    {"value": enums.Month.OCT, "pattern": r"Hyd(?:\.|ref)?"},                 # October
    {"value": enums.Month.NOV, "pattern": r"Tach(?:\.|wedd)?"},               # November
    {"value": enums.Month.DEC, "pattern": r"Rhag(?:\.|fyr)?"}                 # December
]

patterns["cy"]["seasonnames"] = [
    {"value": enums.Season.SPRING, "pattern": r"(?:G|Ng)?wanwyn"},            # Spring
    {"value": enums.Season.SUMMER, "pattern": r"Haf"},                      # Summer
    {"value": enums.Season.AUTUMN, "pattern": r"Hydref"},                   # Autumn
    {"value": enums.Season.WINTER, "pattern": r"(?:C|G|Ng|Ch|Ngh)?aeaf"}      # Winter
]

patterns["cy"]["dateprefix"] = [
    {"value": enums.DatePrefix.CIRCA, "pattern": r"circa"},
    {"value": enums.DatePrefix.CIRCA, "pattern": r"tua'r"},
    {"value": enums.DatePrefix.CIRCA, "pattern": r"oddeuta"},
    {"value": enums.DatePrefix.CIRCA, "pattern": r"o gwmpas"},
    {"value": enums.DatePrefix.EARLY, "pattern": r"(?:gynnar|d?dechrau(?:'r)?)"},
    {"value": enums.DatePrefix.MID, "pattern": r"canol(?:\sy)?"},
    {"value": enums.DatePrefix.LATE, "pattern": r"(?:tua\s)?d?diwedd(?:\syr?)?"},
    {"value": enums.DatePrefix.HALF1, "pattern": r"hanner cyntaf(?:\sy)?"},
    {"value": enums.DatePrefix.HALF2, "pattern": r"ail hanner(?:\sy)?"},
    {"value": enums.DatePrefix.QUARTER1, "pattern": r"chwarter (?:1|cynt)af(?:\sy)?"},
    {"value": enums.DatePrefix.QUARTER2, "pattern": r"[2a]il chwarter(?:\sy)?"},
    {"value": enums.DatePrefix.QUARTER3, "pattern": r"(?:3|tryd)ydd chwarter(?:\sy)?"},
    {"value": enums.DatePrefix.QUARTER4, "pattern": r"(?:(?:4|pedwer)ydd chwarter|chwarter olaf)(?:\sy)?"},
    {"pattern": r"o"},                # from
    {"pattern": r"cyn"},              # before
    {"pattern": r"yn(\systod)?"},     # During
    {"pattern": r"(ar ??l|er)"},       # post | after | since
    {"pattern": r"(tan|erbyn)"}       # until | by
]

patterns["cy"]["datesuffix"] = [
    {"value": enums.DateSuffix.AD, "pattern": r"(?:O\.?C\.?|A\.?D\.?|C\.?E\.?)"},                 # OC, AD, CE
    {"value": enums.DateSuffix.BC, "pattern": r"(?:(?:C\.?){2,3}|(?:cal\.?\s)?B\.?C\.?(?:E\.?)?)"},     # CC, CCC, BC, BCE
    {"value": enums.DateSuffix.BP, "pattern": r"[BC]\.?P\.?"}                                   # BP CP
]

patterns["cy"]["dateseparator"] = [
    {"pattern": r"\s?\p{Pd}\s?"},
    {"pattern": r"\s(?:hyd|tan|neu|i|a|a'r)\s"}      
]

# note - unreliable - based on recurring period terms in other languages and translated using Google translate;
# not checked by native speaker. Dates taken from English equivalent periods
patterns["cy"]["periodnames"] = [
    {"pattern": r"(?:Ch?|G|Ngh?)ynhanesyddol", "value": YearSpan(500000, 43)},    # Prehistoric   
    {"pattern": r"(?:Ch?|G|Ngh?)ynhanesyddol cynnar", "value": YearSpan(500000, -4000)},  # Early Prehistoric 
    {"pattern": r"(?:Ch?|G|Ngh?)ynhanesyddol hwyr", "value": YearSpan(4000, 43)}, # Late prehistoric       
    {"pattern": r"pala?eolithig", "value": YearSpan(500000, -10000)},           # Paleolithic
    {"pattern": r"pala?eolithig cynnar", "value": YearSpan(500000, -150000)},   # early Paleolithic
    {"pattern": r"pala?eolithig canol", "value": YearSpan(150000, -40000)},     # middle Paleolithic
    {"pattern": r"pala?eolithig uchaf", "value": YearSpan(40000, -10000)},      # upper Paleolithic
    {"pattern": r"mesolithig", "value": YearSpan(10000, -4000)},                # Mesolithic
    {"pattern": r"mesolithig cynnar", "value": YearSpan(10000, -7000)},         # early Mesolithic
    {"pattern": r"(?:Ch?|G|Ngh?)anol mesolithig"},                                # middle Mesolithic (dates?)
    {"pattern": r"mesolithig hwyr", "value": YearSpan(7000, -4000)},            # late Mesolithic
    {"pattern": r"neolithig", "value": YearSpan(4000, -2200)},                  # Neolithic
    {"pattern": r"neolithig cynnar", "value": YearSpan(4000, -3300)},           # Early Neolithic
    {"pattern": r"(?:Ch?|G|Ngh?)anol neolithig", "value": YearSpan(3300, -2900)}, # Middle Neolithic
    {"pattern": r"neolithig hwyr", "value": YearSpan(2900, -2200)},             # late neolithic
    {"pattern": r"oes efydd", "value": YearSpan(2600, -700)},                   # bronze age
    {"pattern": r"oes efydd gynnar", "value": YearSpan(2600, -1600)},           # early bronze age
    {"pattern": r"(?:Ch?|G|Ngh?)anol oes efydd", "value": YearSpan(1600, -1200)}, # middle bronze age
    {"pattern": r"oes efydd hwyr", "value": YearSpan(1200, -700)},              # late bronze age
    {"pattern": r"oes yr haearn", "value": YearSpan(800, 43)},                  # iron age
    {"pattern": r"oes haearn gynnar", "value": YearSpan(800, -300)},            # early iron age
    {"pattern": r"oes haearn [cg]anol", "value": YearSpan(300, -100)},          # middle iron age
    {"pattern": r"oes haearn hwyr", "value": YearSpan(100, 43)},                # late iron age
    {"pattern": r"Rhufeinig", "value": YearSpan(43, 410)},                      # Roman
    {"pattern": r"Rhufeinig Cynnar", "value": YearSpan()},                      # Early Roman
    {"pattern": r"Rhufeinig Hwyr", "value": YearSpan()},                        # Late Roman        
    {"pattern": fr"Romano{SPACEORDASH}Prydeinig", "value": YearSpan()},         # Romano British 
    {"pattern": fr"(?:Eingl{SPACEORDASH})?Sacsonaidd", "value": YearSpan()},    # Anglo-Saxon
    {"pattern": fr"(?:Sacso{SPACEORDASH})?Normanaidd", "value": YearSpan()},    # Saxo-Norman                       
    {"pattern": r"Cyfnod Modern", "value": YearSpan()},                         # Modern Era       
    {"pattern": r"Oes y Cerrig", "value": YearSpan()},                          # Stone Age
    {"pattern": r"chalcolithic", "value": YearSpan()},                          # Chalcolithic       
    {"pattern": r"(?:Ch?|G|Ngh?)anol\s?oeso(?:l|edd) cynnar", "value": YearSpan(410, 1066)},    # Early Medieval
    {"pattern": r"(?:Ch?|G|Ngh?)anol\s?oeso(?:l|edd)", "value": YearSpan(1066, 1540)},  # Medieval
    {"pattern": r"??l Ganoloesol", "value": YearSpan(1540, 1901)},              # Post-Medieval
    {"pattern": r"Tuduraidd", "value": YearSpan(1485, 1603)},                   # Tudor
    {"pattern": r"Elisabethaidd", "value": YearSpan(1558, 1603)},               # Elizabethan
    {"pattern": r"Stuart", "value": YearSpan(1603, 1714)},                      # Stuart
    {"pattern": r"Jacobean", "value": YearSpan(1603, 1625)},                    # Jacobean
    {"pattern": r"Hanoverian", "value": YearSpan(1714, 1837)},                  # Hanoverian
    {"pattern": r"Sioraidd", "value": YearSpan(1714, 1837)},                    # Georgian
    {"pattern": r"Fictoraidd", "value": YearSpan(1837, 1901)},                  # Victorian
    {"pattern": r"Edwardaidd", "value": YearSpan(1902, 1910)},                  # Edwardian
    {"pattern": r"Rhyfel byd cyntaf", "value": YearSpan(1914, 1918)},           # First World War
    {"pattern": r"Rhwng rhyfel", "value": YearSpan(1919, 1938)},                # Inter war
    {"pattern": r"ail ryfel byd", "value": YearSpan(1939, 1945)}               # Second World War    
]


# composite datespan patterns
patterns["cy"]["datespans"] = [
    {
        # Month and year e.g. "October 1984"
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{month}}) ({{year}})(\s{{suffix}})?".format(
            prefix = oneofp(patterns["cy"]["dateprefix"] , "datePrefix"),
            spaceordash = SPACEORDASH,
            month = oneofp(patterns["cy"]["monthnames"], "monthName"),
            year = NUMERICYEAR,
            suffix = oneofp(patterns["cy"]["datesuffix"], "dateSuffix")
        )
    },
    {
        # Season and year e.g. "summer 1984"
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{season}}) ({{year}})(\s{{suffix}})?".format(
            prefix = oneofp(patterns["cy"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            season = oneofp(patterns["cy"]["seasonnames"]),
            year = NUMERICYEAR,
            suffix = oneofp(patterns["cy"]["datesuffix"])
        )
    },
    {
        # year with suffix e.g. "circa 8100 BCE"
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{year}})(\s?{{suffix}})".format(
            prefix = oneofp(patterns["cy"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            year = NUMERICYEAR,
            suffix = oneofp(patterns["cy"]["datesuffix"])
        )
    },
    {
        # year with prefix e.g. "yn 1485"
        "pattern": fr"({{prefix}}{{spaceordash}}?)+({{year}})(\s?{{suffix}})?".format(
            prefix = oneofp(patterns["cy"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            year = NUMERICYEAR,
            suffix = oneofp(patterns["cy"]["datesuffix"])
        )
    },
    {
        # from year to year
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{fromYear}})(\s?{{suffix}})?{{separator}}({{prefix}}{{spaceordash}}?)*({{toYear}})(\s?{{suffix}})?".format(
            prefix = oneofp(patterns["cy"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            fromYear = NUMERICYEAR,
            separator = oneofp(patterns["cy"]["dateseparator"]),
            toYear = NUMERICYEAR,
            suffix = oneofp(patterns["cy"]["datesuffix"])
        )
    },
    {
        # named historical periods
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{named}})(\s?{{suffix}})?\b".format(
            prefix = oneofp(patterns["cy"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            named = oneofp(patterns["cy"]["periodnames"]),
            suffix = oneofp(patterns["cy"]["datesuffix"])
        )
    },
    {
        # from named to named historical periods
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{named1}}){{separator}}({{prefix}}{{spaceordash}}?)*({{named2}})\b".format(
            prefix = oneofp(patterns["cy"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            named1 = oneofp(patterns["cy"]["periodnames"]),
            named2 = oneofp(patterns["cy"]["periodnames"]),
            separator = oneofp(patterns["cy"]["dateseparator"])
        )
    },
    {
        # decades e.g. e.g. "1550au"
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{decade}})(\s{{suffix}})?".format(
            prefix = oneofp(patterns["cy"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            decade = r"\b[1-9]\d{1,2}0au",
            suffix = oneofp(patterns["cy"]["datesuffix"])
        )
    },
    {
        # from decade to decade e.g. e.g. "1970au a'r 1980au"
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{decade1}}){{separator}}({{prefix}}{{spaceordash}}?)*({{decade2}})\b".format(
            prefix = oneofp(patterns["cy"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            decade1 = r"\b[1-9]\d{1,2}0au",
            decade2 = r"\b[1-9]\d{1,2}0au",
            separator = oneofp(patterns["cy"]["dateseparator"]),
        )
    },
    {
        # Ordinal centuries e.g. "pumed ganrif OC" (5th century AD)
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{ordinal}})\s?g(anrif)?(\s{{suffix}})?".format(
            spaceordash = SPACEORDASH,
            prefix = oneofp(patterns["cy"]["dateprefix"]),
            ordinal = oneofp(patterns["cy"]["ordinals"]),
            suffix = oneofp(patterns["cy"]["datesuffix"])
        )
    },
    {
        # Ordinal centuries e.g. "ganrif 1af CCC" (1st century BCE)
        "pattern": fr"({{prefix}}{{spaceordash}}?)*ganrif ({{ordinal}})(\s{{suffix}})?".format(
            prefix = oneofp(patterns["cy"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            ordinal = oneofp(patterns["cy"]["ordinals"]),
            suffix = oneofp(patterns["cy"]["datesuffix"])
        )
    },
    {
        # From ordinal to ordinal century e.g.
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{fromOrdinal}}) g(anrif)?(\s{{suffix}})?{{separator}}({{prefix}}{{spaceordash}}?)*({{toOrdinal}}) g(anrif)?(\s{{suffix}})?".format(
            prefix = oneofp(patterns["cy"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            fromOrdinal = oneofp(patterns["cy"]["ordinals"]),
            separator = oneofp(patterns["cy"]["dateseparator"]),
            toOrdinal = oneofp(patterns["cy"]["ordinals"]),
            suffix = oneofp(patterns["cy"]["datesuffix"])
        )
    },
    {
        # Cardinal centuries e.g. "ddechrau'r 18g" (Early 18th century)
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{cardinal}})g(anrif)?(\s{{suffix}})?".format(
            prefix = oneofp(patterns["cy"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            cardinal = oneofp(patterns["cy"]["cardinals"]),
            suffix = oneofp(patterns["cy"]["datesuffix"])
        )
    },
    {
        # From cardinal to cardinal century e.g.
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{fromCardinal}})g(anrif)?{{separator}}({{prefix}}{{spaceordash}}?)*({{toCardinal}})g(anrif)?(\s{{suffix}})?".format(
            prefix = oneofp(patterns["cy"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            fromCardinal = oneofp(patterns["cy"]["cardinals"]),
            separator = oneofp(patterns["cy"]["dateseparator"]),
            toCardinal = oneofp(patterns["cy"]["cardinals"]),
            suffix = oneofp(patterns["cy"]["datesuffix"])
        )
    },
    {
        # Ordinal millennium e.g. "dechrau'r 2il mileniwm OC"
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{ordinal}}) mileniwm(\s{{suffix}})?".format(
            prefix = oneofp(patterns["cy"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            ordinal = oneofp(patterns["cy"]["ordinals"]),
            suffix = oneofp(patterns["cy"]["datesuffix"])
        )
    },
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
patterns["de"]["cardinals"] = [
    {"value": 1, "pattern": r"(?:1|eins)"},
    {"value": 2, "pattern": r"(?:2|zwei)"},
    {"value": 3, "pattern": r"(?:3|drei)"},
    {"value": 4, "pattern": r"(?:4|vier)"},
    {"value": 5, "pattern": r"(?:5|f??nf)"},
    {"value": 6, "pattern": r"(?:6|sechs)"},
    {"value": 7, "pattern": r"(?:7|sieben)"},
    {"value": 8, "pattern": r"(?:8|acht)"},
    {"value": 9, "pattern": r"(?:9|neun)"},
    {"value": 10, "pattern": r"(?:10|zehn)"},
    {"value": 11, "pattern": r"(?:11|elf)"},
    {"value": 12, "pattern": r"(?:12|zw??lf)"},
    {"value": 13, "pattern": r"(?:13|dreizehn)"},
    {"value": 14, "pattern": r"(?:14|vierzehn)"},
    {"value": 15, "pattern": r"(?:15|f??nfzehn)"},
    {"value": 16, "pattern": r"(?:16|sechzehn)"},
    {"value": 17, "pattern": r"(?:17|siebzehn)"},
    {"value": 18, "pattern": r"(?:18|achtzehn)"},
    {"value": 19, "pattern": r"(?:19|neunzehn)"},
    {"value": 20, "pattern": r"(?:20|zwanzig)"},
    {"value": 21, "pattern": r"(?:21|einundzwanzig)"},
    {"value": 22, "pattern": r"(?:22|zweiundzwanzig)"},
    {"value": 23, "pattern": r"(?:23|dreiundzwanzig)"},
    {"value": 24, "pattern": r"(?:24|vierundzwanzig)"},
    {"value": 25, "pattern": r"(?:25|f??nfundzwanzig)"},
    {"value": 26, "pattern": r"(?:26|sechsundzwanzig)"},
    {"value": 27, "pattern": r"(?:27|siebenundzwanzig)"},
    {"value": 28, "pattern": r"(?:28|achtundzwanzig)"},
    {"value": 29, "pattern": r"(?:29|neunundzwanzig)"},
    {"value": 30, "pattern": r"(?:30|drei??ig)"},
    {"value": 31, "pattern": r"(?:31|einunddrei??ig)"}
]

patterns["de"]["ordinals"] = [
    {"value": 1, "pattern": r"(?:1\.|erstes?)"},                  # first
    {"value": 2, "pattern": r"(?:2\.|zweiten?)"},               # second
    {"value": 3, "pattern": r"(?:3\.|drittes?)"},                 # third
    {"value": 4, "pattern": r"(?:4\.|viertes?)"},                 # fourth
    {"value": 5, "pattern": r"(?:5\.|f??nftes?)"},                 # fifth
    {"value": 6, "pattern": r"(?:6\.|sechstes?)"},                # sixth
    {"value": 7, "pattern": r"(?:7\.|siebtes?)"},                 # seventh
    {"value": 8, "pattern": r"(?:8\.|achtes?)"},                  # eighth
    {"value": 9, "pattern": r"(?:9\.|neuntes?)"},                 # ninth
    {"value": 10, "pattern": r"(?:10\.|zehntes?)"},                # tenth
    {"value": 11, "pattern": r"(?:11\.|elftes?)"},                 # eleventh
    {"value": 12, "pattern": r"(?:12\.|zw??lftes?)"},               # twelfth
    {"value": 13, "pattern": r"(?:13\.|dreizehntes?)"},            # thirteenth
    {"value": 14, "pattern": r"(?:14\.|vierzehntes?)"},            # fourteenth
    {"value": 15, "pattern": r"(?:15\.|f??nfzehntes?)"},            # fifteenth
    {"value": 16, "pattern": r"(?:16\.|sechzehntes?)"},            # sixteenth
    {"value": 17, "pattern": r"(?:17\.|siebzehntes?)"},            # seventeenth
    {"value": 18, "pattern": r"(?:18\.|achtzehntes?)"},            # eighteenth
    {"value": 19, "pattern": r"(?:19\.|neunzehntes?)"},            # nineteenth
    {"value": 20, "pattern": r"(?:20\.|zwanzigstes?)"},            # twentieth
    {"value": 21, "pattern": r"(?:21\.|einundzwanzigstes?)"},      # twenty first
    {"value": 22, "pattern": r"(?:22\.|zweiundzwanzigstes?)"},     # twenty second
    {"value": 23, "pattern": r"(?:23\.|dreiundzwanzigstes?)"},     # twenty third
    {"value": 24, "pattern": r"(?:24\.|vierundzwanzigstes?)"},     # twenty fourth
    {"value": 25, "pattern": r"(?:25\.|f??nfundzwanzigstes?)"},     # twenty fifth
    {"value": 26, "pattern": r"(?:26\.|sechsundzwanzigstes?)"},    # twenty sixth
    {"value": 27, "pattern": r"(?:27\.|siebenundzwanzigstes?)"},   # twenty seventh
    {"value": 28, "pattern": r"(?:28\.|achtundzwanzigstes?)"},     # twenty eighth
    {"value": 29, "pattern": r"(?:29\.|neunundzwanzigstes?)"},     # twenty ninth
    {"value": 30, "pattern": r"(?:30\.|drei??igstes?)"},            # thirtieth
    {"value": 31, "pattern": r"(?:31\.|Drei??ig zuerst|einunddrei??igsten)"}   # thirty first
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
    {"value": enums.Month.JAN, "pattern": r"J[a??]n(?:\.|uar)?"},      # January
    {"value": enums.Month.FEB, "pattern": r"Feb(?:\.|ruar)?"},        # February
    {"value": enums.Month.MAR, "pattern": r"M??rz"},                 # March
    {"value": enums.Month.APR, "pattern": r"Apr(?:\.|il)?"},          # April
    {"value": enums.Month.MAY, "pattern": r"Mai"},                  # May
    {"value": enums.Month.JUN, "pattern": r"Juni"},                 # June
    {"value": enums.Month.JUL, "pattern": r"Juli"},                 # July
    {"value": enums.Month.AUG, "pattern": r"Aug(?:\.|ust)?"},         # August
    {"value": enums.Month.SEP, "pattern": r"Sept(?:\.|ember)?"},      # Spetember
    {"value": enums.Month.OCT, "pattern": r"Okt(?:\.|ober)?"},        # October
    {"value": enums.Month.NOV, "pattern": r"Nov(?:\.|ember)?"},       # November
    {"value": enums.Month.DEC, "pattern": r"Dez(?:\.|ember)?"}        # December
]

patterns["de"]["seasonnames"] = [
    {"value": enums.Season.SPRING, "pattern": r"Fr??hling"},             # Spring
    {"value": enums.Season.SUMMER, "pattern": r"Sommer"},               # Summer
    {"value": enums.Season.AUTUMN, "pattern": r"Herbst"},               # Autumn
    {"value": enums.Season.WINTER, "pattern": r"Winter"}                # Winter
]

patterns["de"]["dateprefix"] = [
    {"value": enums.DatePrefix.CIRCA, "pattern": r"zirca"},
    {"value": enums.DatePrefix.CIRCA, "pattern": r"ca\.?"},
    {"value": enums.DatePrefix.CIRCA, "pattern": r"um"},
    {"value": enums.DatePrefix.CIRCA, "pattern": r"etwa"},
    {"value": enums.DatePrefix.EARLY, "pattern": r"fr??he[ns]"},             # early
    {"value": enums.DatePrefix.MID, "pattern": r"Mitte des"},               # mid
    {"value": enums.DatePrefix.LATE, "pattern": r"(?:sp??te[ns]|ende des)"},    # late
    {"value": enums.DatePrefix.HALF1, "pattern": r"erste h??lfte des"},      # first half
    {"value": enums.DatePrefix.HALF2, "pattern": r"Zweiten? h??lfte des"},   # second half
    {"value": enums.DatePrefix.QUARTER1, "pattern": r"Erstes Viertel des"},   # first quarter
    {"value": enums.DatePrefix.QUARTER2, "pattern": r"Zweites Viertel des"},  # second quarter
    {"value": enums.DatePrefix.QUARTER3, "pattern": r"Drittes Viertel des"},  # third quarter
    {"value": enums.DatePrefix.QUARTER4, "pattern": r"(?:Viertes|letztes) Viertel des"}, # fourth quarter
    {"pattern": r"anfang"},               # beginning of
    {"pattern": r"(?:ab|von|aus (?:dem)?)"},  # from (the)
    {"pattern": r"vor"},                  # before
    {"pattern": r"(?:im|wurde)"},           # During " was in
    {"pattern": r"(?:nach|seit)"},          # post " after " since
    {"pattern": r"bis"}                   # until " by " to
]


r"n(\.|a(.?|ch)?)(\sChr(\.?|istus)?)"

patterns["de"]["datesuffix"] = [
    {"value": enums.DateSuffix.AD, "pattern": r"(?:n(?:\.|a(?:.?|ch)?)?(?:\sChr(?:\.|istus)?)|A\.?D\.?|C\.?E\.?)"},
    {"value": enums.DateSuffix.BC, "pattern": r"(?:v(?:\.|or)?(?:\sChr(?:\.|istus)?)?|v\.u\.Z\.|(?:cal\.?\s)?B\.?C\.?(?:E\.?)?)"},
    {"value": enums.DateSuffix.BP, "pattern": r"B\.?P\.?"}
]

patterns["de"]["dateseparator"] = [
    {"pattern": r"\s?\p{Pd}\s?"},
    {"pattern": r"\sbi[st]\s"},
    {"pattern": r"\sund\s"},
    {"pattern": r"\soder\s"}      
]

# named periods from RxLookup-NamedPeriod.json - C# project, think originally from Perio.do??
patterns["de"]["periodnames"] = [
    {"pattern": r"Pal??olithikum", "value": YearSpan(-298000, -9550)},               # Palaeolithic
    {"pattern": r"Mittelpal??olithikum", "value": YearSpan(-298000, -41500)},        # Middle palaeolithic
    {"pattern": r"??lteres Jungpal??olithikum", "value": YearSpan(-41500, -32500)},   # Older early palaeolithic
    {"pattern": r"Mittleres Jungpal??olithikum", "value": YearSpan(-32500, -22500)}, # Middle palaeolithic
    {"pattern": r"J??ngeres Jungpal??olithikum", "value": YearSpan(-22500, -11950)},  # Younger palaeolithic
    {"pattern": r"Sp??tpal??olithikum", "value": YearSpan(-11950, -9550)},            # Late palaeolithic
    {"pattern": r"Mesolithikum", "value": YearSpan(-9550, -5600)},                  # Mesolithic
    {"pattern": r"Neolithikum", "value": YearSpan(-5600, -4000)},                   # Neolithic
    {"pattern": r"Fr??hes Neolithikum", "value": YearSpan(-5600, -4800)},            # Early Neolithic
    {"pattern": r"Mittel Neolithikum", "value": YearSpan(-4800, -4000)},            # Middle Neolithic
    {"pattern": r"Kupferzeit", "value": YearSpan(-4000, -2200)},                    # Copper age
    {"pattern": r"??ltere Kupferzeit", "value": YearSpan(-4000, -3400)},             # Older copper age
    {"pattern": r"Mittlere Kupferzeit", "value": YearSpan(-3400, -3000)},           # Middle copper age
    {"pattern": r"J??ngere Kupferzeit", "value": YearSpan(-3000, -2200)},            # Younger copper age
    {"pattern": r"Bronzezeit", "value": YearSpan(-2200, -800)},                     # Bronze age
    {"pattern": r"Fr??hen? Bronzezeit", "value": YearSpan(-2200, -1600)},            # Early bronze age
    {"pattern": r"Mittlere Bronzezeit", "value": YearSpan(-1600, -1300)},           # Middle bronze age
    {"pattern": r"Sp??te Bronzezeit", "value": YearSpan(-1300, -800)},               # Late bronze age
    {"pattern": r"Eisenzeit", "value": YearSpan(-800, 0)},                          # Iron age
    {"pattern": r"??ltere Eisenzeit", "value": YearSpan(-800, -450)},                # Older iron age
    {"pattern": r"J??ngere Eisenzeit", "value": YearSpan(450, 0)},                   # Younger iron age
    {"pattern": r"R??mische(\sPeriode)?", "value": YearSpan(0, 375)},                # Roman period
    {"pattern": r"Fr??he R??mische(\sPeriode)?", "value": YearSpan(0, 180)},          # Early Roman period
    {"pattern": r"Sp??te R??mische(\sPeriode)?", "value": YearSpan(180, 375)},        # Late Roman period
    {"pattern": r"V??lkerwanderungszeit", "value": YearSpan(375, 586)},              # Migration period
    {"pattern": r"Mittelalter", "value": YearSpan(586, 1500)},                      # Medieval / Middle Ages
    {"pattern": r"Fr??hes Mittelalter", "value": YearSpan(586, 976)},                # Early middle ages
    {"pattern": r"Hochmittelalter", "value": YearSpan(976, 1250)},                  # High  middle ages
    {"pattern": r"Sp??tmittelalter", "value": YearSpan(1250, 1500)},                 # Late middle ages
    {"pattern": r"Neuzeit", "value": YearSpan(1500, 1850)},                         # Modern times
    {"pattern": r"Zeitgeschichte", "value": YearSpan(1850, 2000)}                   # Contemporary
]

patterns["de"]["datespans"] = [
    {
        # Month and year
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{month}})\s({{year}})(\s{{suffix}})?".format(
            prefix = oneofp(patterns["de"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            month = oneofp(patterns["de"]["monthnames"]),
            year = NUMERICYEAR,
            suffix = oneofp(patterns["de"]["datesuffix"])
        )
    },
    {
        # Season and year
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{season}}) ({{year}})(\s{{suffix}})?".format(
            prefix = oneofp(patterns["de"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            season = oneofp(patterns["de"]["seasonnames"]),
            year = NUMERICYEAR,
            suffix = oneofp(patterns["de"]["datesuffix"])
        )
    },
    {
        # year with suffix e.g. "circa 8100 BCE"
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{year}})(\s?{{suffix}})".format(
            prefix = oneofp(patterns["de"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            year = NUMERICYEAR,
            suffix = oneofp(patterns["de"]["datesuffix"])
        )
    },
    {
        # year with prefix e.g. "bis 1854"
        "pattern": fr"({{prefix}}{{spaceordash}}?)+({{year}})(\s?{{suffix}})?".format(
            prefix = oneofp(patterns["de"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            year = NUMERICYEAR,
            suffix = oneofp(patterns["de"]["datesuffix"])
        )
    },
    {
        # from year to year
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{fromYear}})(\s?{{suffix}})?{{separator}}({{prefix}}{{spaceordash}}?)*({{toYear}})(\s?{{suffix}})?\b".format(
            prefix = oneofp(patterns["de"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            fromYear = NUMERICYEAR,
            separator = oneofp(patterns["de"]["dateseparator"]),
            toYear = NUMERICYEAR,
            suffix = oneofp(patterns["de"]["datesuffix"])
        )
    },
    {
        # named historical periods
        "pattern":  f"\b({{prefix}}{{spaceordash}}?)*({{named}})\b".format(
            prefix = oneofp(patterns["de"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            named = oneofp(patterns["de"]["periodnames"])
        )
    },
    {
        # from named to named historical periods
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{named1}}){{separator}}({{prefix}}{{spaceordash}}?)*({{named2}})".format(
            prefix = oneofp(patterns["de"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            named1 = oneofp(patterns["de"]["periodnames"]),
            named2 = oneofp(patterns["de"]["periodnames"]),
            separator = oneofp(patterns["de"]["dateseparator"]),
        )
    },
    {
        # decades e.g. "e.g. Um 1850er"
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{decade}})er(\sJahre)?(\s?{{suffix}})?\b".format(
            prefix = oneofp(patterns["de"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            decade = r"\b[1-9]\d{1,2}0",
            suffix = oneofp(patterns["de"]["datesuffix"])
        )
    },
    {
        # from decade to decade e.g. e.g. "1850er bis 1890er"
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{decade1}}){{separator}}({{prefix}}{{spaceordash}}?)*({{decade2}})(\s?{{suffix}})?\b".format(
            prefix = oneofp(patterns["de"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            decade1 = r"\b[1-9]\d{1,2}0er",
            decade2 = r"\b[1-9]\d{1,2}0er",
            separator = oneofp(patterns["de"]["dateseparator"]),
            suffix = oneofp(patterns["de"]["datesuffix"])
        )
    },
    {
        # Ordinal centuries e.g. "5. Jahrhundert n.Chr" (5th century AD)
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{ordinal}}) (Jahrhunderts?|Jhs?\.?)(\s{{suffix}})?".format(
            prefix = oneofp(patterns["de"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            ordinal = oneofp(patterns["de"]["ordinals"]),
            suffix = oneofp(patterns["de"]["datesuffix"])
        )
    },
    {
        # Ordinal millennia e.g. "erste H??lfte des 6. Jahrtausends v. Chr." (first half of the 6th millennium BC)
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{ordinal}}) Jahrtausends?(\s{{suffix}})?".format(
            prefix = oneofp(patterns["de"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            ordinal = oneofp(patterns["de"]["ordinals"]),
            suffix = oneofp(patterns["de"]["datesuffix"])
        )
    },
    {
        # from ordinal millennium to ordinal millennium  "7. bis 6. Jahrtausend v. Chr."
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{fromMill}})(\s?{{suffix}})?{{separator}}({{prefix}}{{spaceordash}}?)*({{toMill}})(\s?{{suffix}})?\b".format(
            prefix = oneofp(patterns["de"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            fromMill = oneofp(patterns["de"]["ordinals"]),
            separator = oneofp(patterns["de"]["dateseparator"]),
            toMill = oneofp(patterns["de"]["ordinals"]),
            suffix = oneofp(patterns["de"]["datesuffix"])
        )
    }
]

patterns["de"]["directions"] = [
    {"value": enums.Direction.N, "pattern": r"Norden"}, 
    {"value": enums.Direction.NE, "pattern": r"Nordosten"},
    {"value": enums.Direction.E, "pattern": r"Osten"},
    {"value": enums.Direction.SE, "pattern": r"S??d-Ost"}, 
    {"value": enums.Direction.S, "pattern": r"S??den"}, 
    {"value": enums.Direction.SW, "pattern": fr"S??dwesten"}, 
    {"value": enums.Direction.W, "pattern": r"Westen"}, 
    {"value": enums.Direction.NW, "pattern": fr"Nordwest"}
]

# English language patterns
patterns["en"]["cardinals"] = [
    {"value": 1, "pattern": r"(?:1|one)"},
    {"value": 2, "pattern": r"(?:2|two)"},
    {"value": 3, "pattern": r"(?:3|three)"},
    {"value": 4, "pattern": r"(?:4|four)"},
    {"value": 5, "pattern": r"(?:5|five)"},
    {"value": 6, "pattern": r"(?:6|six)"},
    {"value": 7, "pattern": r"(?:7|seven)"},
    {"value": 8, "pattern": r"(?:8|eight)"},
    {"value": 9, "pattern": r"(?:9|nine)"},
    {"value": 10, "pattern": r"(?:10|ten)"},
    {"value": 11, "pattern": r"(?:11|eleven)"},
    {"value": 12, "pattern": r"(?:12|twelve)"},
    {"value": 13, "pattern": r"(?:13|thirteen)"},
    {"value": 14, "pattern": r"(?:14|fourteen)"},
    {"value": 15, "pattern": r"(?:15|fifteen)"},
    {"value": 16, "pattern": r"(?:16|sixteen)"},
    {"value": 17, "pattern": r"(?:17|seventeen)"},
    {"value": 18, "pattern": r"(?:18|eighteen)"},
    {"value": 19, "pattern": r"(?:19|nineteen)"},
    {"value": 20, "pattern": r"(?:20|twenty)"},
    {"value": 21, "pattern": fr"(?:21|twenty{SPACEORDASH}one)"},
    {"value": 22, "pattern": fr"(?:22|twenty{SPACEORDASH}two)"},
    {"value": 23, "pattern": fr"(?:23|twenty{SPACEORDASH}three)"},
    {"value": 24, "pattern": fr"(?:24|twenty{SPACEORDASH}four)"},
    {"value": 25, "pattern": fr"(?:25|twenty{SPACEORDASH}five)"},
    {"value": 26, "pattern": fr"(?:26|twenty{SPACEORDASH}six)"},
    {"value": 27, "pattern": fr"(?:27|twenty{SPACEORDASH}seven)"},
    {"value": 28, "pattern": fr"(?:28|twenty{SPACEORDASH}eight)"},
    {"value": 29, "pattern": fr"(?:29|twenty{SPACEORDASH}nine)"},
    {"value": 30, "pattern": r"(?:30|thirty)"},
    {"value": 31, "pattern": fr"(?:31|thirty{SPACEORDASH}one)"}
]

patterns["en"]["ordinals"] = [
    {"value": 1, "pattern": r"(?:1|fir)st"},                         # 1st, first
    {"value": 2, "pattern": r"(?:2|seco)nd"},                        # 2nd, second
    {"value": 3, "pattern": r"(?:3|thi)rd"},                         # 3rd, third
    {"value": 4, "pattern": r"(?:4|four)th"},                        # 4th, fourth
    {"value": 5, "pattern": r"(?:5|fif)th"},                         # 5th, fifth
    {"value": 6, "pattern": r"(?:6|six)th"},                         # 6th, sixth
    {"value": 7, "pattern": r"(?:7|seven)th"},                       # 7th, seventh
    {"value": 8, "pattern": r"(?:8|eigh)th"},                        # 8th, eighth
    {"value": 9, "pattern": r"(?:9|nin)th"},                         # 9th, ninth
    {"value": 10, "pattern": r"(?:10|ten)th"},                       # 10th, tenth
    {"value": 11, "pattern": r"(?:11|eleven)th"},                    # 11th, eleventh
    {"value": 12, "pattern": r"(?:12|twelf)th"},                     # 12th, twelfth
    {"value": 13, "pattern": r"(?:13|thirteen)th"},                  # 13th, thirteenth
    {"value": 14, "pattern": r"(?:14|fourteen)th"},                  # 14th, fourteenth
    {"value": 15, "pattern": r"(?:15|fifteen)th"},                   # 15th, fifteenth
    {"value": 16, "pattern": r"(?:16|sixteen)th"},                   # 16th, sixteenth
    {"value": 17, "pattern": r"(?:17|seventeen)th"},                 # 17th, seventeenth
    {"value": 18, "pattern": r"(?:18|eighteen)th"},                  # 18th, eighteenth
    {"value": 19, "pattern": r"(?:19|nineteen)th"},                  # 19th, nineteenth
    {"value": 20, "pattern": r"(?:20|twentie)th"},                   # 20th, twentieth
    {"value": 21, "pattern": fr"(?:21|twenty{SPACEORDASH}fir)st"},    # 21st, twenty first
    {"value": 22, "pattern": fr"(?:22|twenty{SPACEORDASH}seco)nd"},   # 22nd, twenty second
    {"value": 23, "pattern": fr"(?:23|twenty{SPACEORDASH}thi)rd"},    # 23rd, twenty third
    {"value": 24, "pattern": fr"(?:24|twenty{SPACEORDASH}four)th"},   # 24th, twenty fourth
    {"value": 25, "pattern": fr"(?:25|twenty{SPACEORDASH}fif)th"},    # 25th, twenty fifth
    {"value": 26, "pattern": fr"(?:26|twenty{SPACEORDASH}six)th"},    # 26th, twenty sixth
    {"value": 27, "pattern": fr"(?:27|twenty{SPACEORDASH}seven)th"},  # 27th, twenty seventh
    {"value": 28, "pattern": fr"(?:28|twenty{SPACEORDASH}eigh)th"},   # 28th, twenty eighth
    {"value": 29, "pattern": fr"(?:29|twenty{SPACEORDASH}nin)th"},    # 29th, twenty ninth
    {"value": 30, "pattern": fr"(?:30|thirtie)th"},                   # 30th, thirtieth
    {"value": 31, "pattern": fr"(?:31|thirty{SPACEORDASH}fir)st" }    # 31st, thirty first
]

patterns["en"]["daynames"] = [
    {"value": enums.Day.MON, "pattern": r"Mon(?:\.|day)?"},                 # Mon, Mon., Monday
    {"value": enums.Day.TUE, "pattern": r"Tue(?:\.|s\.?|sday)?"},           # Tue, Tue., Tues, Tues., Tuesday
    {"value": enums.Day.WED, "pattern": r"Wed(?:\.|nesday)?"},              # Wed, Wed., Wednesday
    {"value": enums.Day.THU, "pattern": r"Thu(?:\.|rs?\.?|sday)?"},         # Thu, Thu., Thur, Thur., Thurs, Thursday
    {"value": enums.Day.FRI, "pattern": r"Fri(?:\.|day)?"},                 # Fri, Fri., Friday
    {"value": enums.Day.SAT, "pattern": r"Sat(?:\.|urday)?"},               # Sat, Sat., Saturday
    {"value": enums.Day.SUN, "pattern": r"Sun(?:\.|day)?"}                  # Sun, Sun., Sunday
]

patterns["en"]["monthnames"] = [
    {"value": enums.Month.JAN, "pattern": r"Jan(?:\.|uary)?"},            # Jan, Jan., January
    {"value": enums.Month.FEB, "pattern": r"Feb(?:\.|ruary)?"},           # Feb, Feb., February
    {"value": enums.Month.MAR, "pattern": r"Mar(?:\.|ch)?"},              # Mar, Mar., March
    {"value": enums.Month.APR, "pattern": r"Apr(?:\.|il)?"},              # Apr, Apr., April
    {"value": enums.Month.MAY, "pattern": r"May"},                      # May
    {"value": enums.Month.JUN, "pattern": r"Jun[\.e]?"},                # Jun, Jun., June
    {"value": enums.Month.JUL, "pattern": r"Jul[\.y]?"},                # Jul, Jul., July
    {"value": enums.Month.AUG, "pattern": r"Aug(?:\.|ust)?"},             # Aug, Aug., August
    {"value": enums.Month.SEP, "pattern": r"Sep(?:t?\.?|tember)?"},        # Sep, Sep., Sept, Sept., September
    {"value": enums.Month.OCT, "pattern": r"Oct(?:\.|ober)?"},            # Oct, Oct., October
    {"value": enums.Month.NOV, "pattern": r"Nov(?:\.|ember)?"},           # Nov, Nov., November
    {"value": enums.Month.DEC, "pattern": r"Dec(?:\.|ember)?"}            # Dec, Dec., December
]

patterns["en"]["seasonnames"] = [
    {"value": enums.Season.SPRING, "pattern": r"Spring(?:time)?"},        # Spring
    {"value": enums.Season.SUMMER, "pattern": r"Summer(?:time)?"},        # Summer
    {"value": enums.Season.AUTUMN, "pattern": r"(?:Autumn|Fall)"},        # Autumn
    {"value": enums.Season.WINTER, "pattern": r"Winter(?:time)?"}         # Winter
]

patterns["en"]["dateprefix"] =  [
    {"value": enums.DatePrefix.CIRCA, "pattern": r"(?:circa|ca?\.|???)"},
    {"value": enums.DatePrefix.CIRCA, "pattern": r"around"},
    {"value": enums.DatePrefix.CIRCA, "pattern": r"about"},
    {"value": enums.DatePrefix.CIRCA, "pattern": r"approx(?:\.|imately)?"},
    {"value": enums.DatePrefix.EARLY, "pattern": r"early"},
    {"value": enums.DatePrefix.EARLYMID, "pattern": fr"early{SPACEORDASH}mid(?:dle)?"},
    {"value": enums.DatePrefix.MID, "pattern": r"mid(?:dle)?"},
    {"value": enums.DatePrefix.MIDLATE, "pattern": fr"mid(?:dle)?{SPACEORDASH}later?"},
    {"value": enums.DatePrefix.LATE, "pattern": r"later?"},
    {"value": enums.DatePrefix.HALF1, "pattern": r"(?:1|fir)st half(?:\sof)?"},
    {"value": enums.DatePrefix.HALF2, "pattern": r"(?:2|seco)nd half(?:\sof)?"},
    {"value": enums.DatePrefix.QUARTER1, "pattern": r"(?:1|fir)st quarter(?:\sof)?"},
    {"value": enums.DatePrefix.QUARTER2, "pattern": r"(?:2|seco)nd quarter(?:\sof)?"},
    {"value": enums.DatePrefix.QUARTER3, "pattern": r"(?:3|thi)rd quarter(?:\sof)?"},
    {"value": enums.DatePrefix.QUARTER4, "pattern": r"(?:(?:4|four)th|last) quarter(?:\sof)?"},
    {"pattern": r"(?:beginning|start|end) of(?:\sthe)?"},
    {"pattern": r"(?:from|until)(?:\sthe)?"},
    {"pattern": r"(?:before|pre|prior to)(?:\sthe)?"},
    {"pattern": r"(?:in|during)(?:\sthe)?"},
    {"pattern": r"(?:post|after|since)(?:\sthe)?"}
]

patterns["en"]["datesuffix"] = [
    {"value": enums.DateSuffix.AD, "pattern": r"(?:A\.?D\.?|C\.?E\.?)"},
    {"value": enums.DateSuffix.BC, "pattern": r"(?:cal\.?\s)?B\.?C\.?(?:E\.?)?"},
    {"value": enums.DateSuffix.BP, "pattern": r"B\.?P\.?"}
]
 
patterns["en"]["dateseparator"] = [
    {"pattern": r"\s?\p{Pd}\s?"},
    {"pattern": r"\s?/\s?"},
    {"pattern": r"\sto\s"},
    {"pattern": r"\sor\s"},
    {"pattern": r"\sand\s"},
    {"pattern": r"\suntil\s"}     
]

patterns["en"]["periodnames"] = [
    {"pattern": r"pala?eolithic\b", "value": YearSpan(500000, -10000)},
    {"pattern": r"lower pala?eolithic\b", "value": YearSpan(500000, -150000)},
    {"pattern": r"middle pala?eolithic\b", "value": YearSpan(150000, -40000)},
    {"pattern": r"upper pala?eolithic\b", "value": YearSpan(40000, -10000)},
    {"pattern": r"mesolithic\b", "value": YearSpan(10000, -4000)},
    {"pattern": r"early mesolithic\b", "value": YearSpan(10000, -7000)},
    {"pattern": r"late mesolithic\b", "value": YearSpan(7000, -4000)},
    {"pattern": r"early prehistoric\b", "value": YearSpan(500000, -4000)},
    {"pattern": r"neolithic\b", "value": YearSpan(4000, -2200)},
    {"pattern": r"early neolithic\b", "value": YearSpan(4000, -3300)},
    {"pattern": r"middle neolithic\b", "value": YearSpan(3300, -2900)},
    {"pattern": r"late neolithic\b", "value": YearSpan(2900, -2200)},
    {"pattern": r"bronze age\b", "value": YearSpan(2600, -700)},
    {"pattern": r"early bronze age\b", "value": YearSpan(2600, -1600)},
    {"pattern": r"middle bronze age\b", "value": YearSpan(1600, -1200)},
    {"pattern": r"late bronze age\b", "value": YearSpan(1200, -700)},
    {"pattern": r"iron age\b", "value": YearSpan(800, 43)},
    {"pattern": r"early iron age\b", "value": YearSpan(800, -300)},
    {"pattern": r"middle iron age\b", "value": YearSpan(300, -100)},
    {"pattern": r"late iron age\b", "value": YearSpan(100, 43)},
    {"pattern": r"later? prehistoric\b", "value": YearSpan(4000, 43)},
    {"pattern": r"prehistoric\b", "value": YearSpan(500000, 43)},
    {"pattern": r"roman\b", "value": YearSpan(43, 410)},
    {"pattern": r"earl(?:y|ier) roman\b"},              # not in eh_periods, but occurs in archaeological texts
    {"pattern": r"later? roman\b"},                     # not in eh_periods, but occurs in archaeological texts
    {"pattern": fr"romano{SPACEORDASH}british\b"},      # not in eh_periods, but occurs in archaeological texts
    {"pattern": fr"(?:anglo{SPACEORDASH})?saxon\b"},    # not in eh_periods, but occurs in archaeological texts
    {"pattern": fr"(?:saxo{SPACEORDASH})?norman\b"},    # not in eh_periods, but occurs in archaeological texts
    {"pattern": r"later? media?eval\b"},                # not in eh_periods, but occurs in archaeological texts
    {"pattern": r"modern era\b"},                       # not in eh_periods, but occurs in archaeological texts
    {"pattern": r"stone age\b"},                        # not in eh_periods, but occurs in archaeological texts
    {"pattern": r"chalcolithic\b"},                     # not in eh_periods, but occurs in archaeological texts
    {"pattern": r"early media?eval\b(?:\speriod)?", "value": YearSpan(410, 1066)},
    {"pattern": r"media?eval\b(?:\speriod)?", "value": YearSpan(1066, 1540)},
    {"pattern": fr"post{SPACEORDASH}media?eval\b(?:\speriod)?", "value": YearSpan(1540, 1901)},
    {"pattern": r"tudor\b", "value": YearSpan(1485, 1603)},
    {"pattern": r"elizabethan\b", "value": YearSpan(1558, 1603)},
    {"pattern": r"stuart", "value": YearSpan(1603, 1714)},
    {"pattern": r"jacobean\b", "value": YearSpan(1603, 1625)},
    {"pattern": r"hanoverian\b", "value": YearSpan(1714, 1837)},
    {"pattern": r"georgian\b", "value": YearSpan(1714, 1837)},
    {"pattern": r"victorian\b", "value": YearSpan(1837, 1901)},
    {"pattern": r"20th century\b", "value": YearSpan(1901, 2000)},
    {"pattern": r"early 20th century\b", "value": YearSpan(1901, 1932)},
    {"pattern": r"edwardian\b", "value": YearSpan(1902, 1910)},
    {"pattern": r"(?:first world war|world war I|WW\s?I)\b", "value": YearSpan(1914, 1918)},
    {"pattern": fr"(?:inter{SPACEORDASH}war)\b", "value": YearSpan(1919, 1938)}, # added to accommodate ReMatch ADS CBA DOB records
    {"pattern": r"mid 20th century\b", "value": YearSpan(1933, 1966)},
    {"pattern": r"(?:second world war|world war II|WW\s?II)\b", "value": YearSpan(1939, 1945)},
    {"pattern": r"late 20th century\b", "value": YearSpan(1967, 2000)},
    {"pattern": r"21st century\b", "value": YearSpan(2001, 2100)}
]

# experimental only - not connected to datespan work
# chemical element names - not actually used yet
# list derived from https:#www.lenntech.com"periodic"symbol"symbol.htm
# todo - unique values - enum chemical element number?
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
patterns["en"]["activities"] = [
    {"pattern": r"additions?"},                 # addition, additions
    {"pattern": r"alter(?:ing|ed|ations?)"},    # altering, altered, alteration, alterations
    {"pattern": r"conver(?:ting|ted|sions?)"},  # converting, converted, conversion, conversions
    {"pattern": r"complet(?:ing|ed|ion)"},      # completing, completed, completion
    {"pattern": r"damag(?:ing|ed?)"},           # damaging, damage, damaged
    {"pattern": r"demoli(?:shing|shed|tion)"},  # demolishing, demolished, demolition
    {"pattern": r"modifi(?:ed|cations?)"},      # modified, modification, modifications
    {"pattern": r"rebuil(?:ding|t)"},           # rebuilding, rebuilt
    {"pattern": r"repair(?:ing|s|ed)"},         # repairing, repairs, repaired
    {"pattern": r"replac(?:ed|ement|ing)"},     # replaced, replacement, replacing
    {"pattern": r"refur[bn]ish(?:ing|ed)"},     # refurbished, refurbishing, refurnished, refurnishing
    {"pattern": r"remodell(?:ed|ing)"},         # remodelled, remodelling
    {"pattern": r"renew(?:ing|ed|al)"},         # renewing, renewed, renewal
    {"pattern": r"renovat(?:ing|ed|ions?)"}     # renovating, renovated, renovation, renovations
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
patterns["es"]["cardinals"] = [
    {"value": 1, "pattern": r"(?:1|I|un[oa]?)"},
    {"value": 2, "pattern": r"(?:2|II|dos)"},
    {"value": 3, "pattern": r"(?:3|III|tres)"},
    {"value": 4, "pattern": r"(?:4|IV|cuatro)"},
    {"value": 5, "pattern": r"(?:5|V|cinco)"},
    {"value": 6, "pattern": r"(?:6|VI|seis)"},
    {"value": 7, "pattern": r"(?:7|VII|siete)"},
    {"value": 8, "pattern": r"(?:8|VIII|ocho)"},
    {"value": 9, "pattern": r"(?:9|IX|nueve)"},
    {"value": 10, "pattern": r"(?:10|X|diez)"},
    {"value": 11, "pattern": r"(?:11|XI|once)"},
    {"value": 12, "pattern": r"(?:12|XII|doce)"},
    {"value": 13, "pattern": r"(?:13|XIII|trece)"},
    {"value": 14, "pattern": r"(?:14|XIV|catorce)"},
    {"value": 15, "pattern": r"(?:15|XV|quince)"},
    {"value": 16, "pattern": r"(?:16|XVI|diecis??is)"},
    {"value": 17, "pattern": r"(?:17|XVII|diecisiete)"},
    {"value": 18, "pattern": r"(?:18|XVIII|dieciocho)"},
    {"value": 19, "pattern": r"(?:19|XIX|diecinueve)"},
    {"value": 20, "pattern": r"(?:20|XX|veinte)"},
    {"value": 21, "pattern": r"(?:21|XXI|veintiuno)"},
    {"value": 22, "pattern": r"(?:22|XXII|veintid??s)"},
    {"value": 23, "pattern": r"(?:23|XXIII|veintitres)"},
    {"value": 24, "pattern": r"(?:24|XXIV|veinticuatro)"},
    {"value": 25, "pattern": r"(?:25|XXV|veinticinco)"},
    {"value": 26, "pattern": r"(?:26|XXVI|veintiseis)"},
    {"value": 27, "pattern": r"(?:27|XXVII|veintisiete)"},
    {"value": 28, "pattern": r"(?:28|XXVIII|veintiocho)"},
    {"value": 29, "pattern": r"(?:29|XXIX|veintinueve)"},
    {"value": 30, "pattern": r"(?:30|XXX|treinta)"},
    {"value": 31, "pattern": r"(?:31|XXXI|treinta y uno)"}
]

patterns["es"]["ordinals"] = [
    {"value": 1, "pattern": r"(?:1\s???|I|primer[oa]?)"},                  # first
    {"value": 2, "pattern": r"(?:2\s???|II|2do|segund[oa])"},             # second
    {"value": 3, "pattern": r"(?:3\s???|III|3ro|tercer[oa]?)"},            # third
    {"value": 4, "pattern": r"(?:4\s???|IV|4to|cuart[oa])"},              # fourth
    {"value": 5, "pattern": r"(?:5\s???|V|5to|quint[oa])"},              # fifth
    {"value": 6, "pattern": r"(?:6\s???|VI|6to|sext[oa])"},               # sixth
    {"value": 7, "pattern": r"(?:7\s???|VII|7mo|s??ptim[oa])"},             # seventh
    {"value": 8, "pattern": r"(?:8\s???|VIII|8vo|octav[oa])"},              # eighth
    {"value": 9, "pattern": r"(?:9\s???|IX|9no|noven[oa])"},              # ninth
    {"value": 10, "pattern": r"(?:10\s???|X|10mo|d??cim[oa])"},             # tenth
    {"value": 11, "pattern": r"(?:11\s???|XI|11mo|und??cim[oa])"},           # eleventh
    {"value": 12, "pattern": r"(?:12\s???|XII|12mo|duod??cim[oa])"},          # twelfth
    {"value": 13, "pattern": r"(?:13\s???|XIII|13ro|decimotercer[oa])"},      # thirteenth
    {"value": 14, "pattern": r"(?:14\s???|XIV|14to|decimocuart[oa])"},       # fourteenth
    {"value": 15, "pattern": r"(?:15\s???|XV|15to|decimoquint[oa])"},       # fifteenth
    {"value": 16, "pattern": r"(?:16\s???|XVI|16to|decimosext[oa])"},        # sixteenth
    {"value": 17, "pattern": r"(?:17\s???|XVII|17mo|decimos??ptim[oa])"},      # seventeenth
    {"value": 18, "pattern": r"(?:18\s???|XVIII|18vo|decimoctav[oa])"},        # eighteenth
    {"value": 19, "pattern": r"(?:19\s???|XIX|19no|decimonoven[oa])"},       # nineteenth
    {"value": 20, "pattern": r"(?:20\s???|XX|20mo|vig??sim[oa])"},           # twentieth
    {"value": 21, "pattern": r"(?:21\s???|XXI|21ro|vig??simoprimer[oa])"},    # twenty first
    {"value": 22, "pattern": r"(?:22\s???|XXII|22do|vig??simosegund[oa])"},    # twenty second
    {"value": 23, "pattern": r"(?:23\s???|XXIII|23ro|vig??simotercer[oa])"},    # twenty third
    {"value": 24, "pattern": r"(?:24\s???|XXIV|24to|vig??simocuart[oa])"},     # twenty fourth
    {"value": 25, "pattern": r"(?:25\s???|XXV|25to|vig??simoquint[oa])"},     # twenty fifth
    {"value": 26, "pattern": r"(?:26\s???|XXVI|26to|vig??simosext[oa])"},      # twenty sixth
    {"value": 27, "pattern": r"(?:27\s???|XXVII|27mo|vig??simos??ptim[oa])"},    # twenty seventh
    {"value": 28, "pattern": r"(?:28\s???|XXVIII|28vo|vig??simooctav[oa])"},     # twenty eighth
    {"value": 29, "pattern": r"(?:29\s???|XXIX|29no|vig??simonoven[oa])"},     # twenty ninth
    {"value": 30, "pattern": r"(?:30\s???|XXX|30mo|trig??sim[oa])"},          # thirtieth
    {"value": 31, "pattern": r"(?:31\s???|XXXI|31ro|trig??simoprimer[oa])"}    # thirty first
]

patterns["es"]["daynames"] = [
    {"value": enums.Day.MON, "pattern": r"(?:L|Lun|lunes)\b"},      # Monday
    {"value": enums.Day.TUE, "pattern": r"(?:M|Mar|martes)\b"},     # Tuesday
    {"value": enums.Day.WED, "pattern": r"(?:X|Mie|mi??rcoles)\b"},  # Wednesday
    {"value": enums.Day.THU, "pattern": r"(?:J|Jue|jueves)\b"},     # Thursday
    {"value": enums.Day.FRI, "pattern": r"(?:V|Vie|viernes)\b"},    # Friday
    {"value": enums.Day.SAT, "pattern": r"(?:S|S??b|s??bado)\b"},     # Saturday
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
    {"value": enums.Month.SEP, "pattern": r"Sept(?:\.|iembre)?"}, # September
    {"value": enums.Month.OCT, "pattern": r"Oct(?:\.|ubre)?"},    # October
    {"value": enums.Month.NOV, "pattern": r"Nov(?:\.|iembre)?"},  # November
    {"value": enums.Month.DEC, "pattern": r"Dic(?:\.|iembre)?"}   # December
]

patterns["es"]["seasonnames"] = [
    {"value": enums.Season.SPRING, "pattern": r"Primavera"},    # Spring
    {"value": enums.Season.SUMMER, "pattern": r"Verano"},       # Summer
    {"value": enums.Season.AUTUMN, "pattern": r"Oto??o"},        # Autumn
    {"value": enums.Season.WINTER, "pattern": r"Invierno"}      # Winter
]

patterns["es"]["dateprefix"] = [
    {"value": enums.DatePrefix.CIRCA, "pattern": r"hacia"},
    {"value": enums.DatePrefix.CIRCA, "pattern": r"aprox(?:\.|imadamente)?"},
    {"value": enums.DatePrefix.CIRCA, "pattern": r"aproximadamente"},
    {"value": enums.DatePrefix.CIRCA, "pattern": r"Alrededor de(?:l a??o)?"},
    {"value": enums.DatePrefix.EARLY, "pattern": r"(?:principios|inicio) del?"}, # beginning of
    {"value": enums.DatePrefix.MID, "pattern": r"Mediados del?"},
    {"value": enums.DatePrefix.LATE, "pattern": r"Finales del?"}, # end of
    {"value": enums.DatePrefix.HALF1, "pattern": r"Primera mitad del?"},
    {"value": enums.DatePrefix.HALF2, "pattern": r"Segunda mitad del?"},
    {"value": enums.DatePrefix.QUARTER1, "pattern": r"Primer cuarto del?"},
    {"value": enums.DatePrefix.QUARTER2, "pattern": r"Segundo cuarto del?"},
    {"value": enums.DatePrefix.QUARTER3, "pattern": r"Tercer trimestre del?"},
    {"value": enums.DatePrefix.QUARTER4, "pattern": r"Cuarto cuarto del?"},
    {"pattern": r"de"},                       # from
    {"pattern": r"antes de"},                 # before
    {"pattern": r"durante"},                  # During
    {"pattern": r"(?:post|despu??s de|desde)"},  # post / after / since
    {"pattern": r"(?:hasta|para)"}              # until / by
]

patterns["es"]["datesuffix"] = [
    {"value": enums.DateSuffix.AD, "pattern": r"(?:d[.\s]?C\.?|A\.?D\.?|C\.?E\.?)"},
    {"value": enums.DateSuffix.BC, "pattern": r"(?:a[.\s]?C\.?|antes de Cristo|(?:cal\.?\s)?B\.?C\.?(?:E\.?)?)"},
    {"value": enums.DateSuffix.BP, "pattern": r"B\.?P\.?"}
]

patterns["es"]["dateseparator"] = [
    {"pattern": r"\s?(?:\p{Pd}|\/|hasta|a(?:\sla)?|y|o)\s?"} #,    
]

patterns["es"]["periodnames"] = [
    {"pattern": r"Paleol??tic[ao]", "value": YearSpan(528000, -50000)},
    {"pattern": r"Paleol??tic[ao] Inferior", "value": YearSpan(528000, -200000)},
    {"pattern": r"Paleol??tic[ao] Medi[ao]", "value": YearSpan(200000, -50000)},
    {"pattern": r"Paleol??tic[ao] Superior", "value": YearSpan(50000, -7000)},
    {"pattern": r"Epipaleol??tic[ao]", "value": YearSpan(7000, -4500)},
    {"pattern": r"neol??tic[ao]"},
    {"pattern": r"Neol??tic[ao] Antigu[ao]", "value": YearSpan(4500, -2300)},
    {"pattern": r"Neol??tic[ao] Antigu[ao]", "value": YearSpan(4500, -2700)},
    {"pattern": r"Neol??tic[ao] Final", "value": YearSpan(2700, -2300)},
    {"pattern": r"Edad del Bronce", "value": YearSpan(2300, -800)},
    {"pattern": r"Edad del Bronce Inicial", "value": YearSpan(2300, -1700)},
    {"pattern": r"Edad del Bronce Medi[ao]", "value": YearSpan(1700, -1200)},
    {"pattern": r"Edad del Bronce Final", "value": YearSpan(1200, -800)},
    {"pattern": r"Edad del Hierro", "value": YearSpan(1200, -50)},
    {"pattern": r"Primera Edad del Hierro", "value": YearSpan(800, -400)},
    {"pattern": r"Segunda Edad del Hierro", "value": YearSpan(400, -50)},
    {"pattern": r"Roman[ao]", "value": YearSpan(50, 400)},
    {"pattern": r"Alt[ao] Roman[ao]", "value": YearSpan(50, 200)},
    {"pattern": r"Baj[ao] Roman[ao]", "value": YearSpan(200, 400)},
    {"pattern": r"Edad Medi[ao]", "value": YearSpan(400, 1500)},
    {"pattern": r"Alta Edad Medi[ao]", "value": YearSpan(400, 700)},
    {"pattern": r"Edad Medi[ao] central", "value": YearSpan(700, 1200)},
    {"pattern": r"Baja Edad Medi[ao]", "value": YearSpan(1200, 1500)},
    {"pattern": r"Edad Modern[ao]", "value": YearSpan(1500, 1900)},
    {"pattern": r"Edad Contempor??ne[ao]", "value": YearSpan(1900, 1999)}
]

patterns["es"]["datespans"] = [
     {
        # Month and 4 digit year
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{month}}) ({{year}})(\s{{suffix}})?".format(
            prefix = oneofp(patterns["es"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            month = oneofp(patterns["es"]["monthnames"]),
            year =  NUMERICYEAR,
            suffix = oneofp(patterns["es"]["datesuffix"])
        )
    },
    {
        # Season and 4 digit year
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{season}}) ({{year}})(\s{{suffix}})?".format(
            prefix = oneofp(patterns["es"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            season = oneofp(patterns["es"]["seasonnames"]),
            year =  NUMERICYEAR,
            suffix = oneofp(patterns["es"]["datesuffix"])
        )
    },
    {
        # year with suffix e.g. "8100 BCE"
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{year}})(\s?{{suffix}})".format(
            prefix = oneofp(patterns["es"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            year =  NUMERICYEAR,
            suffix = oneofp(patterns["es"]["datesuffix"])
        )
    },
    {
        # year with prefix e.g. "circa 1854"
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)+({{year}})(\s?{{suffix}})?".format(
            prefix = oneofp(patterns["es"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            year =  NUMERICYEAR,
            suffix = oneofp(patterns["es"]["datesuffix"])
        )
    },
    {
        # from year to year
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{fromYear}})(\s?{{suffix}})?{{separator}}({{prefix}}{{spaceordash}}?)*({{toYear}})(\s?{{suffix}})?\b".format(
            prefix = oneofp(patterns["es"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            fromYear = NUMERICYEAR,
            separator = oneofp(patterns["es"]["dateseparator"]),
            toYear = NUMERICYEAR,
            suffix = oneofp(patterns["es"]["datesuffix"])
        )
    },
    {
        # named historical periods
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{named}})\b".format(
            prefix = oneofp(patterns["es"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            named = oneofp(patterns["es"]["periodnames"])
        )
    },
    {
        # from named to named historical periods
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{named1}}){{separator}}({{prefix}}{{spaceordash}}?)*({{named2}})".format(
            prefix = oneofp(patterns["es"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            named1 = oneofp(patterns["es"]["periodnames"]),
            separator = oneofp(patterns["es"]["dateseparator"]),
            named2 = oneofp(patterns["es"]["periodnames"]),
        )
    },
    {
        # Ordinal centuries e.g. "5to siglo"
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{ordinal}}) siglo(\s{{suffix}})?".format(
            prefix = oneofp(patterns["es"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            ordinal = oneofp(patterns["es"]["ordinals"]),
            suffix = oneofp(patterns["es"]["datesuffix"])
        )
    },
    {
        # decades e.g. "e.g. 1950's"
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{decade}})(\s{{suffix}})?\b".format(
            prefix = oneofp(patterns["es"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            decade = r"\b[1-9]\d{1,2}0'?s",
            suffix = oneofp(patterns["es"]["datesuffix"])
        )
    },
    {
        # from decade to decade e.g. e.g. "early 1920s to 1950s"
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{decade1}}){{separator}}({{prefix}}{{spaceordash}}?)*({{decade2}})(\s?{{suffix}})?\b".format(
            prefix = oneofp(patterns["es"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            decade1 = r"\b[1-9]\d{1,2}0'?s",
            decade2 = r"\b[1-9]\d{1,2}0'?s",
            separator = oneofp(patterns["es"]["dateseparator"]),
            suffix = oneofp(patterns["es"]["datesuffix"])
        )
    },
    {
        # Roman numeral centuries e.g. "siglo V dC" (5th century AD)
        "pattern": fr"({{prefix}}{{spaceordash}}?)*siglo [MDCLXVI]+(\s{{suffix}})?".format(
            prefix = oneofp(patterns["es"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            suffix = oneofp(patterns["es"]["datesuffix"])
        )
    },
    {
        # from century to century e.g. siglos XIX-XVII a. C.
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*siglos?\s({{fromCentury}})(\s{{suffix}})?{{separator}}({{prefix}}{{spaceordash}}?)*({{toCentury}})(\s?{{suffix}})?\b".format(
            prefix = oneofp(patterns["es"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            fromCentury = ROMAN,
            separator = oneofp(patterns["es"]["dateseparator"]),
            toCentury = ROMAN,
            suffix = oneofp(patterns["es"]["datesuffix"])
        )
    },
    {
        # Roman numeral millennia e.g. "X millennio a.C."
        "pattern": fr"({{prefix}}{{spaceordash}}?)*[MDCLXVI]+ milenio(\s{{suffix}})?".format(
            prefix = oneofp(patterns["es"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            suffix = oneofp(patterns["es"]["datesuffix"])
        )
    },
    {
        # Ordinal millennia e.g. "Primo millennio d.C."
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{ordinal}}) milenio(\s{{suffix}})?".format(
            prefix = oneofp(patterns["es"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            ordinal = oneofp(patterns["es"]["ordinals"]),
            suffix = oneofp(patterns["es"]["datesuffix"])
        )
    },
    {
        # dynasties e.g. "dinast??a XII"
        "pattern": fr"({{prefix}}{{spaceordash}}?)*dinast??a [MDCLXVI]+".format(
            prefix = oneofp(patterns["es"]["dateprefix"]),
            spaceordash = SPACEORDASH
        )
    }
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
patterns["fr"]["cardinals"] = [
    {"value": 0, "pattern": r"(?:0|z??ro)"},
    {"value": 1, "pattern": r"(?:1|une?)"},
    {"value": 2, "pattern": r"(?:2|deux)"},
    {"value": 3, "pattern": r"(?:3|trois)"},
    {"value": 4, "pattern": r"(?:4|quatre)"},
    {"value": 5, "pattern": r"(?:5|cinq)"},
    {"value": 6, "pattern": r"(?:6|six)"},
    {"value": 7, "pattern": r"(?:7|sept)"},
    {"value": 8, "pattern": r"(?:8|huit)"},
    {"value": 9, "pattern": r"(?:9|neuf)"},
    {"value": 10, "pattern": r"(?:10|dix)"},
    {"value": 11, "pattern": r"(?:11|onze)"},
    {"value": 12, "pattern": r"(?:12|douze)"},
    {"value": 13, "pattern": r"(?:13|treize)"},
    {"value": 14, "pattern": r"(?:14|quatorze)"},
    {"value": 15, "pattern": r"(?:15|quinze)"},
    {"value": 16, "pattern": r"(?:16|seize)"},
    {"value": 17, "pattern": fr"(?:17|dix{SPACEORDASH}sept)"},
    {"value": 18, "pattern": fr"(?:18|dix{SPACEORDASH}huit)"},
    {"value": 19, "pattern": fr"(?:19|dix{SPACEORDASH}neuf)"},
    {"value": 20, "pattern": r"(?:20|vingt)"},
    {"value": 21, "pattern": r"(?:21|vingt et un)"},
    {"value": 22, "pattern": fr"(?:22|vingt{SPACEORDASH}deux)"},
    {"value": 23, "pattern": fr"(?:23|vingt{SPACEORDASH}trois)"},
    {"value": 24, "pattern": fr"(?:24|vingt{SPACEORDASH}quatre)"},
    {"value": 25, "pattern": fr"(?:25|vingt{SPACEORDASH}cinq)"},
    {"value": 26, "pattern": fr"(?:26|vingt{SPACEORDASH}six)"},
    {"value": 27, "pattern": fr"(?:27|vingt{SPACEORDASH}sept)"},
    {"value": 28, "pattern": fr"(?:28|vingt{SPACEORDASH}huit)"},
    {"value": 29, "pattern": fr"(?:29|vingt{SPACEORDASH}neuf)"},
    {"value": 30, "pattern": r"(?:30|trente)"},
    {"value": 31, "pattern": fr"(?:31|trente et un)"}
]

patterns["fr"]["ordinals"] = [
    {"value": 0, "pattern": r"z??ro[i??]??me"},                                 # zeroth
    {"value": 1, "pattern": r"(?:(?:1|I)er?|premi(?:er|??re))"},              # first
    {"value": 2, "pattern": r"(?:(?:2|II)(?:e|??me)|deuxi??me|seconde?)"},     # second
    {"value": 3, "pattern": r"(?:(?:3|III)(?:e|??me)|troisi??me)"},            # third
    {"value": 4, "pattern": r"(?:(?:4|IV)(?:e|??me)|quatri??me)"},             # fourth
    {"value": 5, "pattern": r"(?:(?:5|V)(?:e|??me)|cinqui??me)"},              # fifth
    {"value": 6, "pattern": r"(?:(?:6|VI)(?:e|??me)|sixi??me)"},               # sixth
    {"value": 7, "pattern": r"(?:(?:7|VII)(?:e|??me)|septi??me)"},             # seventh
    {"value": 8, "pattern": r"(?:(?:8|VIII)(?:e|??me)|huiti??me)"},            # eighth
    {"value": 9, "pattern": r"(?:(?:9|IX)(?:e|??me)|neuvi??me)"},              # ninth
    {"value": 10, "pattern": r"(?:(?:10|X)(?:e|??me)|dixi??me)"},              # tenth
    {"value": 11, "pattern": r"(?:(?:11|XI)(?:e|??me)|onzi??me)"},             # eleventh
    {"value": 12, "pattern": r"(?:(?:12|XII)(?:e|??me)|douzi??me)"},           # twelfth
    {"value": 13, "pattern": r"(?:(?:13|XIII)(?:e|??me)|treizi??me)"},         # thirteenth
    {"value": 14, "pattern": r"(?:(?:14|XIV)(?:e|??me)|quatorzi??me)"},        # fourteenth
    {"value": 15, "pattern": r"(?:(?:15|XV)(?:e|??me)|quinzi??me)"},           # fifteenth
    {"value": 16, "pattern": r"(?:(?:16|XVI)(?:e|??me)|seizi??me)"},           # sixteenth
    {"value": 17, "pattern": fr"(?:(?:17|XVII)(?:e|??me)|dix{SPACEORDASH}septi??me)"},      # seventeenth
    {"value": 18, "pattern": fr"(?:(?:18|XVIII)(?:e|??me)|dix{SPACEORDASH}huiti??me)"},     # eighteenth
    {"value": 19, "pattern": fr"(?:(?:19|XIX)(?:e|??me)|dix{SPACEORDASH}neuvi??me)"},       # nineteenth
    {"value": 20, "pattern": r"(?:(?:20|XX)(?:e|??me)|vingti??me)"},                        # twentieth
    {"value": 21, "pattern": r"(?:(?:21|XXI)(?:e|??me)|vingt et uni??me)"},                 # twenty first
    {"value": 22, "pattern": fr"(?:(?:22|XXII)(?:e|??me)|vingt{SPACEORDASH}deuxi??me)"},    # twenty second
    {"value": 23, "pattern": fr"(?:(?:23|XXIII)(?:e|??me)|vingt{SPACEORDASH}troisi??me)"},  # twenty third
    {"value": 24, "pattern": fr"(?:(?:24|XXIV)(?:e|??me)|vingt{SPACEORDASH}quatri??me)"},   # twenty fourth
    {"value": 25, "pattern": fr"(?:(?:25|XXV)(?:e|??me)|vingt{SPACEORDASH}cinqui??me)"},    # twenty fifth
    {"value": 26, "pattern": fr"(?:(?:26|XXVI)(?:e|??me)|vingt{SPACEORDASH}sixi??me)"},     # twenty sixth
    {"value": 27, "pattern": fr"(?:(?:27|XXVII)(?:e|??me)|vingt{SPACEORDASH}septi??me)"},   # twenty seventh
    {"value": 28, "pattern": fr"(?:(?:28|XXVIII)(?:e|??me)|vingt{SPACEORDASH}huiti??me)"},  # twenty eighth
    {"value": 29, "pattern": fr"(?:(?:29|XXIX)(?:e|??me)|vingt{SPACEORDASH}neuvi??me)"},    # twenty ninth
    {"value": 30, "pattern": r"(?:(?:30|XXX)(?:e|??me)|trenti??me)"},                       # thirtieth
    {"value": 31, "pattern": r"(?:(?:31|XXXI)(?:e|??me)|trent et uni??me)"}                 # thirty first
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
    {"value": enums.Month.FEB, "pattern": r"F??vr(?:\.|ier)?"},    # February
    {"value": enums.Month.MAR, "pattern": r"Mars"},             # March
    {"value": enums.Month.APR, "pattern": r"Avr(?:\.|il)?"},      # April
    {"value": enums.Month.MAY, "pattern": r"Mai"},              # May
    {"value": enums.Month.JUN, "pattern": r"Juin"},             # June
    {"value": enums.Month.JUL, "pattern": r"Juill(?:\.|et)?"},    # July
    {"value": enums.Month.AUG, "pattern": r"Ao??t"},             # August
    {"value": enums.Month.SEP, "pattern": r"Sept(?:\.|embre)?"},  # September
    {"value": enums.Month.OCT, "pattern": r"Oct(?:\.|obre)?"},    # October
    {"value": enums.Month.NOV, "pattern": r"Nov(?:\.|embre)?"},   # November
    {"value": enums.Month.DEC, "pattern": r"D??c(?:\.|embre)?"}    # December
]

patterns["fr"]["seasonnames"] = [
    {"value": enums.Season.SPRING, "pattern": r"printemps"},    # Spring
    {"value": enums.Season.SUMMER, "pattern": r"??t??"},          # Summer
    {"value": enums.Season.AUTUMN, "pattern": r"automne"},      # Autumn
    {"value": enums.Season.WINTER, "pattern": r"hiver"}         # Winter
]

patterns["fr"]["dateprefix"] = [
    {"value": enums.DatePrefix.CIRCA, "pattern": r"environ"},
    {"value": enums.DatePrefix.CIRCA, "pattern": r"vers(?:\sle)?"},
    {"value": enums.DatePrefix.CIRCA, "pattern": r"circa"},
    {"value": enums.DatePrefix.EARLY, "pattern": r"(?:le\s)?(?:d??but(?:\sd[ue])?|ancien)"},
    {"value": enums.DatePrefix.MID, "pattern": r"(?:le\s)?(?:milieu d[ue]|moyen)"},
    {"value": enums.DatePrefix.LATE, "pattern": r"(?:la\s)?(fin(?:\sd[ue])?|r??cent)"},
    {"value": enums.DatePrefix.HALF1, "pattern": r"(?:Premi??re|1er?) moiti?? d[ue]"},
    {"value": enums.DatePrefix.HALF2, "pattern": r"(?:Deuxi??me|seconde?|2e) moiti?? d[ue]"},
    {"value": enums.DatePrefix.THIRD1, "pattern": r"(?:Premi??re|1er?) tiers d[ue]"},          # 1st third
    {"value": enums.DatePrefix.THIRD2, "pattern": r"(?:Deuxi??me|seconde?|2e) tiers d[ue]"},   # 2nd third
    {"value": enums.DatePrefix.THIRD3, "pattern": r"(?:troisi??me|dernier|3e) tiers d[ue]"},   # last third
    {"value": enums.DatePrefix.QUARTER1, "pattern": r"(?:Premi??re|1er?) quart d[ue]"},          # 1st quarter
    {"value": enums.DatePrefix.QUARTER2, "pattern": r"(?:Deuxi??me|seconde?|2e) quart d[ue]"},   # 2nd quarter
    {"value": enums.DatePrefix.QUARTER3, "pattern": r"(?:Troisi??me|3e) quart d[ue]"},           # 3rd quarter
    {"value": enums.DatePrefix.QUARTER4, "pattern": r"(?:Quatri??me|dernier|4e) quart d[ue]"},   # last quarter
    {"pattern": r"(?:avant|av\.|apr[e??]s|apr?\.|en|depuis)"} # pre, post, before, after, during " since
]

patterns["fr"]["datesuffix"] = [
    {
        "value": enums.DateSuffix.AD, 
        "pattern": oneof([
            r"apr(?:[e??]s|\.)?\s(?:J[??e]sus[-\s]Christ|J\.?[-\s]?C\.?)",
            r"J\.?C\.?",
            r"A\.?D\.?",
            r"C\.?E\.?"
        ])
    },    
    {
        "value": enums.DateSuffix.BC, 
        "pattern": oneof([
            r"av(?:ant|\.)?(?:\s(J[??e]sus[-\s]Christ|J\.?[-\s]?C\.?))?",
            r"(?:cal\.?\s)?B\.?C\.?(E\.?)?"
        ])
    },
    {"value": enums.DateSuffix.BP, "pattern": r"B\.?P\.?"}
]

patterns["fr"]["dateseparator"] = [
    {"pattern": r"\s?\p{Pd}\s?"},
    {"pattern": r"\s?/\s?"},
    {"pattern": r"\s??\s"},
    {"pattern": r"\sau\s"},
    {"pattern": r"\set\s"},
    {"pattern": r"\sou\s"}
]

patterns["fr"]["periodnames"] = [
    {"pattern": r"Pal??olithique inf??rieur", "value": YearSpan(800000, -300000)},        # Lower palaeolithic
    {"pattern": r"Pal??olithique moyen", "value": YearSpan(300000, -40000)},             # Middle palaeolithic
    {"pattern": r"Pal??olithique sup??rieur", "value": YearSpan(40000, -12500)},          # Upper palaeolithic
    {"pattern": r"??pipal??olithique", "value": YearSpan(12500, -9600)},                  # Epipalaeolithic
    {"pattern": r"Mesolithique", "value": YearSpan(9600, -5500)},                       # Mesolithic
    {"pattern": r"(?:(?:??poque|p??riode)\s)?N??olithique", "value": YearSpan(6000, -2100)},   # Neolithic
    {"pattern": r"N??olithique final"}, # patterns observed in text                      # Final Neolithic
    {"pattern": r"protohistorique"},
    {"pattern": fr"gallo{SPACEORDASH}romain[es]"},                                      # Gallo Roman
    {"pattern": r"??ge du Bronze"},                                                      # Bronze age
    {"pattern": r"??ge du Fer"},                                                         # Iron age
    {"pattern": r"La T??ne(?:\sfinale)?"},                                                 # The final dinner
    {"pattern": r"??ge du Bronze ancien", "value": YearSpan(2200, -1600)},               # ancient bronze age
    {"pattern": r"??ge du Bronze moyen", "value": YearSpan(1600, -1400)},                # middle bronze age
    {"pattern": r"??ge du Bronze final", "value": YearSpan(1400, -1800)},                # final bronze age
    {"pattern": r"premier ??ge du Fer", "value": YearSpan(800, -450)},                   # first iron age
    {"pattern": r"second ??ge du Fer", "value": YearSpan(450, -50)},                     # Second iron age
    {"pattern": fr"Haut{SPACEORDASH}Empire", "value": YearSpan(50, 300)},               # High Empire
    {"pattern": r"Antiquit?? tardive", "value": YearSpan(300, 500)},                     # Late antiquity
    {"pattern": r"Moyen [??A]ge", "value": YearSpan(400, 400)},                          # Middle ages
    {"pattern": r"haut Moyen [??A]ge", "value": YearSpan(400, 1000)},                    # High middle age
    {"pattern": r"Moyen [??A]ge classique", "value": YearSpan(1000, 1400)},              # Classical middle ages
    {"pattern": r"bas Moyen [??A]ge", "value": YearSpan(1400, 1600)},                    # Low middle ages
    {"pattern": r"(?:(?:??poque|p??riode)\s)?moderne", "value": YearSpan(1600, 1800)},        # Modern period
    {"pattern": r"Renaissance", "value": YearSpan(1500, 1600)},                         # Renaissance
    {"pattern": r"Si??cle des Lumi??res", "value": YearSpan(1600, 1800)},                 # Age of enlightenment
    {"pattern": r"(?:(?:??poque|p??riode)\s)?contemporaine", "value": YearSpan(1800, 2000)},  # Contemporary period
    {"pattern": r"minoen", "value": YearSpan()},                                        # Minoan
    {"pattern": r"minoen ancien", "value": YearSpan()},                                 # Ancient Minoan
    {"pattern": r"minoen moyen", "value": YearSpan()},                                  # Middle Minoan
    {"pattern": r"minoen r??cent", "value": YearSpan()},                                 # recent Minoan
    {"pattern": r"minoen r??cent I A", "value": YearSpan()},                             # recent Minoan I A
    {"pattern": r"minoen r??cent I B", "value": YearSpan()},                             # recent Minoan I B
    {"pattern": r"minoen r??cent II", "value": YearSpan()},                              # Recent Minoan II
    {"pattern": r"minoen r??cent III", "value": YearSpan()},                             # Minoan III
    {"pattern": r"subminoen", "value": YearSpan()},                                     # sub Minoan
    {"pattern": r"corinthien", "value": YearSpan()},                                    # Corinthian
    {"pattern": r"corinthien ancien", "value": YearSpan()},                             # ancient Corinthian
    {"pattern": r"corinthien moyen", "value": YearSpan()},                              # Middle Corinthian
    {"pattern": r"corinthien r??cent I", "value": YearSpan()},                           # recent Corinthan I                        
    {"pattern": r"corinthien r??cent II", "value": YearSpan()},                          # recent Corinthan II
    {"pattern": r"(?:(?:??poque|p??riode)\s)?archa??que", "value": YearSpan()},                # Archaic
    {"pattern": r"(?:(?:??poque|p??riode)\s)?georgienne", "value": YearSpan(1714, 1837)},     # Georgian
    {"pattern": r"(?:(?:??poque|p??riode)\s)?victorienne", "value": YearSpan(1837, 1901)},    # Victorian
    {"pattern": r"(?:(?:??poque|p??riode)\s)?hell??nistique", "value": YearSpan(323, -31)},    # Hellenistic
    {"pattern": fr"(?:(?:??poque|p??riode)\s)?julio{SPACEORDASH}claudienne", "value": YearSpan(27, 68)}, # Claudian
    {"pattern": r"(?:(?:??poque|p??riode)\s)?august??enne", "value": YearSpan(27, 14)},        # Augustan
    {"pattern": r"(?:(?:??poque|p??riode)\s)?tib??rienne", "value": YearSpan(14, 37)},         # Tiberian
    {"pattern": fr"(?:(?:??poque|p??riode)\s)?tib??ro{SPACEORDASH}claudienne", "value": YearSpan(14, 54)},
    {"pattern": r"(?:(?:??poque|p??riode)\s)?claudienne", "value": YearSpan(41, 54)},         # Claudian
    {"pattern": r"(?:(?:??poque|p??riode)\s)?n??ronienne", "value": YearSpan(54, 68)},         # Neronian
    {"pattern": r"(?:(?:??poque|p??riode)\s)?flavienne", "value": YearSpan(69, 96)},          # Flavian
    {"pattern": r"(?:(?:??poque|p??riode)\s)?de Vespasien", "value": YearSpan(69, 79)},       # Vespasian
    {"pattern": r"(?:(?:??poque|p??riode)\s)?de Domitien", "value": YearSpan(81, 96)},        # Domitian
    {"pattern": r"(?:(?:??poque|p??riode)\s)?de Trajan", "value": YearSpan(98, 117)},         # Trajan
    {"pattern": r"(?:(?:??poque|p??riode)\s)?d'Hadrien", "value": YearSpan(117, 138)},       # Hadrianic
    {"pattern": r"(?:(?:??poque|p??riode)\s)?antonine", "value": YearSpan(138, 161)},         # Antonine
    {"pattern": r"(?:(?:??poque|p??riode)\s)?aur??lienne", "value": YearSpan(161, 180)},       # Aurelian
    {"pattern": r"(?:(?:??poque|p??riode)\s)?s??v??rienne", "value": YearSpan(193, 211)},       # Severian
    {"pattern": r"(?:(?:??poque|p??riode)\s)?de Gallien", "value": YearSpan(253, 268)},       # Gallien
    {"pattern": r"(?:(?:??poque|p??riode)\s)?des T??trarques", "value": YearSpan(293, 364)},   # Tetrarchs
    {"pattern": r"(?:(?:??poque|p??riode)\s)?constantinienne", "value": YearSpan(305, 363)},  # Constantinian
    {"pattern": fr"(?:(?:??poque|p??riode)\s)?Bas{SPACEORDASH}Empire", "value": YearSpan(0, 0)},
    {"pattern": r"(?:(?:??poque|p??riode)\s)?byzantine", "value": YearSpan(0, 0)}
]

patterns["fr"]["datespans"] = [
    {
        # Month and year
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{month}}) ({{year}})(\s{{suffix}})?".format(
            prefix = oneofp(patterns["fr"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            month = oneofp(patterns["fr"]["monthnames"]),
            year =  NUMERICYEAR,
            suffix = oneofp(patterns["fr"]["datesuffix"])
        )
    },
    {
        # Season and year
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{season}}) ({{year}})(\s{{suffix}})?".format(
            prefix = oneofp(patterns["fr"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            season = oneofp(patterns["fr"]["seasonnames"]),
            year =  NUMERICYEAR,
            suffix = oneofp(patterns["fr"]["datesuffix"])
        )
    },
    {
        # year with suffix
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{year}})( ans)?(\s?{{suffix}})\b".format(
            prefix = oneofp(patterns["fr"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            year =  NUMERICYEAR,
            suffix = oneofp(patterns["fr"]["datesuffix"])
        )
    },
    {
        # year with prefix
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)+({{year}})( ans)?(\s?{{suffix}})?\b".format(
            prefix = oneofp(patterns["fr"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            year =  NUMERICYEAR,
            suffix = oneofp(patterns["fr"]["datesuffix"])
        )
    },
    {
        # from year to year
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{fromYear}})( ans)?(\s?{{suffix}})?{{separator}}({{prefix}}{{spaceordash}}?)*({{toYear}})(\s?{{suffix}})?\b".format(
            prefix = oneofp(patterns["fr"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            fromYear = NUMERICYEAR,
            separator = oneofp(patterns["fr"]["dateseparator"]),
            toYear = NUMERICYEAR,
            suffix = oneofp(patterns["fr"]["datesuffix"])
        )
    },
    {
        # named historical periods
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{named}})\b".format(
            prefix = oneofp(patterns["fr"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            named = oneofp(patterns["fr"]["periodnames"])
        )
    },
    {
        # from named to named historical periods
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{named1}}){{separator}}({{prefix}}{{spaceordash}}?)*({{named2}})".format(
            prefix = oneofp(patterns["fr"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            named1 = oneofp(patterns["fr"]["periodnames"]),
            separator = oneofp(patterns["fr"]["dateseparator"]),
            named2 = oneofp(patterns["fr"]["periodnames"])
        )
    },
    {
        # decades e.g. "1850's"
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{decade}})(\s?{{suffix}})?\b".format(
            prefix = oneofp(patterns["fr"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            decade = r"\b[1-9]\d{1,2}0'?s",
            suffix = oneofp(patterns["fr"]["datesuffix"])
        )
    },
    {
        # from decade to decade e.g. e.g. ""
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{decade1}}){{separator}}({{prefix}}{{spaceordash}}?)*({{decade2}})\b".format(
            prefix = oneofp(patterns["fr"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            decade1 = r"\b[1-9]\d{1,2}0'?s",
            decade2 = r"\b[1-9]\d{1,2}0'?s",
            separator = oneofp(patterns["fr"]["dateseparator"])
        )
    },
    {
        # Ordinal century e.g. "cinqui??me si??cle apr??s JC", "5th century AD"
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{ordinal}}) s(i??cle|\.)(\s{{suffix}})?\b".format(
            prefix = oneofp(patterns["fr"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            ordinal = oneofp(patterns["fr"]["ordinals"]),
            suffix = oneofp(patterns["fr"]["datesuffix"])
        )
    },
    {
        # From ordinal to ordinal century e.g. "le milieu du Ier si??cle et le d??but du IIe si??cle"
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{fromOrdinal}}) s(i??cle|\.){{separator}}({{prefix}}{{spaceordash}}?)*({{toOrdinal}}) s(i??cle|\.)(\s{{suffix}})?".format(
            prefix = oneofp(patterns["fr"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            fromOrdinal = oneofp(patterns["fr"]["ordinals"]),
            separator = oneofp(patterns["fr"]["dateseparator"]),
            toOrdinal = oneofp(patterns["fr"]["ordinals"]),
            suffix = oneofp(patterns["fr"]["datesuffix"])
        )
    },
    {
        # Ordinal millennium
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{ordinal}}) mill??naire(\s{{suffix}})?\b".format(
            prefix = oneofp(patterns["fr"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            ordinal = oneofp(patterns["fr"]["ordinals"]),
            suffix = oneofp(patterns["fr"]["datesuffix"])
        )
    },
    {
        # Roman numeral centuries e.g. "IIe s. av. J.-C." (2nd century BC)
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{roman}})er? s(i??cle|\.)(\s{{suffix}})?".format(
            prefix = oneofp(patterns["fr"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            roman =  ROMAN,
            suffix = oneofp(patterns["fr"]["datesuffix"])
        )
    },
    {
        # From Roman to Roman century e.g. "XIe-XIIIe si??cle"
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{fromRoman}})e{{separator}}({{prefix}}{{spaceordash}}?)*({{toRoman}})e s(i??cle|\.)(\s{{suffix}})?".format(
            prefix = oneofp(patterns["fr"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            fromRoman = ROMAN,
            separator = oneofp(patterns["fr"]["dateseparator"]),
            toRoman = ROMAN,
            suffix = oneofp(patterns["fr"]["datesuffix"])
        )
    }
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
patterns["it"]["cardinals"] = [
    {"value": 1, "pattern": r"(?:1|I|un[oa])"},
    {"value": 2, "pattern": r"(?:2|II|due)"},
    {"value": 3, "pattern": r"(?:3|III|tre)"},
    {"value": 4, "pattern": r"(?:4|IV|quattro)"},
    {"value": 5, "pattern": r"(?:5|V|cinque)"},
    {"value": 6, "pattern": r"(?:6|VI|sei)"},
    {"value": 7, "pattern": r"(?:7|VII|sette)"},
    {"value": 8, "pattern": r"(?:8|VIII|otto)"},
    {"value": 9, "pattern": r"(?:9|IX|nove)"},
    {"value": 10, "pattern": r"(?:10|X|dieci)"},
    {"value": 11, "pattern": r"(?:11|XI|undici)"},
    {"value": 12, "pattern": r"(?:12|XII|dodici)"},
    {"value": 13, "pattern": r"(?:13|XIII|tredici)"},
    {"value": 14, "pattern": r"(?:14|XIV|quattordici)"},
    {"value": 15, "pattern": r"(?:15|XV|quindici)"},
    {"value": 16, "pattern": r"(?:16|XVI|sedici)"},
    {"value": 17, "pattern": r"(?:17|XVII|diciassette)"},
    {"value": 18, "pattern": r"(?:18|XVIII|diciotto)"},
    {"value": 19, "pattern": r"(?:19|XIX|diciannove)"},
    {"value": 20, "pattern": r"(?:20|XX|venti)"},
    {"value": 21, "pattern": r"(?:21|XXI|ventuno)"},
    {"value": 22, "pattern": r"(?:22|XXII|ventidue)"},
    {"value": 23, "pattern": r"(?:23|XXIII|ventitr??)"},
    {"value": 24, "pattern": r"(?:24|XXIV|ventiquattro)"},
    {"value": 25, "pattern": r"(?:25|XXV|venticinque)"},
    {"value": 26, "pattern": r"(?:26|XXVI|ventisei)"},
    {"value": 27, "pattern": r"(?:27|XXVII|ventisette)"},
    {"value": 28, "pattern": r"(?:28|XXVIII|ventotto)"},
    {"value": 29, "pattern": r"(?:29|XXIX|ventinove)"},
    {"value": 30, "pattern": r"(?:30|XXX|trenta)"},
    {"value": 31, "pattern": r"(?:31|XXXI|quaranta)"}
]

patterns["it"]["ordinals"] = [
    {"value": 1, "pattern": r"(?:1\s?[????]|I|primo)"},             # first
    {"value": 2, "pattern": r"(?:2\s?[????]|II|secondo)"},           # second
    {"value": 3, "pattern": r"(?:3\s?[????]|III|terzo)"},             # third
    {"value": 4, "pattern": r"(?:4\s?[????]|IV|quarto)"},            # fourth
    {"value": 5, "pattern": r"(?:5\s?[????]|V|quinto)"},            # fifth
    {"value": 6, "pattern": r"(?:6\s?[????]|VI|sesto)"},             # sixth
    {"value": 7, "pattern": r"(?:7\s?[????]|VII|settimo)"},           # seventh
    {"value": 8, "pattern": r"(?:8\s?[????]|VIII|ottavo)"},            # eighth
    {"value": 9, "pattern": r"(?:9\s?[????]|IX|nono)"},              # ninth
    {"value": 10, "pattern": r"(?:10\s?[????]|X|decimo)"},           # tenth
    {"value": 11, "pattern": r"(?:11\s?[????]|XI|undicesimo)"},       # eleventh
    {"value": 12, "pattern": r"(?:12\s?[????]|XII|dodicesimo)"},       # twelfth
    {"value": 13, "pattern": r"(?:13\s?[????]|XIII|tredicesimo)"},      # thirteenth
    {"value": 14, "pattern": r"(?:14\s?[????]|XIV|quattordicesimo)"},  # fourteenth
    {"value": 15, "pattern": r"(?:15\s?[????]|XV|quindicesimo)"},     # fifteenth
    {"value": 16, "pattern": r"(?:16\s?[????]|XVI|sedicesimo)"},       # sixteenth
    {"value": 17, "pattern": r"(?:17\s?[????]|XVII|diciassettesimo)"},  # seventeenth
    {"value": 18, "pattern": r"(?:18\s?[????]|XVIII|diciottesimo)"},     # eighteenth
    {"value": 19, "pattern": r"(?:19\s?[????]|XIX|diciannovesimo)"},   # nineteenth
    {"value": 20, "pattern": r"(?:20\s?[????]|XX|ventesimo)"},        # twentieth
    {"value": 21, "pattern": r"(?:21\s?[????]|XXI|ventunesimo)"},      # twenty first
    {"value": 22, "pattern": r"(?:22\s?[????]|XXII|ventiduesima)"},     # twenty second
    {"value": 23, "pattern": r"(?:23\s?[????]|XXIII|ventitreesimo)"},    # twenty third
    {"value": 24, "pattern": r"(?:24\s?[????]|XXIV|ventiquattresimo)"}, # twenty fourth
    {"value": 25, "pattern": r"(?:25\s?[????]|XXV|venticinquesimo)"},  # twenty fifth
    {"value": 26, "pattern": r"(?:26\s?[????]|XXVI|ventiseiesimo)"},    # twenty sixth
    {"value": 27, "pattern": r"(?:27\s?[????]|XXVII|ventisettesimo)"},   # twenty seventh
    {"value": 28, "pattern": r"(?:28\s?[????]|XXVIII|ventotto)"},         # twenty eighth
    {"value": 29, "pattern": r"(?:29\s?[????]|XXIX|ventinovesimo)"},    # twenty ninth
    {"value": 30, "pattern": r"(?:30\s?[????]|XXX|trentesimo)"},       # thirtieth
    {"value": 31, "pattern": r"(?:31\s?[????]|XXXI|trentunesima)"}      # thirty first
]

patterns["it"]["daynames"] = [
    {"value": enums.Day.MON, "pattern": r"un(?:\.|ed??)?"},        # Monday
    {"value": enums.Day.TUE, "pattern": r"mar(?:\.|ted??)?"},      # Tuesday
    {"value": enums.Day.WED, "pattern": r"mer(?:\.|coled??)?"},    # Wednesday
    {"value": enums.Day.THU, "pattern": r"gio(?:\.|ved??)?"},      # Thursday
    {"value": enums.Day.FRI, "pattern": r"ven(?:\.|erd??)?"},      # Friday
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
    {"value": enums.DatePrefix.EARLY, "pattern": r"(?:inizio(?:\sdell?'?)?|Prima Et??|Prim[io])"},
    {"value": enums.DatePrefix.MID, "pattern": r"(?:Met?? del|Medio|Mezzo)"},
    {"value": enums.DatePrefix.LATE, "pattern": r"(?:Tarda Et??|fine(?:\sdell?'?)?|Fino al)"},
    {"value": enums.DatePrefix.HALF1, "pattern": r"(?:1\s?[????]|prima) met?? del"},
    {"value": enums.DatePrefix.HALF2, "pattern": r"(?:2\s?[????]|seconda) met?? del"},
    {"value": enums.DatePrefix.QUARTER1, "pattern": r"(?:1\s?[????]|primo) (?:quarto|trimestre)(\sdel)?"},
    {"value": enums.DatePrefix.QUARTER2, "pattern": r"(?:2\s?[????]|secondo) (?:quarto|trimestre)(\sdel)?"},
    {"value": enums.DatePrefix.QUARTER3, "pattern": r"(?:3\s?[????]|terzo) (?:quarto|trimestre)(\sdel)?"},
    {"value": enums.DatePrefix.QUARTER4, "pattern": r"(?:4\s?[????]|quarto|ultimo) (?:quarto|trimestre)(\sdel)?"},
    {"pattern": r"dal"},                      # from
    {"pattern": r"prima(?:\sdell?'?)?"},      # before
    {"pattern": r"nel"},                      # During
    {"pattern": r"(?:post|dopo il|dal)"},       # post " after " since
    {"pattern": r"(?:fino al|entro il)"}        # until " by
]

patterns["it"]["datesuffix"] = [
    {"value": enums.DateSuffix.AD, "pattern": r"(?:d\.?C\.?|C\.?E\.?)"},
    {"value": enums.DateSuffix.BC, "pattern": r"(?:a\.?C\.?|(?:cal\.?\s)?B\.?C\.?(?:E\.?)?)"},
    {"value": enums.DateSuffix.BP, "pattern": r"B\.?P\.?"}
]

patterns["it"]["dateseparator"] = [
    {"pattern": r"\s?\p{Pd}\s?"},
    {"pattern": r"\s?/\s?"},
    {"pattern": r"\sa\s"},
    {"pattern": r"\sall(?:a\s|')"},
    {"pattern": r"\sed?\slo\s"}         
]

patterns["it"]["periodnames"] = [
    {"pattern": r"Paleolitic[ao]", "value": YearSpan(600000, -10000)},              # Palaeolithic
    {"pattern": r"Paleolitic[ao] Inferiore", "value": YearSpan(600000, -150000)},   # Lower Palaeolithic
    {"pattern": r"Paleolitic[ao] Medio", "value": YearSpan(149999, -40000)},        # Middle Palaeolithic
    {"pattern": r"Paleolitic[ao] Superiore", "value": YearSpan(39999, -10000)},     # Upper Palaeolithic
    {"pattern": r"Mesolitic[ao]", "value": YearSpan(9999, -5000)},                  # Mesolithic
    {"pattern": r"Neolitic[ao]", "value": YearSpan(5000, -3300)},                   # Neolithic
    {"pattern": r"Eneolitic[ao]", "value": YearSpan(3300, -2300)},                  # Eneolithic                 
    {"pattern": r"Et?? del Bronzo", "value": YearSpan(2300, -1000)},                 # Bronze Age
    {"pattern": r"Antica Et?? del Bronzo"},                                          # Ancient Bronze Age
    {"pattern": r"Media Et?? del Bronzo"},                                           # Middle Bronze Age
    {"pattern": r"Tarda Et?? del Bronzo"},                                           # Late Bronze Age
    {"pattern": r"Et?? del Ferro", "value": YearSpan(1000, -750)},                   # Iron Age
    {"pattern": r"Orientalizzante", "value": YearSpan(750, -580)},
    {"pattern": r"Arcaic[ao]", "value": YearSpan(580, -480)},                          # Archaic
    {"pattern": r"Classic[ao]", "value": YearSpan(480, -350)},                      # Classic
    {"pattern": r"Roman[ao]", "value": YearSpan(350, 600)},                         # Roman
    {"pattern": r"Roman[ao] Repubblicano", "value": YearSpan(350, -27)},            # Roman Republican
    {"pattern": r"Roman[ao] Imperiale", "value": YearSpan(27, 400)},                # Roman Imperial
    {"pattern": r"Tard'antichit??", "value": YearSpan(400, 600)},                    # Late Antiquity
    {"pattern": r"Medievale", "value": YearSpan(600, 1350)},                        # Medieval
    {"pattern": r"Rinasciment[ao]", "value": YearSpan(1350, 1550)},                 # Renaissance
    {"pattern": r"Modern[ao]", "value": YearSpan(1550, 1788)},                      # Modern
    {"pattern": r"Contemporane[ao]", "value": YearSpan(1788, 2000)}                    # Contemporary
]

patterns["it"]["datespans"] = [
    {
        # Month and year
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{month}}) ({{year}})(\s{{suffix}})?".format(
            prefix = oneofp(patterns["it"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            month = oneofp(patterns["it"]["monthnames"]),
            year =  NUMERICYEAR,
            suffix = oneofp(patterns["it"]["datesuffix"])
        )
    },
    {
        # Season and year
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{season}}) ({{year}})(\s{{suffix}})?".format(
            prefix = oneofp(patterns["it"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            season = oneofp(patterns["it"]["seasonnames"]),
            year =  NUMERICYEAR,
            suffix = oneofp(patterns["it"]["datesuffix"])
        )
    },
    {
        # year with suffix e.g. "8100 BCE"
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{year}})(\s?{{suffix}})".format(
            prefix = oneofp(patterns["it"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            year =  NUMERICYEAR,
            suffix = oneofp(patterns["it"]["datesuffix"])
        )
    },
    {
        # year with prefix e.g. "circa 1854"
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)+({{year}})(\s?{{suffix}})?".format(
            prefix = oneofp(patterns["it"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            year =  NUMERICYEAR,
            suffix = oneofp(patterns["it"]["datesuffix"])
        )
    },
    {
        # from year to year
        "pattern": fr"\b(tra lo\s)?({{prefix}}{{spaceordash}}?)*({{fromYear}})(\s?{{suffix}})?{{separator}}({{prefix}}{{spaceordash}}?)*({{toYear}})(\s?{{suffix}})?\b".format(
            prefix = oneofp(patterns["it"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            fromYear = NUMERICYEAR,
            separator = oneofp(patterns["it"]["dateseparator"]),
            toYear = NUMERICYEAR,
            suffix = oneofp(patterns["it"]["datesuffix"])
        )
    },
    {
        # named historical periods
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{named}})\b".format(
            prefix = oneofp(patterns["it"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            named = oneofp(patterns["it"]["periodnames"])
        )
    },
    {
        # from named to named historical periods
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{named1}}){{separator}}({{prefix}}{{spaceordash}}?)*({{named2}})".format(
            prefix = oneofp(patterns["it"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            named1 = oneofp(patterns["it"]["periodnames"]),
            named2 = oneofp(patterns["it"]["periodnames"]),
            separator = oneofp(patterns["it"]["dateseparator"])
        )
    },
    {
        # decades e.g. "Intorno al decennio 1850esimo"
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*decennio\s({{decade}})(\s{{suffix}})?\b".format(
            prefix = oneofp(patterns["it"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            decade = r"\b[1-9]\d{1,2}0(esimo)?",
            suffix = oneofp(patterns["it"]["datesuffix"])
        )
    },
    {
        # from decade to decade e.g. e.g. ""
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{decade1}}){{separator}}({{prefix}}{{spaceordash}}?)*({{decade2}})\b".format(
            prefix = oneofp(patterns["it"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            decade1 = r"\b[1-9]\d{1,2}0(esimo)?",
            decade2 = r"\b[1-9]\d{1,2}0(esimo)?",
            separator = oneofp(patterns["it"]["dateseparator"]),
        )
    },
    {
        # Roman numeral centuries e.g. "V secolo d.C." (5th century AD)
        "pattern": fr"({{prefix}}{{spaceordash}}?)*{{roman}} sec(olo|\.)(\s{{suffix}})?".format(
            prefix = oneofp(patterns["it"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            roman = ROMAN,
            suffix = oneofp(patterns["it"]["datesuffix"])
        )
    },
    {
        # alt Roman numeral centuries e.g. "Sec. V d.C." (5th century AD)
        "pattern": fr"({{prefix}}{{spaceordash}}?)*sec(olo|\.) {{roman}}(\s{{suffix}})?".format(
            prefix = oneofp(patterns["it"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            roman = ROMAN,
            suffix = oneofp(patterns["it"]["datesuffix"])
        )
    },
    {
        # Ordinal centuries e.g. "18?? secolo"
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{ordinal}}) sec(olo|\.)(\s{{suffix}})?".format(
            prefix = oneofp(patterns["it"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            ordinal = oneofp(patterns["it"]["ordinals"]),
            suffix = oneofp(patterns["it"]["datesuffix"])
        )
    },
    {
        # Roman numeral millennia e.g. "X millennio a.C."
        "pattern": fr"({{prefix}}{{spaceordash}}?)*{{roman}} mill(ennio|\.)(\s{{suffix}})?".format(
            prefix = oneofp(patterns["it"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            roman = ROMAN,
            suffix = oneofp(patterns["it"]["datesuffix"])
        )
    },
    {
        # Ordinal millennia e.g. "Primo millennio d.C."
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{ordinal}}) mill(ennio|\.)(\s{{suffix}})?".format(
            prefix = oneofp(patterns["it"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            ordinal = oneofp(patterns["it"]["ordinals"]),
            suffix = oneofp(patterns["it"]["datesuffix"])
        )
    }
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
patterns["nl"]["cardinals"] = [
    {"value": 1, "pattern": r"(?:1|????n)"},
    {"value": 2, "pattern": r"(?:2|twee)"},
    {"value": 3, "pattern": r"(?:3|drie)"},
    {"value": 4, "pattern": r"(?:4|vier)"},
    {"value": 5, "pattern": r"(?:5|vijf)"},
    {"value": 6, "pattern": r"(?:6|zes)"},
    {"value": 7, "pattern": r"(?:7|zeven)"},
    {"value": 8, "pattern": r"(?:8|acht)"},
    {"value": 9, "pattern": r"(?:9|negen)"},
    {"value": 10, "pattern": r"(?:10|tien)"},
    {"value": 11, "pattern": r"(?:11|elf)"},
    {"value": 12, "pattern": r"(?:12|twaalf)"},
    {"value": 13, "pattern": r"(?:13|dertien)"},
    {"value": 14, "pattern": r"(?:14|veertien)"},
    {"value": 15, "pattern": r"(?:15|vijftien)"},
    {"value": 16, "pattern": r"(?:16|zestien)"},
    {"value": 17, "pattern": r"(?:17|zeventien)"},
    {"value": 18, "pattern": r"(?:18|achttien)"},
    {"value": 19, "pattern": r"(?:19|negentien)"},
    {"value": 20, "pattern": r"(?:20|twintig)"},
    {"value": 21, "pattern": r"(?:21|eenentwintig)"},
    {"value": 22, "pattern": r"(?:22|twee??ntwintig)"},
    {"value": 23, "pattern": r"(?:23|drie??ntwintig)"},
    {"value": 24, "pattern": r"(?:24|vierentwintig)"},
    {"value": 25, "pattern": r"(?:25|vijfentwintig)"},
    {"value": 26, "pattern": r"(?:26|zesentwintig)"},
    {"value": 27, "pattern": r"(?:27|zevenentwintig)"},
    {"value": 28, "pattern": r"(?:28|achtentwintig)"},
    {"value": 29, "pattern": r"(?:29|negenentwintig)"},
    {"value": 30, "pattern": r"(?:30|dertig)"},
    {"value": 31, "pattern": r"(?:31|eenendertig)"}
]

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
    {"value": 22, "pattern": r"(?:22e|twee??ntwintigste)"},   # twenty second
    {"value": 23, "pattern": r"(?:23e|drie??ntwintig)"},      # twenty third
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
    {"value": enums.Month.FEB, "pattern": r"Feb(?:\.|ruari)?"},       # February
    {"value": enums.Month.MAR, "pattern": r"Maart"},                # March
    {"value": enums.Month.APR, "pattern": r"Apr(?:\.|il)?"},          # April
    {"value": enums.Month.MAY, "pattern": r"Mei"},                  # May
    {"value": enums.Month.JUN, "pattern": r"Juni"},                 # June
    {"value": enums.Month.JUL, "pattern": r"Juli"},                 # July
    {"value": enums.Month.AUG, "pattern": r"Aug(?:\.|ustus)?"},       # August
    {"value": enums.Month.SEP, "pattern": r"Sept(?:\.|ember)?"},      # September
    {"value": enums.Month.OCT, "pattern": r"O[kc]t(?:\.|ober)?"},     # October
    {"value": enums.Month.NOV, "pattern": r"Nov(?:\.|ember)?"},       # November
    {"value": enums.Month.DEC, "pattern": r"Dec(?:\.|ember)?"}        # December
]

patterns["nl"]["seasonnames"] = [
    {"value": enums.Season.SPRING, "pattern": r"Lente"},        # Spring
    {"value": enums.Season.SUMMER, "pattern": r"Zomer"},        # Summer
    {"value": enums.Season.AUTUMN, "pattern": r"Herfst"},       # Autumn
    {"value": enums.Season.WINTER, "pattern": r"Winter"}        # Winter
]

patterns["nl"]["dateprefix"] = [
    {"value": enums.DatePrefix.CIRCA, "pattern": r"ongeveer"},
    {"value": enums.DatePrefix.CIRCA, "pattern": r"ca\.?" },
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
    {"pattern": r"(?:tot|tegen)" }   # until " by
]

patterns["nl"]["datesuffix"] = [
    {"value": enums.DateSuffix.AD, "pattern": r"(?:na?\.?\s?(?:Christus|Chr\.?)|A\.?D\.?|C\.?E\.?)"},
    {"value": enums.DateSuffix.BC, "pattern": r"(?:(?:voor|v????r|v\.?)\s?(?:Christus|Chr\.?|c\.?)|(?:cal\.?\s)?B\.?C\.?(E\.?)?)"},
    {"value": enums.DateSuffix.BP, "pattern": r"(?:(?:??r\s)?f??re nutid|B\.?P\.?)" }
]

patterns["nl"]["dateseparator"] = [
    {"pattern": r"\s?\p{Pd}\s?"},
    {"pattern": r"\s?/\s?"},
    {"pattern": r"\stot\s"},
    {"pattern": r"\sen\s"},
    {"pattern": r"\sof\s"}       
]

patterns["nl"]["periodnames"] = [
    {"pattern": r"Prehistorie", "value": YearSpan()},
    {"pattern": r"Steentijd", "value": YearSpan()},
    {"pattern": r"Paleolithicum", "value": YearSpan()},
    {"pattern": r"Vroeg Paleolithicum", "value": YearSpan()},
    {"pattern": r"Midden Paleolithicum", "value": YearSpan()},
    {"pattern": r"Laat Paleolithicum", "value": YearSpan(-35000, -8801)},       # Late Paleolithic
    {"pattern": r"Laat Paleolithicum A", "value": YearSpan(-35000, -18001)},    # Late Paleolithic A
    {"pattern": r"Laat Paleolithicum B", "value": YearSpan(-18000, -8801)},     # Late Paleolithic B
    {"pattern": r"Mesolithicum", "value": YearSpan(-8800, -5301)},              # Mesolithic
    {"pattern": r"Vroeg Mesolithicum", "value": YearSpan(-8800, -7101)},        # Early Mesolithic
    {"pattern": r"Midden Mesolithicum", "value": YearSpan(-7100, -6451)},       # Middle Mesolithic
    {"pattern": r"Laat Mesolithicum", "value": YearSpan(-6450, -5301)},         # Late Mesolithic
    {"pattern": r"Neolithicum", "value": YearSpan(-5300, -2001)},               # Neolithic
    {"pattern": r"Vroeg Neolithicum", "value": YearSpan(-5300, -4201)},         # Early Neolithic
    {"pattern": r"Vroeg Neolithicum A", "value": YearSpan(-5300, -4901)},       # Early Neolithic A
    {"pattern": r"Vroeg Neolithicum B", "value": YearSpan(-4900, -4201)},       # Early Neolithic B
    {"pattern": r"Midden Neolithicum", "value": YearSpan(-4200, -2851)},        # Middle Neolithic
    {"pattern": r"Midden Neolithicum A", "value": YearSpan(-4200, -3401)},      # Middle Neolithic A
    {"pattern": r"Midden Neolithicum B", "value": YearSpan(-3400, -2851)},      # Middle Neolithic B
    {"pattern": r"Laat Neolithicum", "value": YearSpan(-2850, -2451)},          # Late Neolithic
    {"pattern": r"Laat Neolithicum A", "value": YearSpan(-2850, -2451)},        # Late Neolithic A
    {"pattern": r"Laat Neolithicum B", "value": YearSpan(-2450, -2001)},        # Late Neolithic B
    {"pattern": r"Metaaltijden", "value": YearSpan(-2450, -13)},                # Metal Age
    {"pattern": r"Bronstijd", "value": YearSpan(-2000, -801)},                  # Bronze Age
    {"pattern": r"Vroege Bronstijd", "value": YearSpan(-2000, -1801)},          # Early Bronze Age
    {"pattern": r"Midden Bronstijd", "value": YearSpan(-1800, -1101)},          # Middle Bronze Age
    {"pattern": r"Midden Bronstijd A", "value": YearSpan(-1800, -1501)},        # Middle Bronze Age A
    {"pattern": r"Midden Bronstijd B", "value": YearSpan(-1500, -1101)},        # Middle Bronze Age B
    {"pattern": r"Late Bronstijd", "value": YearSpan(-1101, -801)},             # Late Bronze Age
    {"pattern": r"IJzertijd", "value": YearSpan(-800, -13)},                    # Iron Age
    {"pattern": r"Vroege IJzertijd", "value": YearSpan(-800, -501)},            # Early Iron Age
    {"pattern": r"Midden IJzertijd", "value": YearSpan(-500, -251)},            # Middle Iron Age
    {"pattern": r"Late IJzertijd", "value": YearSpan(-250, -13)},               # Late Iron Age
    {"pattern": r"Protohistorie", "value": YearSpan(-12, 449)},                 # Protohistory
    {"pattern": r"Romeinse?(?:\sTijd)?", "value": YearSpan(-12, 449)},           # Roman
    {"pattern": r"Vroeg Romeinse(?:\sTijd)?", "value": YearSpan(-12, 69)},      # Early Roman
    {"pattern": r"Vroeg Romeinse Tijd A", "value": YearSpan(-12, 24)},          # Early Roman A
    {"pattern": r"Vroeg Romeinse Tijd B", "value": YearSpan(25, 69)},           # Early Roman B
    {"pattern": r"Midden Romeinse(?:\sTijd)?", "value": YearSpan(70, 269)},     # Middle Roman 
    {"pattern": r"Midden Romeinse Tijd A", "value": YearSpan(70, 149)},         # Middle Roman A
    {"pattern": r"Midden Romeinse Tijd B", "value": YearSpan(150, 269)},        # Middle Roman B
    {"pattern": r"Laat Romeinse(?:\sTijd)?", "value": YearSpan(270, 449)},      # Late Roman
    {"pattern": r"Laat Romeinse Tijd A", "value": YearSpan(270, 349)},          # Late Roman A
    {"pattern": r"Laat Romeinse Tijd B", "value": YearSpan(350, 449)},          # Late Roman B
    {"pattern": r"Historie", "value": YearSpan(450, 1950)},                     # Historic
    {"pattern": r"Middeleeuw(?:en|se?)", "value": YearSpan(450, 1499)},         # Medieval
    {"pattern": r"Vroege Middeleeuwen", "value": YearSpan(450, 1049)},          # Early Medieval
    {"pattern": r"Vroege Middeleeuwen A", "value": YearSpan(450, 524)},         # Early Medieval A
    {"pattern": r"Vroege Middeleeuwen B", "value": YearSpan(525, 724)},         # Early Medieval B
    {"pattern": r"Vroege Middeleeuwen C", "value": YearSpan(725, 899)},         # Early Medieval C
    {"pattern": r"Vroege Middeleeuwen D", "value": YearSpan(900, 1049)},        # Early Medieval D
    {"pattern": r"Late Middeleeuwen", "value": YearSpan(1050, 1499)},           # Late Medieval
    {"pattern": r"Late Middeleeuwen A", "value": YearSpan(1050, 1249)},         # Late Medieval A
    {"pattern": r"Late Middeleeuwen B", "value": YearSpan(1250, 1499)},         # Late Medieval B
    {"pattern": r"Nieuwe Tijd", "value": YearSpan(1500, 1944)},                 # Modern period
    {"pattern": r"Nieuwe Tijd A", "value": YearSpan()},                         # Modern period A
    {"pattern": r"Nieuwe Tijd B", "value": YearSpan()},                         # Modern period B
    {"pattern": r"Nieuwe Tijd C", "value": YearSpan()},                         # Modern period C
    {"pattern": r"Nieuwe Tijd Vroeg", "value": YearSpan(1500, 1649)},           # Early Modern period 
    {"pattern": r"Nieuwe Tijd Midden", "value": YearSpan(1650, 1849)},          # Middle Modern period 
    {"pattern": r"Nieuwe Tijd Laat", "value": YearSpan(1850, 1944)},            # Late Modern period 
    {"pattern": r"Recent", "value": YearSpan(1945, 2000)},                      # Contemporary
    {"pattern": r"Onbekend", "value": YearSpan()},
    {"pattern": r"Overige?", "value": YearSpan()},
    {"pattern": r"Hoge Middeleeuwen", "value": YearSpan()},
    {"pattern": r"Volle Middeleeuwen", "value": YearSpan()},
    {"pattern": r"Tweede Wereldoorlog", "value": YearSpan()}
    
]

patterns["nl"]["datespans"] = [
    {
        # Month and year
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{month}}) ({{year}})(\s{{suffix}})?".format(
            prefix = oneofp(patterns["nl"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            month = oneofp(patterns["nl"]["monthnames"]),
            year =  NUMERICYEAR,
            suffix = oneofp(patterns["nl"]["datesuffix"])
        )
    },
    {
        # Season and year
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{season}}) ({{year}})(\s{{suffix}})?".format(
            prefix = oneofp(patterns["nl"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            season = oneofp(patterns["nl"]["seasonnames"]),
            year =  NUMERICYEAR,
            suffix = oneofp(patterns["nl"]["datesuffix"]),
        )
    },
    {
        # year with suffix e.g. "8100 BCE"
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{year}})(\s?{{suffix}})\b".format(
            prefix = oneofp(patterns["nl"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            year =  NUMERICYEAR,
            suffix = oneofp(patterns["nl"]["datesuffix"])
        )
    },
    {
        # year with prefix e.g. "circa 1854"
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)+({{year}})(\s?{{suffix}})?\b".format(
            prefix = oneofp(patterns["nl"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            year =  NUMERICYEAR,
            suffix = oneofp(patterns["nl"]["datesuffix"])
        )
    },
    {
        # from year to year
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{fromYear}})(\s?{{suffix}})?{{separator}}({{prefix}}{{spaceordash}}?)*({{toYear}})(\s?{{suffix}})?\b".format(
            prefix = oneofp(patterns["nl"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            fromYear = NUMERICYEAR,
            separator = oneofp(patterns["nl"]["dateseparator"]),
            toYear = NUMERICYEAR,
            suffix = oneofp(patterns["nl"]["datesuffix"])
        )
    },
    {
        # named historical periods
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{named}})\b".format(
            prefix = oneofp(patterns["nl"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            named = oneofp(patterns["nl"]["periodnames"])
        )
    },
    {
        # from named to named historical periods
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{named1}}){{separator}}({{prefix}}{{spaceordash}}?)*({{named2}})".format(
            prefix = oneofp(patterns["nl"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            named1 = oneofp(patterns["nl"]["periodnames"]),
            named2 = oneofp(patterns["nl"]["periodnames"]),
            separator = oneofp(patterns["nl"]["dateseparator"])
        )
    },
    {
        # decades e.g. "1850's"
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{decade}})(\s?{{suffix}})?\b".format(
            prefix = oneofp(patterns["nl"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            decade = r"\b[1-9]\d{1,2}0'?s",
            suffix = oneofp(patterns["nl"]["datesuffix"])
        )
    },
    {
        # from decade to decade e.g. e.g. ""
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{decade1}}){{separator}}({{prefix}}{{spaceordash}}?)*({{decade2}})(\s?{{suffix}})?\b".format(
            prefix = oneofp(patterns["nl"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            decade1 = r"\b[1-9]\d{1,2}0'?s",
            decade2 = r"\b[1-9]\d{1,2}0'?s",
            separator = oneofp(patterns["nl"]["dateseparator"]),
            suffix = oneofp(patterns["nl"]["datesuffix"])
        )
    },
    {
        # Ordinal century e.g. "vijfde eeuw na Christus", "5th century AD"
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{ordinal}}) eeuw(\s{{suffix}})?".format(
            prefix = oneofp(patterns["nl"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            ordinal = oneofp(patterns["nl"]["ordinals"]),
            suffix = oneofp(patterns["nl"]["datesuffix"])
        )
    },
    {
        # Ordinal"Ordinal century e.g. "14e - 15e eeuw", "14th"15th century"
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{ordinal1}}){{separator}}({{prefix}}{{spaceordash}}?)*({{ordinal2}}) eeuw(\s{{suffix}})?".format(
            prefix = oneofp(patterns["nl"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            ordinal1 = oneofp(patterns["nl"]["ordinals"]),
            ordinal2 = oneofp(patterns["nl"]["ordinals"]),
            separator = oneofp(patterns["nl"]["dateseparator"]),
            suffix = oneofp(patterns["nl"]["datesuffix"])
        )
    },
    {
        # Ordinal millennium e.g. "begin 2de millennium AD"
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{ordinal}}) millennium(\s{{suffix}})?".format(
            prefix = oneofp(patterns["nl"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            ordinal = oneofp(patterns["nl"]["ordinals"]),
            suffix = oneofp(patterns["nl"]["datesuffix"])
        )
    },
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
patterns["no"]["cardinals"] = [
    {"value": 0, "pattern": r"(?:0|Null)"},
    {"value": 1, "pattern": r"(?:1|En)"},
    {"value": 2, "pattern": r"(?:2|To)"},
    {"value": 3, "pattern": r"(?:3|Tre)"},
    {"value": 4, "pattern": r"(?:4|Fire)"},
    {"value": 5, "pattern": r"(?:5|Fem)"},
    {"value": 6, "pattern": r"(?:6|Seks)"},
    {"value": 7, "pattern": r"(?:7|Sju)"},
    {"value": 8, "pattern": r"(?:8|??tte)"},
    {"value": 9, "pattern": r"(?:9|Ni)"},
    {"value": 10, "pattern": r"(?:10|Ti)"},
    {"value": 11, "pattern": r"(?:11|Elleve)"},
    {"value": 12, "pattern": r"(?:12|Tolv)"},
    {"value": 13, "pattern": r"(?:13|Tretten)"},
    {"value": 14, "pattern": r"(?:14|Fjorten)"},
    {"value": 15, "pattern": r"(?:15|Femten)"},
    {"value": 16, "pattern": r"(?:16|Seksten)"},
    {"value": 17, "pattern": r"(?:17|Sytten)"},
    {"value": 18, "pattern": r"(?:18|Atten)"},
    {"value": 19, "pattern": r"(?:19|Nitten)"},
    {"value": 20, "pattern": r"(?:20|Tjue)"},
    {"value": 21, "pattern": r"(?:21|Tjueen)"},
    {"value": 22, "pattern": r"(?:22|Tjueto)"},
    {"value": 23, "pattern": r"(?:23|Tjuetre)"},
    {"value": 24, "pattern": r"(?:24|Tjuefire)"},
    {"value": 25, "pattern": r"(?:25|Tjuefem)"},
    {"value": 26, "pattern": r"(?:26|Tjueseks)"},
    {"value": 27, "pattern": r"(?:27|Tjuesju)"},
    {"value": 28, "pattern": r"(?:28|Tjue??tte)"},
    {"value": 29, "pattern": r"(?:29|Tjueni)"},
    {"value": 30, "pattern": r"(?:30|tretti)"},
    {"value": 31, "pattern": r"(?:31|trettien)"}
]

patterns["no"]["ordinals"] = [
    {"value": 1, "pattern": r"(?:1\.?|f???rste?)"},          # first
    {"value": 2, "pattern": r"(?:2\.?|an(?:nen|na|net|dre))"}, # second
    {"value": 3, "pattern": r"(?:3\.?|tredje)"},            # third
    {"value": 4, "pattern": r"(?:4\.?|fjerde)"},            # fourth
    {"value": 5, "pattern": r"(?:5\.?|femte)"},             # fifth
    {"value": 6, "pattern": r"(?:6\.?|sjette)"},            # sixth
    {"value": 7, "pattern": r"(?:7\.?|syvende|sjuende)"},   # seventh
    {"value": 8, "pattern": r"(?:8\.?|??ttende)"},           # eighth
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
    {"value": 21, "pattern": r"(?:21\.?|tjuef??rste?)"},      # twenty first
    {"value": 22, "pattern": r"(?:22\.?|tjue sekund)"},      # twenty second
    {"value": 23, "pattern": r"(?:23\.?|tjuetredje)"},       # twenty third
    {"value": 24, "pattern": r"(?:24\.?|tjuefjerde)"},       # twenty fourth
    {"value": 25, "pattern": r"(?:25\.?|tjuefemte)"},        # twenty fifth
    {"value": 26, "pattern": r"(?:26\.?|tjuesjette)"},       # twenty sixth
    {"value": 27, "pattern": r"(?:27\.?|tjuesyvende)"},      # twenty seventh
    {"value": 28, "pattern": r"(?:28\.?|tjue??tte)"},         # twenty eighth
    {"value": 29, "pattern": r"(?:29\.?|tjueniende)"},       # twenty ninth
    {"value": 30, "pattern": r"(?:30\.?|tretti)"},           # thirtieth
    {"value": 31, "pattern": r"(?:11\.?|trettif??rste?)"}     # thirty first
]

patterns["no"]["daynames"] = [
    {"value": enums.Day.MON, "pattern": r"m(?:??|aa?)n(?:dag)?"},  # Monday
    {"value": enums.Day.TUE, "pattern": r"t(?:y|ir)s(?:dag)?"},   # Tuesday
    {"value": enums.Day.WED, "pattern": r"ons(?:dag)?"},        # Wednesday
    {"value": enums.Day.THU, "pattern": r"tors(?:dag)?"},       # Thursday
    {"value": enums.Day.FRI, "pattern": r"fre(?:dag)?"},        # Friday
    {"value": enums.Day.SAT, "pattern": r"l(?:au|??)(?:r|dag)?"},  # Saturday
    {"value": enums.Day.SUN, "pattern": r"s??n(?:dag)?"},        # Sunday
    {"pattern": r"i forg??rs"},        # Day before yesterday
    {"pattern": r"i g??r"},            # Yesterday
    {"pattern": r"i dag"},            # Today
    {"pattern": r"i morgen"},         # Tomorrow
    {"pattern": r"i overmorgen"}      # Day after tomorrow
]

patterns["no"]["monthnames"] = [
    {"value": enums.Month.JAN, "pattern": r"jan(?:uar)?"},    # January
    {"value": enums.Month.FEB, "pattern": r"feb(?:r|ruar)?"}, # February
    {"value": enums.Month.MAR, "pattern": r"mars?"},        # March
    {"value": enums.Month.APR, "pattern": r"apr(?:il)?"},     # April
    {"value": enums.Month.MAY, "pattern": r"mai"},          # May
    {"value": enums.Month.JUN, "pattern": r"juni?"},        # June
    {"value": enums.Month.JUL, "pattern": r"juli?"},        # July
    {"value": enums.Month.AUG, "pattern": r"aug(?:ust)?"},    # August
    {"value": enums.Month.SEP, "pattern": r"sept(?:ember)?"}, # September
    {"value": enums.Month.OCT, "pattern": r"okt(?:ober)?"},   # October
    {"value": enums.Month.NOV, "pattern": r"nov(?:ember)?"},  # November
    {"value": enums.Month.DEC, "pattern": r"des(?:ember)?"}   # December
]

patterns["no"]["seasonnames"] = [
    {"value": enums.Season.SPRING, "pattern": r"(?:p??\s)?v??r(?:en)?(?:\sI)?"},
    {"value": enums.Season.SUMMER, "pattern": r"(?:p??\s)?sommer(?:en)?"},
    {"value": enums.Season.AUTUMN, "pattern": r"(?:p??\s)?h??st(?:en)?"},
    {"value": enums.Season.WINTER, "pattern": r"(?:p??\s)?vinter(?:en)?"},
    {"pattern": r"m??rketiden"},               # dark time
    {"pattern": r"(?:p??\s)?vinterhalv??ret"},    # winter half
    {"pattern": r"(?:p??\s)?sommerhalv??ret"}     # summer half
]

patterns["no"]["dateprefix"] = [
    {"value": enums.DatePrefix.CIRCA, "pattern": r"cir[ck]a"},
    {"value": enums.DatePrefix.CIRCA, "pattern": r"ca\.?"},
    {"value": enums.DatePrefix.CIRCA, "pattern": r"rundt"},
    {"value": enums.DatePrefix.CIRCA, "pattern": r"omtrent" },
    {"value": enums.DatePrefix.EARLY, "pattern": r"(?:[e????]ldre|eldste|tidl?[ei]g(?:\sp??)?|begynnelsen av)"},
    {"value": enums.DatePrefix.MID, "pattern": r"(?:midt(en)?(\sdet)?|mellom)(?:\sav(\sdet)?)?"},
    {"value": enums.DatePrefix.LATE, "pattern": r"(?:Yngre|sei?n\p{Pd}?|slutten av|sent|h??[gy]\p{Pd}?)"},
    {"value": enums.DatePrefix.HALF1, "pattern": r"f???rste halvdel(?:\sav(?:\sdet)?)?"},           # first half (of the)
    {"value": enums.DatePrefix.HALF2, "pattern": r"(?:andre|annen) halvdel(?:\sav(?:\sdet)?)?"},     # second half (of the)
    {"value": enums.DatePrefix.QUARTER1, "pattern": r"f???rste kvartal(?:\sav(?:\sdet)?)?"},       # first quarter (of the)
    {"value": enums.DatePrefix.QUARTER2, "pattern": r"andre kvartal(?:\sav(?:\sdet)?)?"},         # second quarter (of the)
    {"value": enums.DatePrefix.QUARTER3, "pattern": r"tredje kvartal(?:\sav(?:\sdet)?)?"},        # third quarter (of the)
    {"value": enums.DatePrefix.QUARTER4, "pattern": r"(?:fjerde|siste) kvartal(?:\sav(?:\sdet)?)?"}, # fourth|last quarter (of the)
    {"pattern": r"inngangen til"},                    # beginning of
    {"pattern": r"(?:I\s)?begynnelsen av(?:\sdet)?"},     # beginning of
    {"pattern": r"slutten av(?:\sdet)?"},               # end of
    {"pattern": r"fr(?:??|aa?)"},                        # from
    {"pattern": r"f[o??]r"},                           # before
    {"pattern": r"(?:I|p??)"},                           # in
    {"pattern": r"(?:I\s)?l??pet av"},                   # During
    {"pattern": r"(?:etter|siden)"},                    # post " after " since
    {"pattern": r"(?:inn)?til"}                       # until " by
]

patterns["no"]["datesuffix"] = [
    {"value": enums.DateSuffix.AD, "pattern": r"(?:e\.\s?Kr\.?|A\.?D\.?|C\.?E\.?)"},
    {"value": enums.DateSuffix.BC, "pattern": r"(?:f??r n??tid|f\.\s?Kr\.?|fvt\.?|(?:cal\.?\s)?B\.?C\.?(?:E\.?)?)"},
    {"value": enums.DateSuffix.BP, "pattern": r"B\.?P\.?" }
]

patterns["no"]["dateseparator"] = [
    {"pattern": r"\s?\p{Pd}\s?"},
    {"pattern": r"\s?/\s?"},
    {"pattern": r"\stil\s"},
    {"pattern": r"\sog\s"},
    {"pattern": r"\soch\s"},
    {"pattern": r"\seller\s"}       
]

patterns["no"]["century"] = [
    {"pattern": r"??rhundre"}
]

patterns["no"]["millennium"] = [
    {"pattern": r"??rtusen"}
]

# named historical periods. See https:#no.wikipedia.org"wiki"Steinalderen_i_Norge
# and also Perio.do collection http://n2t.net/ark:/99152/p04h98q
patterns["no"]["periodnames"] = [
    {"pattern": r"eldre steinalder(?:en)?", "value": YearSpan(-9500, -4000)}, # early stone age    
    {"pattern": r"steinalder(?:en)?", "value": YearSpan(-9500, -1700)}, # stone age
    {"pattern": r"tidlig(?:mesolitt?iske?|mesol[iuo]tikk?um)", "value": YearSpan(-9500, -8000)}, # Early Mesolithic
    {"pattern": r"mellom(?:mesolitt?iske?|mesol[iuo]tikk?um)", "value": YearSpan(-8000, -6000)}, # Middle Mesolithic
    {"pattern": r"sen(?:mesolitt?iske?|mesol[iuo]tikk?um)", "value": YearSpan(-8000, -6000)}, # Late Mesolithic
    {"pattern": r"yngre steinalder(?:en)?", "value": YearSpan(-4000, -1700)}, # Neolithic    
    {"pattern": r"tidlig(?:neolittiske?|neolitikum)", "value": YearSpan(-4000, -2800)}, # Early Neolithic 
    {"pattern": r"mellom(?:neolittiske?|neolitikum)", "value": YearSpan(-2800, -2400)}, # Middle Neolithic 
    {"pattern": r"sei?n(?:neolittiske?|neolitikum)", "value": YearSpan(-2400, -1700)}, # Late Neolithic
    {"pattern": r"tidlig metalltid", "value": YearSpan(-2000, -300)}, # Early Metal Age
    {"pattern": r"brons(?:ea|??|aa?)lder(?:en)?", "value": YearSpan(-1700, -500)}, # Bronze age    
    {"pattern": r"eldre brons(?:ea|??|aa?)lder(?:en)?", "value": YearSpan(-1700, -1100)}, # Early Bronze age
    {"pattern": r"yngre brons(?:ea|??|aa?)lder(?:en)?", "value": YearSpan(-1700, -500)}, # Late Bronze age
    {"pattern": r"j[e????]rn(?:??|aa?)lder(?:en)?", "value": YearSpan(-500, 1050)}, # Iron age
    {"pattern": r"eldre j[e????]rn(?:??|aa?)lder(?:en)?", "value": YearSpan(-500, 550)}, # Early Iron age
    {"pattern": r"yngre j[e????]rn(?:??|aa?)lder(?:en)?", "value": YearSpan(550, 1050)}, # Late Iron age
    {"pattern": r"f??rromersk j[e????]rn(?:??|aa?)lder(?:en)?", "value": YearSpan(-500, 0)}, # Pre-Roman Iron age
    {"pattern": r"romer(?:ske?|tid)", "value": YearSpan(0, 400)}, # Roman Iron Age
    {"pattern": r"eldre romer(?:ske?|tid)", "value": YearSpan(0, 200)}, # Early Roman Iron Age
    {"pattern": r"yngre romer(?:ske?|tid)", "value": YearSpan(200, 400)}, # Early Roman Iron Age
    {"pattern": r"Folkevandringstid(?:en)?", "value": YearSpan(400, 550)}, # migration period
    {"pattern": r"merovingertid(?:en)?", "value": YearSpan(550, 750)}, # Merovingian
    {"pattern": r"Vikinge?tid(?:en)?", "value": YearSpan(750, 1050)}, # Viking age
    {"pattern": r"(?:middelalder(?:en)?|medeltida)", "value": YearSpan(1050, 1500)}, # Medieval   
    {"pattern": r"tidlig(?:middelalder(?:en)?|medeltida)", "value": YearSpan(1050, 1130)}, # Early Medieval
    {"pattern": r"h??y(?:middelalder(?:en)?|medeltida)", "value": YearSpan(1050, 1350)}, # High Middle Ages
    {"pattern": r"sen(?:middelalder(?:en)?|medeltida)", "value": YearSpan(1350, 1500)}, # Late Middle Ages
    {"pattern": r"(?:nyere|moderne|v??r) tida?", "value": YearSpan(1500, 2050)},    # Modern period
    {"pattern": r"istid(?:ens?)?"}, # ice age
    {"pattern": r"oldtid(?:ens?)?"}, # ancient times
    {"pattern": r"forhistoriske"}, # prehistoric
    {"pattern": r"(?:paleolittiske?|paleolitikum)"}, # Paleolithic
    {"pattern": r"jegersteinalder(?:en)?"}, # Early Mesolithic   
    {"pattern": r"pionerfase"}, # subdivision of early Mesolithic
    {"pattern": r"pionerbosetning(en)?"}, # subdivision of early Mesolithic
    {"pattern": r"jeger(?:\p{Pd}?kultur(?:en)?)?"}, # subdivision of early Mesolithic
    {"pattern": r"fosna(?:\p{Pd}?kultur(?:en)?)?"}, # subdivision of Mesolithic
    {"pattern": r"komsa(?:\p{Pd}?kultur(?:en)?)?"}, # subdivision of Mesolithic
    {"pattern": r"(?:Mikrolittfasen|\bMM\b)"}, # subdivision of middle Mesolithic
    {"pattern": r"T??rkopfasen"}, # subdivision of middle Mesolithic
    {"pattern": r"Lundev(?:??|aa?)genfasen"}, # subdivision of middle Mesolithic
    {"pattern": r"N??stvet"}, # subdivision of late Mesolithic
    {"pattern": r"N??stvet(?:\p{Pd}?kultur(?:en)?)?"}, # subdivision of late Mesolithic
    {"pattern": r"N??stvetfasen"}, # subdivision of late Mesolithic
    {"pattern": r"Gj??lstadfasen"}, # subdivision of late Mesolithic
    {"pattern": r"Tverrpilfasen"}, # subdivision of late Mesolithic
    {"pattern": r"N??stvet??ksfasen"}, # subdivision of late Mesolithic
    {"pattern": r"(?:Traktbeger(?:fasen)?|\bTRB\b)"}, # subdivision of Early Neolithic (from Marianne Moen)
    {"pattern": r"Senstenalder"}, # subdivision of Neolithic (from Marianne Moen)
    {"pattern": r"Bondesteinalder"}, # subdivision of Neolithic (from Marianne Moen)
    {"pattern": r"Strids??ksfasen"}, # subdivision of middle neolithic (from Marianne Moen)
    {"pattern": r"seinneolitikum"}, # subdivision of late neolithic (from Marianne Moen)
    {"pattern": r"metalltid(en)?"}, # Metal age        
    {"pattern": r"Germansk j[e????]rn(?:??|aa?)lder(?:en)?"}, # Germanic iron age   
    {"pattern": r"reformatorisk"}, # reformation
    {"pattern": r"Borgerkrigstid(?:en)?"}, # Civil War Period
    {"pattern": r"mellomkrigstid(?:en)?"}, # inter war period    
    #{ "pattern": r"i dag"},   # the present
    {"pattern": r"etter\p{Pd}reformatorisk"},
    {"pattern": r"Per(?:\.|iode) [IV]+" } # period numbers related to Bronze age (from Marianne Moen)    
]

# composite patterns for expressions of datespans
patterns["no"]["datespans"] = [
    {
        # Prefix and numeric year, maybe a suffix e.g. "fr?? 1984"
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)+({{year}})(\s{{suffix}})?\b".format(
            prefix = oneofp(patterns["no"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            year =  NUMERICYEAR,
            suffix = oneofp(patterns["no"]["datesuffix"])
        )
    },
    {
        # maybe a prefix, numeric year and a suffix e.g. "fr?? 1984"
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{year}})(\s{{suffix}})\b".format(
            prefix = oneofp(patterns["no"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            year =  NUMERICYEAR,
            suffix = oneofp(patterns["no"]["datesuffix"])
        )
    },
    {
        # Month and year e.g. "Oktober 1984"
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{month}}) ({{year}})(\s{{suffix}})?\b".format(
            prefix = oneofp(patterns["no"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            month = oneofp(patterns["no"]["monthnames"]),
            year =  NUMERICYEAR,
            suffix = oneofp(patterns["no"]["datesuffix"])
        )
    },
    {
        # Season and year e.g. "h??st 1984 f.Kr"
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{season}}) ({{year}})(\s{{suffix}})?\b".format(
            prefix = oneofp(patterns["no"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            season = oneofp(patterns["no"]["seasonnames"]),
            year =  NUMERICYEAR,
            suffix = oneofp(patterns["no"]["datesuffix"])
        )
    },
    {
        # e.g. 2+ digits, starting with 1..9, ending with 0, then "-??rene" e.g. "30-??rene" (the 30s)
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{year}}){{spaceordash}}??r(a|s|ene)\b".format(
            prefix = oneofp(patterns["no"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            year =  r"[1-9]\d{0,}0"
        )
    },
    {
        # e.g. "i ??r 166" (the year 166)
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*i ??r ({{year}})(\s{{suffix}})?\b".format(
            prefix = oneofp(patterns["no"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            year =  NUMERICYEAR,
            suffix = oneofp(patterns["no"]["datesuffix"])
        )
    },
    {
        # ordinal century e.g. "f??rste halvdel av det andre ??rhundre f.Kr."
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{ordinal}}) ??rhundre(t|de)?(\s{{suffix}})?\b".format(
            prefix = oneofp(patterns["no"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            ordinal = oneofp(patterns["no"]["ordinals"]),
            suffix = oneofp(patterns["no"]["datesuffix"])
        )
    },
    {
        # Part of ordinal millennium e.g. "f??rste halvdel av det andre ??rtusen f.Kr."
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{ordinal}}) ??rtusen(\s{{suffix}})?\b".format(
            prefix = oneofp(patterns["no"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            ordinal = oneofp(patterns["no"]["ordinals"]),
            suffix = oneofp(patterns["no"]["datesuffix"])
        )
    },
    {
        # numeric year (not starting with 0) with suffix e.g. "ca. 8100 f.Kr."
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*(??r\s)?({{year}})(\s?{{suffix}})\b".format(
            prefix = oneofp(patterns["no"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            year =  NUMERICYEAR,
            suffix = oneofp(patterns["no"]["datesuffix"])
        )
    },
    {
        # numeric year (not starting with 0) with tolerance followed by suffix e.g. "2735??35 BP"
        "pattern": fr"\b({{year}})(\s?{{tolerance}})(\s?{{suffix}})?".format(
            year =  NUMERICYEAR,
            tolerance = r"??[1-9]\d*",
            suffix = oneofp(patterns["no"]["datesuffix"])
        )
    },
    {
        # numeric year with suffix followed by tolerance e.g. "2735 BP??35"
        "pattern": fr"\b({{year}})(\s?{{suffix}})?(\s?{{tolerance}})".format(
            year =  NUMERICYEAR,
            tolerance = r"??[1-9]\d*",
            suffix = oneofp(patterns["no"]["datesuffix"])
        )
    },
    {
        # from year to year e.g. "ca. 8100???7800 f.Kr."
        # see https:#www.regular-expressions.info"unicode.html
        # and https:#www.fileformat.info"info"unicode"category"Pd"list.htm
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{fromYear}})(\s?{{suffix}})?{{separator}}({{prefix}}{{spaceordash}}?)*({{toYear}})(\s?{{suffix}})?\b".format(
            prefix = oneofp(patterns["no"]["dateprefix"]),
            suffix = oneofp(patterns["no"]["datesuffix"]),
            spaceordash = SPACEORDASH, # note unicode property \p{Pd} covers all types of hyphen"dash https:#www.fileformat.info"info"unicode"category"Pd"list.htm
            fromYear = NUMERICYEAR,
            separator = oneofp(patterns["no"]["dateseparator"]),
            toYear = NUMERICYEAR
        )
    },
    {
        # From ordinal to ordinal century e.g. "andre eller tredje ??rhundre e.Kr."
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{fromOrdinal}}){{separator}}({{prefix}}{{spaceordash}}?)*({{toOrdinal}}) ??rhundret?(\s{{suffix}})?".format(
            prefix = oneofp(patterns["no"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            fromOrdinal = oneofp(patterns["no"]["ordinals"]),
            separator = oneofp(patterns["no"]["dateseparator"]),
            toOrdinal = oneofp(patterns["no"]["ordinals"]),
            suffix = oneofp(patterns["no"]["datesuffix"])
        )
    },
    {
        # From ordinal to ordinal millennium e.g. "andre eller tredje ??rtusen e.Kr."
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{fromOrdinal}}){{separator}}({{prefix}}{{spaceordash}}?)*({{toOrdinal}}) ??rtusen(\s{{suffix}})?".format(
            prefix = oneofp(patterns["no"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            fromOrdinal = oneofp(patterns["no"]["ordinals"]),
            separator = oneofp(patterns["no"]["dateseparator"]),
            toOrdinal = oneofp(patterns["no"]["ordinals"]),
            suffix = oneofp(patterns["no"]["datesuffix"])
        )
    },
    {
        # Decades e.g. "1100-tallet" (1100s i.e. 12th century)
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{decade}})(\s{{suffix}})?\b".format(
            prefix = oneofp(patterns["no"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            decade = r"[1-9]\d{0,2}0-tal(ls|l?ets?)",
            suffix = oneofp(patterns["no"]["datesuffix"])
        )
    },
    {
        # from decade to decade e.g. e.g. ""
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{decade1}}){{separator}}({{prefix}}{{spaceordash}}?)*({{decade2}})\b".format(
            prefix = oneofp(patterns["no"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            decade1 = r"[1-9]\d{0,2}0-tal(ls|l?ets?)",
            decade2 = r"[1-9]\d{0,2}0-tal(ls|l?ets?)",
            separator = oneofp(patterns["no"]["dateseparator"]),
        )
    },
    {
        # named historical periods
        "pattern": fr"({{prefix}}{{spaceordash}}?)*{{named}}".format(
            prefix = oneofp(patterns["no"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            named = oneofp(patterns["no"]["periodnames"])
        )
    },
    {
        # from named to named historical periods
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{named1}}){{separator}}({{prefix}}{{spaceordash}}?)*({{named2}})".format(
            prefix = oneofp(patterns["no"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            named1 = oneofp(patterns["no"]["periodnames"]),
            separator = oneofp(patterns["no"]["dateseparator"]),
            named2 = oneofp(patterns["no"]["periodnames"])
        )
    }
]

patterns["no"]["directions"] = [
    {"value": enums.Direction.N, "pattern": r"Nord"}, 
    {"value": enums.Direction.NE, "pattern": fr"Nord{SPACEORDASH}??st"},
    {"value": enums.Direction.E, "pattern": r"??st"},
    {"value": enums.Direction.SE, "pattern": r"S??r??st"}, 
    {"value": enums.Direction.S, "pattern": r"S??r"}, 
    {"value": enums.Direction.SW, "pattern": r"S??rvest"}, 
    {"value": enums.Direction.W, "pattern": r"Vest"}, 
    {"value": enums.Direction.NW, "pattern": r"Nordvest"}
]

# 12th century = 1100-tallet, 12. ??rhundre , 12. ??rhundre f.Kr. (f.Kr. =BC e.Kr. = AD) Femte ??rhundre e.Kr.
# Swedish patterns 
patterns["sv"]["cardinals"] = [
    {"value": 1, "pattern": r"(?:1|enn)"},
    {"value": 2, "pattern": r"(?:2|tv??)"},
    {"value": 3, "pattern": r"(?:3|tre)"},
    {"value": 4, "pattern": r"(?:4|fyra)"},
    {"value": 5, "pattern": r"(?:5|fem)"},
    {"value": 6, "pattern": r"(?:6|sex)"},
    {"value": 7, "pattern": r"(?:7|sju)"},
    {"value": 8, "pattern": r"(?:8|??tta)"},
    {"value": 9, "pattern": r"(?:9|nio)"},
    {"value": 10, "pattern": r"(?:10|tio)"},
    {"value": 11, "pattern": r"(?:11|elva)"},
    {"value": 12, "pattern": r"(?:12|tolv)"},
    {"value": 13, "pattern": r"(?:13|tretton)"},
    {"value": 14, "pattern": r"(?:14|fjorton)"},
    {"value": 15, "pattern": r"(?:15|femton)"},
    {"value": 16, "pattern": r"(?:16|sexton)"},
    {"value": 17, "pattern": r"(?:17|sjutton)"},
    {"value": 18, "pattern": r"(?:18|arton)"},
    {"value": 19, "pattern": r"(?:19|nitton)"},
    {"value": 20, "pattern": r"(?:20|tjugo)"},
    {"value": 21, "pattern": r"(?:21|tjugoett)"},
    {"value": 22, "pattern": r"(?:22|tjugotv??)"},
    {"value": 23, "pattern": r"(?:23|tjugotre)"},
    {"value": 24, "pattern": r"(?:24|tjugofyra)"},
    {"value": 25, "pattern": r"(?:25|tjugofem)"},
    {"value": 26, "pattern": r"(?:26|tjugosex)"},
    {"value": 27, "pattern": r"(?:27|tjugosju)"},
    {"value": 28, "pattern": r"(?:28|tjugo??tta)"},
    {"value": 29, "pattern": r"(?:29|tjugonio)"},
    {"value": 30, "pattern": r"(?:30|trettio)"},
    {"value": 31, "pattern": r"(?:31|trettioett)" }
]

patterns["sv"]["ordinals"] = [
    {"value": 1, "pattern": r"(?:1\:\s?a|f??rsta)"},         # first
    {"value": 2, "pattern": r"(?:2\:\s?a|andra)"},          # second
    {"value": 3, "pattern": r"(?:3\:\s?e|tredje)"},         # third
    {"value": 4, "pattern": r"(?:4\:\s?e|fj??rde)"},         # fourth
    {"value": 5, "pattern": r"(?:5\:\s?e|femte)"},          # fifth
    {"value": 6, "pattern": r"(?:6\:\s?e|sj??tte)"},         # sixth
    {"value": 7, "pattern": r"(?:7\:\s?e|sjunde)"},         # seventh
    {"value": 8, "pattern": r"(?:8\:\s?e|??ttonde)"},        # eighth
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
    {"value": 21, "pattern": r"(?:21\:\s?e|tjugof??rsta)"},   # twenty first
    {"value": 22, "pattern": r"(?:22\:\s?e|tjugoandra)"},    # twenty second
    {"value": 23, "pattern": r"(?:23\:\s?e|tjugotredje)"},   # twenty third
    {"value": 24, "pattern": r"(?:24\:\s?e|tjugofj??rde)"},   # twenty fourth
    {"value": 25, "pattern": r"(?:25\:\s?e|tjugofemte)"},    # twenty fifth
    {"value": 26, "pattern": r"(?:26\:\s?e|tjugosj??tte)"},   # twenty sixth
    {"value": 27, "pattern": r"(?:27\:\s?e|tjugosjunde)"},   # twenty seventh
    {"value": 28, "pattern": r"(?:28\:\s?e|tjugo??ttonde)"},  # twenty eighth
    {"value": 29, "pattern": r"(?:29\:\s?e|tjugonionde)"},   # twenty ninth
    {"value": 30, "pattern": r"(?:30\:\s?e|trettionde)"},    # thirtieth
    {"value": 31, "pattern": r"(?:31\:\s?e|trettiof??rsta)" } # thirty first
]

patterns["sv"]["daynames"] = [
    {"value": enums.Day.MON, "pattern": r"M??n(?:\.|dag)?"},     # Monday
    {"value": enums.Day.TUE, "pattern": r"Tis(?:\.|dag)?"},     # Tuesday
    {"value": enums.Day.WED, "pattern": r"Ons(?:\.|dag)?"},     # Wednesday
    {"value": enums.Day.THU, "pattern": r"Tors(?:\.|dag)?"},    # Thursday
    {"value": enums.Day.FRI, "pattern": r"Fre(?:\.|dag)?"},     # Friday
    {"value": enums.Day.SAT, "pattern": r"L??r(?:\.|dag)?"},     # Saturday
    {"value": enums.Day.SUN, "pattern": r"S??n(?:\.|dag)?" }     # Sunday
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
    {"value": enums.Month.DEC, "pattern": r"Dec(?:\.|ember)?" }   # December
]

patterns["sv"]["seasonnames"] = [
    {"value": enums.Season.SPRING, "pattern": r"V??r"},          # Spring
    {"value": enums.Season.SUMMER, "pattern": r"Sommar"},       # Summer
    {"value": enums.Season.AUTUMN, "pattern": r"H??st"},         # Autumn
    {"value": enums.Season.WINTER, "pattern": r"Vintern?"},    # Winter
    {"pattern": r"vinterhalv??ret"},                             # Winter half
    {"pattern": r"Sommarhalv??ret" }                             # Summer half
]

patterns["sv"]["dateprefix"] = [
    {"value": enums.DatePrefix.CIRCA, "pattern": r"cirka"},                 # circa
    {"value": enums.DatePrefix.CIRCA, "pattern": r"ungef??r"},
    {"value": enums.DatePrefix.CIRCA, "pattern": r"runt" },
    {"value": enums.DatePrefix.EARLY, "pattern": r"(?:tidigt|b??rjan av)"},  # early
    {"value": enums.DatePrefix.MID, "pattern": r"Mitten av"},               # middle
    {"value": enums.DatePrefix.LATE, "pattern": r"(?:Sen[ta]?|sentida|Slutet av)"},  # late
    {"value": enums.DatePrefix.HALF1, "pattern": r"F??rsta h??lften av"},     # first half
    {"value": enums.DatePrefix.HALF2, "pattern": r"Andra halvan"},          # second half
    {"value": enums.DatePrefix.QUARTER1, "pattern": r"f??rsta kvartalet"},   # first quarter
    {"value": enums.DatePrefix.QUARTER2, "pattern": r"andra kvartalet"},    # second quarter
    {"value": enums.DatePrefix.QUARTER3, "pattern": r"tredje kvartalet"},   # third quarter
    {"value": enums.DatePrefix.QUARTER4, "pattern": r"fj??rde kvartalet"},   # fourth quarter
    {"pattern": r"slutet av(?:\sdet)?"},    # end of
    {"pattern": r"fr??n"},                 # from
    {"pattern": r"f??re"},                 # before
    {"pattern": r"under"},                # During " in
    {"pattern": r"(?:post|etter|sedan)"}, # post " after " since
    {"pattern": r"(?:fram till|upp??t)" }   # until " by
]

patterns["sv"]["datesuffix"] = [
    {"value": enums.DateSuffix.AD, "pattern": r"(?:(?:Efter|e\.?\s?)(?:Kristus|Kr\.?|K\.?)|A\.?D\.?)"},
    {"value": enums.DateSuffix.BC, "pattern": r"(?:(?:f??re|f\.?\s?)(?:Kristus|Kr\.?|K\.?)|(?:(?:cal\.?\s)?B\.?C\.?))"},
    {"value": enums.DateSuffix.BP, "pattern": r"(?:(?:??r\s)?f??re nutid|B\.?P\.?)"},
    {"value": enums.DateSuffix.AD, "pattern": r"(?:(?:Efter|Enligt) v??r tider??kning|(?:e\.?)?v\.?t\.?|C\.?E\.?)"},
    {"value": enums.DateSuffix.BC, "pattern": r"(?:F??re v??r tider??kning|f\.?v\.?t\.?|B\.?C\.?E\.?)" }
]
 
patterns["sv"]["dateseparator"] = [
    {"pattern": r"\s?\p{Pd}\s?"},
    {"pattern": r"\s?/\s?"},
    {"pattern": r"\still\s"},
    {"pattern": r"\soch\s"},
    {"pattern": r"\se\s"}       
]

patterns["sv"]["periodnames"] = [
    {"pattern": r"Paleolitikum", "value": YearSpan(35000, -8200)},
    {"pattern": r"F??rhistorisk tid", "value": YearSpan(8200, 1050)},
    {"pattern": r"Sten??lder", "value": YearSpan(8200, -1800)},
    {"pattern": r"??ldre sten??lder", "value": YearSpan(8200, -4200)},
    {"pattern": r"Tidigmesolitikum", "value": YearSpan(8200, -7000)},
    {"pattern": r"Mellanmesolitikum", "value": YearSpan(7000, -6000)},
    {"pattern": r"Senmesolitikum", "value": YearSpan(6000, -4200)},
    {"pattern": r"Maglemosekulturen", "value": YearSpan(7500, -6000)},
    {"pattern": r"Kongemosekulturen", "value": YearSpan(6000, -5200)},
    {"pattern": r"Erteb??llekulturen", "value": YearSpan(5200, -4000)},
    {"pattern": r"Yngre sten??ldern", "value": YearSpan(3900, -1800)},
    {"pattern": r"Tidigneolitikum", "value": YearSpan(3900, -3300)},
    {"pattern": r"Mellanneolitikum", "value": YearSpan(3300, -2400)},
    {"pattern": r"Mellanneolitisk tid A", "value": YearSpan(3300, -2800)},
    {"pattern": r"Mellanneolitisk tid B", "value": YearSpan(2800, -2400)},
    {"pattern": r"Senneolitikum", "value": YearSpan(2400, -1800)},
    {"pattern": r"Trattb??garkulturen", "value": YearSpan(3900, -2400)},
    {"pattern": r"Klockb??garkultur", "value": YearSpan(3000, -2000)},
    {"pattern": r"Gropkeramisk kultur", "value": YearSpan(3200, -2300)},
    {"pattern": r"Stridsyxekulturen", "value": YearSpan(2800, -2400)},
    {"pattern": r"Brons??lder", "value": YearSpan(1800, -500)},
    {"pattern": r"??ldre brons??lder", "value": YearSpan(1800, -1100)},
    {"pattern": r"Yngre brons??lder", "value": YearSpan(1100, -500)},
    {"pattern": r"J??rn??ldern?", "value": YearSpan(500, 1050)},
    {"pattern": r"??ldre j??rn??lder", "value": YearSpan(500, 400)},
    {"pattern": r"F??rromersk j??rn??lder", "value": YearSpan(500, 0)},
    {"pattern": r"Romersk j??rn??lder", "value": YearSpan(0, 400)},
    {"pattern": r"Yngre j??rn??lder", "value": YearSpan(400, 1050)},
    {"pattern": r"Folkvandringstid", "value": YearSpan(400, 550)},
    {"pattern": r"Vendeltid", "value": YearSpan(550, 800)},
    {"pattern": r"Vikingatid", "value": YearSpan(800, 1050)},
    {"pattern": r"Historisk tid", "value": YearSpan(1050, 2000)},
    {"pattern": r"Medeltida?", "value": YearSpan(1050, 1520)},
    {"pattern": r"Tidig medeltid", "value": YearSpan(1050, 1200)},
    {"pattern": r"H??gmedeltid", "value": YearSpan(1200, 1350)},
    {"pattern": r"Senmedeltid", "value": YearSpan(1350, 1527)},
    {"pattern": r"Folkungatiden", "value": YearSpan(1250, 1363)},
    {"pattern": r"Kalmarunionen", "value": YearSpan(1397, 1523)},
    {"pattern": r"Modern tid", "value": YearSpan(1521, 2000)},
    {"pattern": r"Tidigmodern tid", "value": YearSpan(1500, 1789)},
    {"pattern": r"Vasatiden", "value": YearSpan(1521, 1654)},
    {"pattern": r"??ldre vasatiden", "value": YearSpan(1521, 1611)},
    {"pattern": r"Yngre vasatiden", "value": YearSpan(1611, 1654)},
    {"pattern": r"Karolinska tiden", "value": YearSpan(1654, 1718)},
    {"pattern": r"Stormaktstiden", "value": YearSpan(1611, 1721)},
    {"pattern": r"Frihetstiden", "value": YearSpan(1719, 1772)},
    {"pattern": r"Senmodern tid", "value": YearSpan(1789, 2000)}
]

patterns["sv"]["datespans"] = [
    {
        # Month and year
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{month}}) ({{year}})(\s{{suffix}})?".format(
            prefix = oneofp(patterns["sv"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            month = oneofp(patterns["sv"]["monthnames"]),
            year =  NUMERICYEAR,
            suffix = oneofp(patterns["sv"]["datesuffix"])
        )
    },
    {
        # Season and year
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{season}}) ({{year}})(\s{{suffix}})?".format(
            prefix = oneofp(patterns["sv"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            season = oneofp(patterns["sv"]["seasonnames"]),
            year =  NUMERICYEAR,
            suffix = oneofp(patterns["sv"]["datesuffix"])
        )
    },
    {
        # year with prefix e.g. "sedan 1850"
        "pattern": fr"({{prefix}}{{spaceordash}}?)+({{year}})(\s?{{suffix}})?".format(
            prefix = oneofp(patterns["sv"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            year =  NUMERICYEAR,
            suffix = oneofp(patterns["sv"]["datesuffix"])
        )
    },
    {
        # year with suffix e.g. "circa 8100 BCE"
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{year}})(\s?{{suffix}})".format(
            prefix = oneofp(patterns["sv"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            year =  NUMERICYEAR,
            suffix = oneofp(patterns["sv"]["datesuffix"])
        )
    },
    {
        # from year to year
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{fromYear}})(\s?{{suffix}})?{{separator}}({{prefix}}{{spaceordash}}?)*({{toYear}})(\s?{{suffix}})?\b".format(
            prefix = oneofp(patterns["sv"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            fromYear = NUMERICYEAR,
            separator = oneofp(patterns["sv"]["dateseparator"]),
            toYear = NUMERICYEAR,
            suffix = oneofp(patterns["sv"]["datesuffix"])
        )
    },
    {
        # named historical periods
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{named}})".format(
            prefix = oneofp(patterns["sv"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            named = oneofp(patterns["sv"]["periodnames"])
        )
    },
    {
        # from named to named historical periods
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{named1}}){{separator}}({{prefix}}{{spaceordash}}?)*({{named2}})".format(
            prefix = oneofp(patterns["sv"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            named1 = oneofp(patterns["sv"]["periodnames"]),
            named2 = oneofp(patterns["sv"]["periodnames"]),
            separator = oneofp(patterns["sv"]["dateseparator"]),
        )
    },
    {
        # decades e.g. "1850-talet"
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{decade}})(\s{{suffix}})?\b".format(
            prefix = oneofp(patterns["sv"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            decade = r"\b[1-9]\d{1,2}0-tal(e[nt]s?|\.)?",
            suffix = oneofp(patterns["sv"]["datesuffix"])
        )
    },
    {
        # from decade to decade e.g. e.g. ""
        "pattern": fr"\b({{prefix}}{{spaceordash}}?)*({{decade1}}){{separator}}({{prefix}}{{spaceordash}}?)*({{decade2}})\b".format(
            prefix = oneofp(patterns["sv"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            decade1 = r"\b[1-9]\d{1,2}0-tal(e[nt]s?|\.)?",
            decade2 = r"\b[1-9]\d{1,2}0-tal(e[nt]s?|\.)?",
            separator = oneofp(patterns["sv"]["dateseparator"])
        )
    },
    {
        # Ordinal century e.g. "femte ??rhundradet e.Kr." (5th century AD)
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{ordinal}}) ??rhundradet(\s{{suffix}})?".format(
            prefix = oneofp(patterns["sv"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            ordinal = oneofp(patterns["sv"]["ordinals"]),
            suffix = oneofp(patterns["sv"]["datesuffix"])
        )
    },
    {
        # Ordinal millennium e.g. "tidigt 2: a ??rtusendet e.Kr."
        "pattern": fr"({{prefix}}{{spaceordash}}?)*({{ordinal}}) ??rtusendet(\s{{suffix}})?".format(
            prefix = oneofp(patterns["sv"]["dateprefix"]),
            spaceordash = SPACEORDASH,
            ordinal = oneofp(patterns["sv"]["ordinals"]),
            suffix = oneofp(patterns["sv"]["datesuffix"])
        )
    },
]

patterns["sv"]["directions"] = [
    {"value": enums.Direction.N, "pattern": r"Norr"}, 
    {"value": enums.Direction.NE, "pattern": r"Nordost"},
    {"value": enums.Direction.E, "pattern": r"??st"},
    {"value": enums.Direction.SE, "pattern": r"Sydost"}, 
    {"value": enums.Direction.S, "pattern": r"s??der"}, 
    {"value": enums.Direction.SW, "pattern": r"Sydv??st"}, 
    {"value": enums.Direction.W, "pattern": r"v??st"}, 
    {"value": enums.Direction.NW, "pattern": r"nordv??st"}
]
