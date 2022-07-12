# =============================================================================
# Package   : yearspans
# Module    : test-yearspanmatcher_nl.py
# Version   : Draft 0.1
# Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
# Contact   : ceri.binding@southwales.ac.uk
# Project   : ReMatch
# Summary   : Unit tests for YearSpanMatcher modules 
# Require   : 
# Imports   : unittest, relib, YearSpanMatcherNL, YearSpan
# Example   : 
# License   : http://creativecommons.org/publicdomain/zero/1.0/ [CC0]
# =============================================================================
# History
# 14/02/2020 CFB Initially created script
# =============================================================================
import unittest
from yearspan import YearSpan
from yearspanmatcher_nl import YearSpanMatcherNL

class TestYearSpanMatcherNL(unittest.TestCase):
    matcher = YearSpanMatcherNL()

    def test_matchMonthYearAD(self):
        span = self.matcher.match("Januari 1066 na Christus") # January 1066 AD
        expected = "1066/1066"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchMonthYearBC(self):
        span = self.matcher.match("Januari 1066 voor Christus") # January 1066 BC
        expected = "-1065/-1065"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchMonthYearBP(self):
        span = self.matcher.match("Januari 1066 BP") # January 1066 BP
        expected = "0934/0934"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchSeasonYearAD(self):
        span = self.matcher.match("Lente 1066 na Christus") # Spring 1066 AD
        expected = "1066/1066"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchSeasonYearBC(self):
        span = self.matcher.match("Lente 1066 voor Christus") # Spring 1066 BC
        expected = "-1065/-1065"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchSeasonYearBP(self):
        span = self.matcher.match("Lente 1066 BP") #Spring 1066 BP
        expected = "0934/0934"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchCardinalCenturyAD(self):
        span = self.matcher.match("Begin 11e eeuw na Christus") # Early 11th Century AD
        expected = "1001/1040"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchCardinalCenturyBC(self):
        span = self.matcher.match("Begin 11e eeuw voor Christus") # Early 11th Century BC
        expected = "-1099/-1059"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchOrdinalCenturyAD(self):
        span = self.matcher.match("Begin elfde eeuw na Christus") # Early Eleventh Century AD
        expected = "1001/1040"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchOrdinalCenturyBC(self):
        span = self.matcher.match("Begin elfde eeuw voor Christus")  # Early Eleventh Century BC
        expected = "-1099/-1059"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchCardinalToCardinalCenturyAD(self):
        span = self.matcher.match("begin 11e tot eind 12e eeuw na Christus") # early 11th to late 12th century AD
        expected = "1001/1200"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchCardinalToCardinalCenturyBC(self):
        span = self.matcher.match("begin 12e tot eind 11e eeuw voor Christus") # early 12th to late 11th century BC
        expected = "-1199/-1000"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchOrdinalToOrdinalCenturyAD(self):
        span = self.matcher.match("begin elfde tot eind twaalfde eeuw na Christus") # early eleventh to late twelfth century AD
        expected = "1001/1200"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchOrdinalToOrdinalCenturyBC(self):
        span = self.matcher.match("begin twaalfde tot eind elfde eeuw voor Christus") # early twelfth to late eleventh century BC
        expected = "-1199/-1000"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchOrdinalMillenniumAD(self):
        span = self.matcher.match("laat 1e millennium na Christus") # late 1st millennium AD
        expected = "0600/1000"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchOrdinalMillenniumBC(self):
        span = self.matcher.match("laat 1e millennium voor Christus") # late 1st millennium BC
        expected = "-0399/0000"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchOrdinalToOrdinalMillenniumAD(self):
        span = self.matcher.match("laat 1e tot begin 2e millennium na Christus") # late 1st to early 2nd millennium AD
        expected = "0600/1400"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearWithPrefixAD(self):
        span = self.matcher.match("begin 1950 na Christus") # early 1950 AD
        expected = "1950/1950"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearWithPrefixBC(self):
        span = self.matcher.match("begin 1950 voor Christus") # early 1950 BC
        expected = "-1949/-1949"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchYearWithPrefixBP(self):
        span = self.matcher.match("begin 1950 BP")  # early 1950 BP
        expected = "0050/0050"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearWithSuffixAD(self):
        span = self.matcher.match("1950 na Christus") # 1950 AD
        expected = "1950/1950"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearWithSuffixBC(self):
        span = self.matcher.match("1950 voor Christus") # 1950 BC
        expected = "-1949/-1949"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchYearWithSuffixBP(self):
        span = self.matcher.match("1950 BP") # 1950 BP
        expected = "0050/0050"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearToYear1AD(self):
        span = self.matcher.match("1255-7 n.Chr") # 1255 - 7 AD
        expected = "1255/1257"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearToYear2AD(self):
        span = self.matcher.match("1250 - 57 n.Chr") # 1250 - 57 AD
        expected = "1250/1257"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearToYear4AD(self):
        span = self.matcher.match("1200 - 1500 na Christus") # 1200 - 1500 AD
        expected = "1200/1500"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchYearToYearBC(self):
        span = self.matcher.match("1500 - 1200 voor Christus") # 1500 - 1200 BC
        expected = "-1499/-1199"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearToYearBP(self):
        span = self.matcher.match("1200 - 1500 BP") # 1200 - 1500 BP
        expected = "0500/0800"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchLoneDecade(self):
        span = self.matcher.match("jaren 1850") # 1850's
        expected = "1850/1859"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())    

    def test_matchDecadeToDecade(self):
        span = self.matcher.match("jaren 1850 tot 1860") # 1950's to 1960's
        expected = "1850/1869"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())  

    def test_matchNamedPeriod(self):
        span = self.matcher.match("Romeinse") # Roman
        expected = "-0011/0449"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchNamedToNamedPeriod(self):
        span = self.matcher.match("Romeins tot middeleeuws") # Roman to Medieval
        expected = "-0011/1499"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())


if __name__ == '__main__':
    unittest.main()
