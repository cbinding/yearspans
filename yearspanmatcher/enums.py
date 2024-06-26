"""
=============================================================================
Project   : ARIADNEplus
Package   : yearspanmatcher
Module    : enums.py
Classes   : Allen, Language, DateSuffix, DatePrefix, Day, Month, Season,
            Century, Millennium, Direction
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Summary   : Enumerated values for consistency in coding
Imports   : Enum, unique
Example   : enums.Language.DE, enums.Language.DE.name, enums.Language.DE.value
License   : https://github.com/cbinding/yearspans/blob/main/LICENSE.md
=============================================================================
History
28/01/2020 CFB Initially created script (ported from Javascript prototype)
30/01/2024 CFB Lexvo URIs updated ("/code/" => "/iso639-1/")
11/04/2024 CFB Allen enum added - relationships between year spans
=============================================================================
"""
from enum import Enum, unique

# usage:
# enums.Allen.BEFORE
# enums.Allen.BEFORE.name ("BEFORE")
# enums.Allen.BEFORE.value ("before")
@unique
class Allen(Enum):
    BEFORE = "before"	
    AFTER = "after"
    MEETS = "meets"
    METBY = "metby"
    OVERLAPS = "overlaps"
    OVERLAPPEDBY = "overlapped by"
    STARTS = "starts"
    STARTEDBY = "started by"
    FINISHES = "finishes"
    FINISHEDBY = "finished by"
    WITHIN = "within"
    CONTAINS = "contains"
    EQUALS = "equals"


# usage:
# enums.Language.DE
# enums.Language.DE.name ("DE")
# enums.Language.DE.value ("http://lexvo.org/id/iso639-1/de")
@unique
class Language(Enum):
    NONE = ""
    CS = "http://lexvo.org/id/iso639-1/cs"     # Czech
    CY = "http://lexvo.org/id/iso639-1/cy"     # Welsh
    DE = "http://lexvo.org/id/iso639-1/de"     # German
    EN = "http://lexvo.org/id/iso639-1/en"     # English
    ES = "http://lexvo.org/id/iso639-1/es"     # Spanish
    FR = "http://lexvo.org/id/iso639-1/fr"     # French
    IT = "http://lexvo.org/id/iso639-1/it"     # Italian
    NL = "http://lexvo.org/id/iso639-1/nl"     # Dutch
    NO = "http://lexvo.org/id/iso639-1/no"     # Norwegian
    SV = "http://lexvo.org/id/iso639-1/sv"     # Swedish


# Enums ported from C# TimeSpanLib
# usage: enums.DateSuffix.CE
@unique
class DateSuffix(Enum):
    NONE = 0
    CE = 1
    BCE = 2
    BP = 3


# Enums ported from C# TimeSpanLib
# usage: enums.DatePrefix.EARLY
@unique
class DatePrefix(Enum):
    NONE = 0
    EARLY = 1
    EARLYMID = 2
    MID = 3
    MIDLATE = 4
    LATE = 5
    HALF1 = 6
    HALF2 = 7
    THIRD1 = 8
    THIRD2 = 9
    THIRD3 = 10
    QUARTER1 = 11
    QUARTER2 = 12
    QUARTER3 = 13
    QUARTER4 = 14
    CIRCA = 15


# Not currently used
# usage: enums.Direction.N
# enums.Direction.N.name ("N")
# enums.Direction.N.value ("http://vocab.getty.edu/aat/300078761")
@unique
class Direction(Enum):
    NONE = ""
    N = "http://vocab.getty.edu/aat/300078761"     # North
    NE = "http://vocab.getty.edu/aat/300078809"    # North East
    E = "http://vocab.getty.edu/aat/300078759"     # East
    SE = "http://vocab.getty.edu/aat/300078827"    # South East
    S = "http://vocab.getty.edu/aat/300078825"     # South
    SW = "http://vocab.getty.edu/aat/300078829"    # South West
    W = "http://vocab.getty.edu/aat/300078836"     # West
    NW = "http://vocab.getty.edu/aat/300078812"    # North West


# usage: enums.Day.MON
@unique
class Day(Enum):
    NONE = ""
    MON = "http://vocab.getty.edu/aat/300410304"   # Monday
    TUE = "http://vocab.getty.edu/aat/300410305"   # Tuesday
    WED = "http://vocab.getty.edu/aat/300410306"   # Wednesday
    THU = "http://vocab.getty.edu/aat/300410307"   # Thursday
    FRI = "http://vocab.getty.edu/aat/300410308"   # Friday
    SAT = "http://vocab.getty.edu/aat/300410309"   # Saturday
    SUN = "http://vocab.getty.edu/aat/300410310"   # Sunday


# usage: enums.Month.JAN
@unique
class Month(Enum):
    NONE = ""
    JAN = "http://vocab.getty.edu/aat/300410290"   # January
    FEB = "http://vocab.getty.edu/aat/300410291"   # February
    MAR = "http://vocab.getty.edu/aat/300410292"   # March
    APR = "http://vocab.getty.edu/aat/300410293"   # April
    MAY = "http://vocab.getty.edu/aat/300410294"   # May
    JUN = "http://vocab.getty.edu/aat/300410295"   # June
    JUL = "http://vocab.getty.edu/aat/300410296"   # July
    AUG = "http://vocab.getty.edu/aat/300410297"   # August
    SEP = "http://vocab.getty.edu/aat/300410298"   # September
    OCT = "http://vocab.getty.edu/aat/300410299"   # October
    NOV = "http://vocab.getty.edu/aat/300410300"   # November
    DEC = "http://vocab.getty.edu/aat/300410301"   # December


