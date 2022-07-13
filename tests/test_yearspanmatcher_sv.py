# =============================================================================
# Package   : yearspans
# Module    : test-yearspanmatcher_sv.py
# Version   : Draft 0.1
# Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
# Contact   : ceri.binding@southwales.ac.uk
# Project   : ReMatch
# Summary   : Unit tests for YearSpanMatcher modules 
# Require   : 
# Imports   : unittest, relib, YearSpanMatcherSV, YearSpan
# Example   : 
# License   : http://creativecommons.org/publicdomain/zero/1.0/ [CC0]
# =============================================================================
# History
# 14/02/2020 CFB Initially created script
# =============================================================================
import unittest

import sys 
sys.path.append("..")

from yearspanmatcher.yearspan import YearSpan
from yearspanmatcher.yearspanmatcher_sv import YearSpanMatcherSV

class TestYearSpanMatcherSV(unittest.TestCase):
    matcher = YearSpanMatcherSV()

    def test_matchMonthYearAD(self):
        span = self.matcher.match("Januari 1066 e.Kr.") # January 1066 AD
        expected = "1066/1066"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchMonthYearBC(self):
        span = self.matcher.match("Januari 1066 f.Kr.") # January 1066 BC
        expected = "-1065/-1065"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchMonthYearBP(self):
        span = self.matcher.match("Januari 1066 BP") # January 1066 BP
        expected = "0934/0934"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchSeasonYearAD(self):
        span = self.matcher.match("Vår 1066 e.Kr.") # Spring 1066 AD
        expected = "1066/1066"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchSeasonYearBC(self):
        span = self.matcher.match("Vår 1066 f.Kr.") # Spring 1066 BC
        expected = "-1065/-1065"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchSeasonYearBP(self):
        span = self.matcher.match("Vår 1066 BP") # Spring 1066 BP
        expected = "0934/0934"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchCardinalCenturyAD(self):
        span = self.matcher.match("Tidigt 1100-tal e.Kr.") # Early 11th Century AD
        expected = "1001/1040"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchCardinalCenturyBC(self):
        span = self.matcher.match("Tidigt 1100-tal f.Kr.") # Early 11th Century BC
        expected = "-1099/-1059"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchOrdinalCenturyAD(self):
        span = self.matcher.match("Tidigt elfte århundrade e.Kr.") # Early Eleventh Century AD
        expected = "1001/1040"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchOrdinalCenturyBC(self):
        span = self.matcher.match("Tidigt elfte århundrade f.Kr.") # Early Eleventh Century BC
        expected = "-1099/-1059"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchCardinalToCardinalCenturyAD(self):
        span = self.matcher.match("tidigt 1000-tal till slutet av 1100-talet e.Kr.") # early 11th to late 12th century AD
        expected = "0901/1100"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchCardinalToCardinalCenturyBC(self):
        span = self.matcher.match("tidigt 1200-tal till slutet av 1100-tal f.Kr.") # early 12th to late 11th century BC
        expected = "-1199/-1000"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchOrdinalToOrdinalCenturyAD(self):
        span = self.matcher.match("tidigt elfte till slutet av tolfte århundradet e.Kr.") # early eleventh to late twelfth century AD
        expected = "1001/1200"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchOrdinalToOrdinalCenturyBC(self):
        span = self.matcher.match("tidigt tolfte till sena elfte århundradet f.Kr.") # early twelfth to late eleventh century BC
        expected = "-1199/-1000"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchOrdinalMillenniumAD(self):
        span = self.matcher.match("slutet av 1: a millenniet e.Kr.") # late 1st millennium AD
        expected = "0600/1000"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchOrdinalMillenniumBC(self):
        span = self.matcher.match("slutet av 1: a millenniet f.Kr.") # late 1st millennium BC
        expected = "-0399/0000"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchOrdinalToOrdinalMillenniumAD(self):
        span = self.matcher.match("sent 1: a till början av 2: a millenniet e.Kr.") # late 1st to early 2nd millennium AD
        expected = "0600/1400"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearWithPrefixAD(self):
        span = self.matcher.match("tidigt 1950 e.Kr.") # early 1950 AD
        expected = "1950/1950"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearWithPrefixBC(self):
        span = self.matcher.match("tidigt 1950 f.Kr.") # early 1950 BC
        expected = "-1949/-1949"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchYearWithPrefixBP(self):
        span = self.matcher.match("tidigt 1950 BP") # early 1950 BP
        expected = "0050/0050"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearWithSuffixAD(self):
        span = self.matcher.match("1950 e.Kr.") # 1950 AD
        expected = "1950/1950"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearWithSuffixBC(self):
        span = self.matcher.match("1950 f.Kr.") # 1950 BC
        expected = "-1949/-1949"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchYearWithSuffixBP(self):
        span = self.matcher.match("1950 BP") # 1950 BP
        expected = "0050/0050"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearToYear1AD(self):
        span = self.matcher.match("1255 - 7 e.Kr.") # 1255 - 7 AD
        expected = "1255/1257"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearToYear2AD(self):
        span = self.matcher.match("1250 - 57 e.Kr.") # 1250 - 57 AD
        expected = "1250/1257"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearToYear4AD(self):
        span = self.matcher.match("1200 - 1500 e.Kr.") # 1200 - 1500 AD
        expected = "1200/1500"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchYearToYearBC(self):
        span = self.matcher.match("1200 - 1500 f.Kr.") # 1200 - 1500 BC
        expected = "-1499/-1199"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearToYearBP(self):
        span = self.matcher.match("1200 - 1500 BP") # 1200 - 1500 BP
        expected = "0500/0800"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchLoneDecade(self):
        span = self.matcher.match("1950-talet") # 1950's
        expected = "1950/1959"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())    

    def test_matchDecadeToDecade(self):
        span = self.matcher.match("1950- till 1960-talet") # 1950's to 1960's
        expected = "1950/1969"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())  

    def test_matchNamedPeriod(self):
        span = self.matcher.match("Vikingatid") # Viking Age
        expected = "0800/1050"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchNamedToNamedPeriod(self):
        span = self.matcher.match("Vikingatid till medeltida") # Viking to Medieval
        expected = "0800/1520"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    
if __name__ == '__main__':
    unittest.main()
