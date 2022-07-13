# yearspans
Utility to determine start/end years from textual expressions of year periods. 
Note this is a Python reworking of some earlier C# .NET project work (https://github.com/cbinding/timespans)

## Background ##
Archaeological dataset records often use a textual expression of dating rather than absolute numeric years for the dating of artefacts. These textual data values can be in a variety of formats and different languages. There can be prefixes present such as 'Circa', 'Early', 'Mid', 'Late' - and suffixes such as 'A.D.', 'B.C.', 'C.E.', 'B.C.E.', 'B.P.' that may influence the dates intended. This situation presents potential problems for temporal comparison of records in a single dataset, but also introduces wider data integration issues, as illustrated in the table below:

| Category | Language | Expresssion |
|------|----------|-------------|
| Ordinal century | Dutch | Begin 11e eeuw voor Christus |
| | English | Circa Second Century BC |
| | French | Début du 11e siècle avant JC |
| | German | Frühes elfte Jahrhundert v |
| | Italian | XV secolo d.C. |
| | Norwegian | Tidlig ellevte århundre e.Kr. |
| | Spanish | Principios del siglo XI d.C. |
| | Swedish | Tidigt elfte århundrade f.Kr. |
| | Welsh | Canol y 15fed ganrif | 
| Year span | English | 1450-1460 | 
| | English | 1485-86 | 
| Single year (with tolerance) | English | C. 1485 | 
| | English | 1540±9 | 
| | English | AD400+ | 
| | English | 400 AD | 
| Decade | English | Circa 1860s | 
| | Italian | intorno al decennio 1910 | 
| | Welsh | 1930au | 
| Century span | English | 5th – 6th century AD	| 
| | Italian | VIII-VII secolo a.C. | 
| | Welsh | 5ed 6ed ganrif | 
| Month and year | English | July 1855 | 
| | Italian | Luglio 1855 | 
| | Welsh | Gorffennaf 1855 | 
| Season and year | English | Summer 1855 | 
| | Italian | Estate 1855 | 
| | Welsh | Haf 1855 | 
| Named periods (from lookup) | English | Georgian | 
| | English | Victorian | 
		
Normalising such data can make subsequent search and comparison of records easier and more accurate. We can do this by supplementing the original data values with additional attributes defining the start and end dates of the timespan. This application attempts to match textual values representing timespans to a number of known patterns, and from there to derive the intended start/end dates of the timespan. For some cases the start/end dates are present and may be extracted directly from the textual string, however in most cases a degree of additional processing is required after the initial pattern match is made. The output facilitates better comparison of textual date spans as often expressed in datasets. Due to the wide variety of possible formats (including punctuation and spurious extra text or white space), the matching patterns developed cannot comprehensively cater for every possible free-text variation present, so any remaining records not processed by this initial automated method can be manually reviewed and assigned suitable start/end dates.

## Century Subdivisions ##
The output dates produced are derived relative to Common Era (CE). Centuries are considered to start at year 1 and end at year 100. Prefix modifiers for centuries take the following meaning (in this application):

| Prefix | Start |  End  |
|--------|------:|------:|
| Early* | 1 | 40 |
| Mid*| 30 | 70 |
| Late* | 60 | 100 |
| First Half | 1 | 50 |
| Second Half | 51 | 100 |
| First Quarter | 1 | 25 |
| Second Quarter | 26 | 50 |
| Third Quarter | 51 | 75 |
| Fourth Quarter | 76 | 100 |

*Note the boundaries of 'Early' 'Mid' and 'Late' overlap, suggesting a level of approximation when using such terms.

In the case of decades, centuries or stated tolerances, an offset is added or subtracted from the initial extracted year in order to interpret the overall extents of the year span being expressed. (e.g. "1540±9" = start year 1531, end year 1549)

For matches on known named periods (e.g. Georgian, Victorian etc.) the start/end years are derived from suitable authority list lookups. 

## Usage ##
Command: 
```python
python3 yearspanmatcher.py -i "{input}" [-l "{language}"]
python3 yearspanmatcher.py -i "Early 2nd Century" -l "en"
```

### Input (required) ###
The timespan expression to be processed. The matching patterns employed are all case insensitive, e.g. "2nd Century AD" and "2nd century ad" would yield identical results.

### Language (optional) ###
The [ISO639-1:2002](https://www.iso.org/iso-639-language-codes.html) language code corresponding to the language of the input data. This hints to the underlying matching process the most appropriate matching patterns to use. Languages currently supported (to a greater or lesser degree) are:

* English ('en') [default]
* Italian ('it') 
* German ('de')
* French ('fr')
* Spanish ('es')
* Swedish ('sv') 
* Welsh('cy')

If the language parameter is omitted or is not one of the recognised values then the default will be 'en' (English).

### Example Output ###

| input | language | min year | max year |
|-------|----------|---------:|---------:|
| Early 2nd Century BC | en | -0199 | -0159 |
| 1839-1895 | en | 1839 | 1895 |
| 1839-75 | en | 1839 | 1875 |
| c. 1521 | en | 1521 | 1521 |
| 140-144 d.C. | it | 0140 | 0144 |
| Inizio undicesimo secolo d.C. | it | 1001 | 1040 |
| inizio del undicesimo alla fine del dodicesimo secolo d.C. | it | 1001 | 1200 |
| III e lo II secolo a.C. | it | -0299 | -0100 |
| intorno a VI secolo d.C. | it | 0501 | 0600 |
| 575-400 a.C. | it | -0574 | -0399 |
| début 11ème à fin 12ème siècle après JC | fr | 1001 | 1200 |
| georgienne à victorienne | fr | 1714 | 1901 |
| dechrau'r 11eg i ddiwedd y 12fed ganrif OC | cy | 1001 | 1200 |
| Canoloesol i Edwardaidd | cy | 1066 | 1910 |
| Frühes elfte Jahrhundert n. Chr | de | 1001 | 1040 |
| Völkerwanderungszeit | de | 0375 | 0586 |
| Principios del siglo XI a.C. | es | -1099 | -1059 |
| finales del 1 ° a principios del 2 ° milenio d.C. | es | 0600 | 1400 |
| Begin 11e eeuw voor Christus | nl | -1099 | -1059 |
| laat 1e tot begin 2e millennium na Christus | nl | 0600 | 1400 |
| Tidlig på 1100-tallet e.Kr. | no | 1001 | 1040 |
| 1950-tallet | no | 1950 | 1959 |
| Tidigt 1100-tal f.Kr. | sv | -1099 | -1059 |
| 1250 - 57 e.Kr. | sv | 1250 | 1257 |


## Testing ##
A suite of tests using the Python 'unittest' framework are located under the 'tests' directory. There are 280 tests in all, covering the various categories of year span textual expressions in each supported language.