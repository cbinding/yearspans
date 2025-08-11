# Yearspans

A utility to determine start/end years from textual expressions of year periods.
Note this is reworked based on some earlier C# .NET code (https://github.com/cbinding/timespans)

## Background

Archaeological dataset records often use a textual expression of a period rather than absolute numeric years for the dating of artefacts. These textual expressions can be in a variety of formats and different languages. There can be prefixes present such as _Circa_, _Early_, _Mid_, _Late_ - and suffixes such as _A.D._, _B.C._, _C.E._, _B.C.E._, _B.P._. This situation introduces potential problems for temporal comparison of records within a single dataset, but also presents wider data integration issues, as illustrated in the table of examples below. If we need to perform temporal comparisons on these values e.g. _filter to values earlier than 1500 CE_ or place them on a timeline - then some preprocessing work is first required in order to determine the meaning of each value:

| Category                     | Language  | Expresssion                   |
| ---------------------------- | --------- | ----------------------------- |
| Ordinal century              | Dutch     | Begin 11e eeuw voor Christus  |
|                              | English   | Circa Second Century BC       |
|                              | French    | Début du 11e siècle avant JC  |
|                              | German    | Frühes elfte Jahrhundert v    |
|                              | Italian   | XV secolo d.C.                |
|                              | Norwegian | Tidlig ellevte århundre e.Kr. |
|                              | Spanish   | Principios del siglo XI d.C.  |
|                              | Swedish   | Tidigt elfte århundrade f.Kr. |
|                              | Welsh     | Canol y 15fed ganrif          |
| Year span                    | English   | 1450-1460                     |
|                              | English   | 1485-86                       |
| Single year (with tolerance) | English   | C. 1485                       |
|                              | English   | 1540±9                        |
|                              | English   | AD400+                        |
|                              | English   | 400 AD                        |
| Decade                       | English   | Circa 1860s                   |
|                              | Italian   | intorno al decennio 1910      |
|                              | Welsh     | 1930au                        |
| Century span                 | English   | 5th – 6th century AD          |
|                              | Italian   | VIII-VII secolo a.C.          |
|                              | Welsh     | 5ed 6ed ganrif                |
| Month and year               | English   | July 1855                     |
|                              | Italian   | Luglio 1855                   |
|                              | Welsh     | Gorffennaf 1855               |
| Season and year              | English   | Summer 1855                   |
|                              | Italian   | Estate 1855                   |
|                              | Welsh     | Haf 1855                      |
| Named periods (from lookup)  | English   | Georgian                      |
|                              | English   | Victorian                     |

Normalising such data can make subsequent search and comparison of records easier and more accurate. We can do this by supplementing the original data values with additional attributes defining the start and end years. This application attempts to match such textual values against a number of predefined patterns, and from there to derive the intended start/end years. For some cases (e.g. _1450-1460_) the start/end years are already present so may be extracted directly from the text, however in most cases a degree of additional processing and calculation is required after the initial pattern match is made. The output can facilitate better comparison of textual year spans as often expressed in datasets. Due to the wide variety of possible formats (including punctuation and spurious extra text or white space), the matching patterns developed cannot comprehensively cater for every possible free-text variation, so any remaining records not processed by this initial automated method can be manually reviewed and assigned suitable start/end dates.

## Century Boundaries and Subdivisions

Centuries are considered to start at year 1 and end at year 100 (e.g. _15th Century_ = start year 1401 CE, end year 1500 CE). Prefix modifiers for centuries take the following meaning (in this application):

| Prefix         | Start | End |
| -------------- | ----: | --: |
| Early\*        |     1 |  40 |
| Mid\*          |    30 |  70 |
| Late\*         |    60 | 100 |
| First Half     |     1 |  50 |
| Second Half    |    51 | 100 |
| First Quarter  |     1 |  25 |
| Second Quarter |    26 |  50 |
| Third Quarter  |    51 |  75 |
| Fourth Quarter |    76 | 100 |