# usage: enums.Season.SPRING
@unique
class Season(Enum):
    NONE = ""
    SPRING = "http://vocab.getty.edu/aat/300133097"    # Spring
    SUMMER = "http://vocab.getty.edu/aat/300133099"    # Summer
    AUTUMN = "http://vocab.getty.edu/aat/300133093"    # Autumn
    WINTER = "http://vocab.getty.edu/aat/300133101"     # Winter


# usage: enums.Century.BC05
# enums.Century.BC05.value ("http://vocab.getty.edu/aat/300404525")
@unique
class Century(Enum):
    NONE = ""
    BC29 = "http://vocab.getty.edu/aat/300404549"
    BC28 = "http://vocab.getty.edu/aat/300404548"
    BC27 = "http://vocab.getty.edu/aat/300404547"
    BC26 = "http://vocab.getty.edu/aat/300404546"
    BC25 = "http://vocab.getty.edu/aat/300404545"
    BC24 = "http://vocab.getty.edu/aat/300404544"
    BC23 = "http://vocab.getty.edu/aat/300404543"
    BC22 = "http://vocab.getty.edu/aat/300404542"
    BC21 = "http://vocab.getty.edu/aat/300404541"
    BC20 = "http://vocab.getty.edu/aat/300404540"
    BC19 = "http://vocab.getty.edu/aat/300404539"
    BC18 = "http://vocab.getty.edu/aat/300404538"
    BC17 = "http://vocab.getty.edu/aat/300404537"
    BC16 = "http://vocab.getty.edu/aat/300404536"
    BC15 = "http://vocab.getty.edu/aat/300404535"
    BC14 = "http://vocab.getty.edu/aat/300404534"
    BC13 = "http://vocab.getty.edu/aat/300404533"
    BC12 = "http://vocab.getty.edu/aat/300404532"
    BC11 = "http://vocab.getty.edu/aat/300404531"
    BC10 = "http://vocab.getty.edu/aat/300404530"
    BC09 = "http://vocab.getty.edu/aat/300404529"
    BC08 = "http://vocab.getty.edu/aat/300404528"
    BC07 = "http://vocab.getty.edu/aat/300404527"
    BC06 = "http://vocab.getty.edu/aat/300404526"
    BC05 = "http://vocab.getty.edu/aat/300404525"
    BC04 = "http://vocab.getty.edu/aat/300404524"
    BC03 = "http://vocab.getty.edu/aat/300404523"
    BC02 = "http://vocab.getty.edu/aat/300404522"
    BC01 = "http://vocab.getty.edu/aat/300404518"
    AD01 = "http://vocab.getty.edu/aat/300404493"
    AD02 = "http://vocab.getty.edu/aat/300404494"
    AD03 = "http://vocab.getty.edu/aat/300404495"
    AD04 = "http://vocab.getty.edu/aat/300404496"
    AD05 = "http://vocab.getty.edu/aat/300404497"
    AD06 = "http://vocab.getty.edu/aat/300404498"
    AD07 = "http://vocab.getty.edu/aat/300404499"
    AD08 = "http://vocab.getty.edu/aat/300404500"
    AD09 = "http://vocab.getty.edu/aat/300404501"
    AD10 = "http://vocab.getty.edu/aat/300404502"
    AD11 = "http://vocab.getty.edu/aat/300404503"
    AD12 = "http://vocab.getty.edu/aat/300404504"
    AD13 = "http://vocab.getty.edu/aat/300404505"
    AD14 = "http://vocab.getty.edu/aat/300404506"
    AD15 = "http://vocab.getty.edu/aat/300404465"
    AD16 = "http://vocab.getty.edu/aat/300404510"
    AD17 = "http://vocab.getty.edu/aat/300404511"
    AD18 = "http://vocab.getty.edu/aat/300404512"
    AD19 = "http://vocab.getty.edu/aat/300404513"
    AD20 = "http://vocab.getty.edu/aat/300404514"
    AD21 = "http://vocab.getty.edu/aat/300404515"


# usage: enums.Millennium.AD02
# enums.Millennium.AD02.value ("http://vocab.getty.edu/aat/300404551")
@unique
class Millennium(Enum):
    NONE = ""
    BC15 = "http://vocab.getty.edu/aat/300404567"
    BC14 = "http://vocab.getty.edu/aat/300404566"
    BC13 = "http://vocab.getty.edu/aat/300404565"
    BC12 = "http://vocab.getty.edu/aat/300404564"
    BC11 = "http://vocab.getty.edu/aat/300404563"
    BC10 = "http://vocab.getty.edu/aat/300404562"
    BC09 = "http://vocab.getty.edu/aat/300404561"
    BC08 = "http://vocab.getty.edu/aat/300404560"
    BC07 = "http://vocab.getty.edu/aat/300404559"
    BC06 = "http://vocab.getty.edu/aat/300404558"
    BC05 = "http://vocab.getty.edu/aat/300404557"
    BC04 = "http://vocab.getty.edu/aat/300404556"
    BC03 = "http://vocab.getty.edu/aat/300404555"
    BC02 = "http://vocab.getty.edu/aat/300404553"
    BC01 = "http://vocab.getty.edu/aat/300404554"
    AD01 = "http://vocab.getty.edu/aat/300404550"
    AD02 = "http://vocab.getty.edu/aat/300404551"
    AD03 = "http://vocab.getty.edu/aat/300404552"

if __name__ == "__main__":    
    print(Season.SPRING.value)