# yearspans
Utility to determine start/end years from textual expressions of year periods. 
Note this is a Python reworking of some earlier C# .NET project work (https://github.com/cbinding/timespans)

## Background ##
Archaeological dataset records often give a textual expression of dating rather than absolute numeric years for the dating of artefacts. These textual data values can be in a variety of formats, sometimes expressed in different languages. There can be prefixes present such as 'Circa', 'Early', 'Mid', 'Late' - and suffixes such as 'A.D.', 'B.C.', 'C.E.', 'B.P.' that may influence the dates intended. This can present a data integration issue, as illustrated in the table below:

| Type | Language | Input | Min | Max |
|------|----------|-------|-----|-----|
| Ordinal named or numbered century | English | Early 2nd Century | 101 | 140 |
| | English | Circa Second Century BC | -200 | -101 |
| | Italian | XV secolo d.C. | 1401 | 1500 |
| | Italian | intorno a VI sec. d.C. | 501 | 600 |
| | Welsh | pymthegfed ganrif | 1401 | 1500 |  
| | Welsh | Canol y15fed ganrif | 1430 | 1470 |
| Year span |	English	| 1450-1460 | 1450 | 1460 |
| | English | 1485-86 | 1485 | 1486 |
| Single year (with tolerance) | English | C. 1485 | 1485 | 1485 |
| | English | 1540±9 | 1531 | 1549 |
| | English | AD400+ | 400 | 400 |
| | English | 400 AD | 400 | 400 |
| Decade | English | Circa 1860s | 1860 | 1869 |
| | Italian | intorno al decennio 1910 | 1910 | 1919 |
| | Welsh | 1930au | 1930 | 1939 |
| Century span | English | 5th – 6th century AD	| 401 | 600 |
| | Italian | VIII-VII secolo a.C. | -800 | -601 |
| | Welsh | 5ed 6ed ganrif | 401 | 600 |
| Month and year | English | July 1855 | 1855 | 1855 |
| | Italian | Luglio 1855 | 1855 | 1855 |
| | Welsh | Gorffennaf 1855 | 1855 | 1855 |
| Season and year | English | Summer 1855 | 1855 | 1855 |
| | Italian | Estate 1855 | 1855 | 1855 |
| | Welsh | Haf 1855 | 1855 | 1855 |
| Named periods (from lookup) | English | Georgian | 1714 | 1837 |
| | English | Victorian | 1837 | 1901 |
		
Normalising this data can make later search and comparison of the records easier. We can do this by supplementing the original values with additional attributes defining the start and end dates of the timespan. This application attempts to match a set of textual values representing timespans to a number of known patterns, and from there to derive the intended start/end dates of the timespan. For some cases the start/end dates are present and can be extracted directly from the textual string, however in most cases a degree of additional processing is required after the initial pattern match is made. The output facilitates the fairer comparison of textual date spans as often expressed in datasets. Due to the wide variety of formats possible (including punctuation and spurious extra text), the matching patterns developed cannot comprehensively cater for every possible free-text variation present, so any remaining records not processed by this initial automated method (start/end years are zero) can be manually reviewed and assigned suitable start/end dates.

## Century Subdivisions ##
The output dates produced are relative to Common Era (CE). Centuries are set to start at year 1 and end at year 100. Prefix modifiers for centuries take the following meaning in this application:

| Prefix | Start | End |
|--------|-------|-----|
| Early | 1 | 40 |
| Mid | 30 | 70 |
| Late | 60 | 100 |
| First Half | 1 | 50 |
| Second Half | 51 | 100 |
| First/1st Quarter | 1 | 25 |
| Second/2nd Quarter | 26 | 50 |
| Third/3rd Quarter | 51 | 75 |
| Fourth/4th Quarter | 76 | 100 |

In the case of decades, centuries or stated tolerances, an offset is added or subtracted from the initial extracted year in order to interpret the overall extents of the year span being expressed. (e.g. "1540±9" = min year 1531, max year 1549)

For matches on known named periods (e.g. Georgian, Victorian etc.) the start/end years are derived from suitable authority list lookups. 

## Usage ##
Command: python yearspanmatcher.py -i "{input}" [-l {language}] 

### Input (required) ###
The timespan expressions to be processed. The matching patterns used are case insensitive.

### Language (optional) ###
The [ISO639-1:2002](https://www.iso.org/iso-639-language-codes.html) language code corresponding to the language of the input data. This hints to the underlying matching process the most appropriate matching patterns to use. Languages supported (to a greater or lesser degree) are:

* English ('en') [default]
* Italian ('it') 
* German ('de')
* French ('fr')
* Spanish ('es')
* Swedish ('sv') 
* Welsh('cy')

If the language parameter is omitted or is not one of the recognised values then the default will be 'en' (English).

### Examples ###
---

| input | language | output |
|-------|----------|--------|
| Early 2nd Century BC | en | -0199/-0159 | 
| 1839-1895 | en | 1839/1895 |
| 1839-75 | en | 1839/1875 |
| c. 1521 | en | 1521/1521 |
| 140-144 d.C. | it | 0140/0144 |
| Inizio undicesimo secolo d.C. | it | 1001/1040 |
| III e lo II secolo a.C. | it | -0299/-0100 |
| intorno a VI secolo d.C. | it | 0501/0600 |
| tra IV e III secolo a.C. | it |  |
| 575-400 a.C. | it | -0574/-0399 |