\*Note the boundaries of _Early_, _Mid_ and _Late_ overlap, suggesting that a level of approximation is intended when using such terms. However these boundaries would not apply if the match is on a PeriodO named period, where the absolute dates exactly as specified are used instead e.g. [Early 2nd Century](http://n2t.net/ark:/99152/p0kh9dspqt5) where the start year is 101 CE, the end year is *132* CE

In the case of decades, centuries or stated tolerances, an offset is added or subtracted from the initial extracted year in order to interpret the overall extents of the year span being expressed. e.g.
* _1540±9_ = start year 1531 CE, end year 1549 CE
* _Circa 1860s_ = start year 1860 CE, end year 1869 CE
* _15th century_ = start year 1401 CE, end year 1500 CE

As explained above, for matches on known named periods (e.g. _Georgian_, _Victorian_ etc.) the start/end years are always taken from the specified PeriodO authority record.

## Usage
All output years are expressed relative to Common Era (CE) as ISO 8601 compatible string values - zero padded, (minimum) 4 digits, signed when negative, with no year zero (so "0000" represents 1 BCE, "-0001" represents 2 BCE etc). 

Commands:

```python
python -m yearspanmatcher.yearspanmatcher -i "{input}" [-l "{language}"] [-p "{PeriodO authority id}"] 

python -m yearspanmatcher.yearspanmatcher -i "Early 2nd Century" -l "en" -p "p0kh9ds" 
# result: "0101/0132 (Early 2nd Century)"

python -m yearspanmatcher.yearspanmatcher -i "Principios del siglo XI d.C." -l "es" 
# result: "1001/1040 (Principios del siglo XI d.C.)" 
```

### Input (required)

The textual timespan expression to be processed. The matching patterns employed are all case insensitive, e.g. _2nd Century AD_ and _2nd century ad_ should yield identical results.

### Language (optional)

The [ISO639-1](https://www.iso.org/iso-639-language-codes.html) two character language code corresponding to the language of the input data. This hints to the underlying matching process the most appropriate matching patterns to use. Languages currently supported are:

- Czech ('cs')
- Dutch ('nl')
- English ('en') [default]
- Italian ('it')
- German ('de')
- French ('fr')
- Norwegian ('no')
- Spanish ('es')
- Swedish ('sv')
- Welsh ('cy')

If the language parameter supplied is omitted or is otherwise not one of these recognised values then the default used will be _en_ (English). For unsupported languages some of the more 'numeric' patterns may still give valid results, and the PeriodO lookups would also work if an appropriate PeriodO authority ID is passed in (see below).

### PeriodO authority ID (optional)
The [PeriodO](https://perio.do/) Authority ID to use for matching on named periods. If the parameter is omitted then an appropriate default is used according to the language specified (see Language above). If a PeriodO authority ID is present then it overrides the default for the language. The default values per language are as follows:

- cs ["p0wctqt"](http://n2t.net/ark:/99152/p0wctqt) - AMCR Periods Vocabulary
- nl ["p0pqptc"](http://n2t.net/ark:/99152/p0pqptc) - Rijksdienst voor het Cultureel Erfgoed. Het Archeologisch Basisregister (ABR)
- en ["p0kh9ds"](http://n2t.net/ark:/99152/p0kh9ds) - Historic England Archaeological and Cultural Periods
- it ["p0qhb66"](http://n2t.net/ark:/99152/p0qhb66) - ARIADNE Data Collection
- de ["p0qhb66"](http://n2t.net/ark:/99152/p0qhb66) - ARIADNE Data Collection
- fr ["p02chr4"](http://n2t.net/ark:/99152/p02chr4) - PACTOLS chronology periods used in DOLIA data
- no ["p04h98q"](http://n2t.net/ark:/99152/p04h98q) - Norsk arkeologisk leksikon
- es ["p0qhb66"](http://n2t.net/ark:/99152/p0qhb66) - ARIADNE Data Collection
- sv ["p0qhb66"](http://n2t.net/ark:/99152/p0qhb66) - ARIADNE Data Collection
- cy ["p0kh9ds"](http://n2t.net/ark:/99152/p0kh9ds) - Historic England Archaeological and Cultural Periods



### Example Output

| input                                                      | language | min year | max year |
| ---------------------------------------------------------- | -------- | -------: | -------: |
| Early 2nd Century BC                                       | en       |    -0199 |    -0159 |
| 1839-1895                                                  | en       |     1839 |     1895 |
| 1839-75                                                    | en       |     1839 |     1875 |
| c. 1521                                                    | en       |     1521 |     1521 |
| 140-144 d.C.                                               | it       |     0140 |     0144 |
| Inizio undicesimo secolo d.C.                              | it       |     1001 |     1040 |
| inizio del undicesimo alla fine del dodicesimo secolo d.C. | it       |     1001 |     1200 |
| III e lo II secolo a.C.                                    | it       |    -0299 |    -0100 |
| intorno a VI secolo d.C.                                   | it       |     0501 |     0600 |
| 575-400 a.C.                                               | it       |    -0574 |    -0399 |
| début 11ème à fin 12ème siècle après JC                    | fr       |     1001 |     1200 |
| georgienne à victorienne                                   | fr       |     1714 |     1901 |
| dechrau'r 11eg i ddiwedd y 12fed ganrif OC                 | cy       |     1001 |     1200 |
| Canoloesol i Edwardaidd                                    | cy       |     1066 |     1910 |
| Frühes elfte Jahrhundert n. Chr                            | de       |     1001 |     1040 |
| Völkerwanderungszeit                                       | de       |     0375 |     0586 |
| Principios del siglo XI a.C.                               | es       |    -1099 |    -1059 |
| finales del 1 ° a principios del 2 ° milenio d.C.          | es       |     0600 |     1400 |
| Begin 11e eeuw voor Christus                               | nl       |    -1099 |    -1059 |
| laat 1e tot begin 2e millennium na Christus                | nl       |     0600 |     1400 |
| Tidlig på 1100-tallet e.Kr.                                | no       |     1001 |     1040 |
| 1950-tallet                                                | no       |     1950 |     1959 |
| Tidigt 1100-tal f.Kr.                                      | sv       |    -1099 |    -1059 |
| 1250 - 57 e.Kr.                                            | sv       |     1250 |     1257 |
| 50. léta 20. století                                       | cs       |     1950 |     1959 |
| počátek dvanáctého až konec jedenáctého století př. n. l.  | cs       |     1199 |     1000 |

## Testing

A suite of tests using the Python _unittest_ framework are located under the _tests_ directory. There are currently 318 unit tests, covering the various categories of year span textual expressions in each supported language. If changes are made to the code base the tests can be re-run to ensure they still pass.
