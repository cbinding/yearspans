# =============================================================================
# Package   : yearspans
# Module    : test_yearspanmatcher_de.py
# Version   : Draft 0.1
# Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
# Contact   : ceri.binding@southwales.ac.uk
# Project   : ReMatch
# Summary   : Unit tests for YearSpanMatcher modules 
# Require   : 
# Imports   : unittest, relib, YearSpanMatcherXX, YearSpan
# Example   : 
# License   : http://creativecommons.org/publicdomain/zero/1.0/ [CC0]
# =============================================================================
# History
# 14/02/2020 CFB Initially created script
# =============================================================================
import unittest

#import sys 
#sys.path.append("..")

from yearspanmatcher import YearSpan, YearSpanMatcherDE

class TestYearSpanMatcherDE(unittest.TestCase):
    matcher = YearSpanMatcherDE()

    def test_matchMonthYearAD(self):
        span = self.matcher.match("Januar 1066 n. Chr") # January 1066 AD
        expected = "1066/1066"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchMonthYearBC(self):
        span = self.matcher.match("Januar 1066 v") # January 1066 BC
        expected = "-1065/-1065"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchMonthYearBP(self):
        span = self.matcher.match("Januar 1066 BP") # Jabuary 1066 BP
        expected = "0934/0934"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchSeasonYearAD(self):
        span = self.matcher.match("Frühling 1066 n. Chr") # Spring 1066 AD
        expected = "1066/1066"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchSeasonYearBC(self):
        span = self.matcher.match("Frühling 1066 v") # Spring 1066 BC
        expected = "-1065/-1065"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchSeasonYearBP(self):
        span = self.matcher.match("Frühling 1066 BP") # Spring 1066 BP
        expected = "0934/0934"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchCardinalCenturyAD(self):
        span = self.matcher.match("Frühes 11. Jahrhundert n. Chr") # Early 11th Century AD
        expected = "1001/1040"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchCardinalCenturyBC(self):
        span = self.matcher.match("Frühes 11. Jahrhundert v") # Early 11th Century BC
        expected = "-1099/-1059"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchOrdinalCenturyAD(self):
        span = self.matcher.match("Frühes elfte Jahrhundert n. Chr") # Early Eleventh Century AD
        expected = "1001/1040"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchOrdinalCenturyBC(self):
        span = self.matcher.match("Frühes elfte Jahrhundert v") # Early Eleventh Century BC
        expected = "-1099/-1059"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchCardinalToCardinalCenturyAD(self):
        span = self.matcher.match("frühes 11. bis spätes 12. Jahrhundert n. Chr") # early 11th to late 12th century AD
        expected = "1001/1200"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchCardinalToCardinalCenturyBC(self):
        span = self.matcher.match("frühes 12. bis spätes 11. Jahrhundert v") # early 12th to late 11th century BC
        expected = "-1199/-1000"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchOrdinalToOrdinalCenturyAD(self):
        span = self.matcher.match("frühes elftes bis spätes zwölftes Jahrhundert n. Chr") # early eleventh to late twelfth century AD
        expected = "1001/1200"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchOrdinalToOrdinalCenturyBC(self):
        span = self.matcher.match("frühes zwölftes bis spätes elftes Jahrhundert v") # early twelfth to late eleventh century BC
        expected = "-1199/-1000"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchOrdinalMillenniumAD(self):
        span = self.matcher.match("spätes 1. Jahrtausend n. Chr") # late 1st millennium AD
        expected = "0600/1000"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchOrdinalMillenniumBC(self):
        span = self.matcher.match("Ende des 1. Jahrtausends vor Christus") # late 1st millennium BC
        expected = "-0399/0000"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchOrdinalToOrdinalMillenniumAD(self):
        span = self.matcher.match("spätes 1. bis frühes 2. Jahrtausend n. Chr") # late 1st to early 2nd millennium AD
        expected = "0600/1400"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearWithPrefixAD(self):
        span = self.matcher.match("Anfang 1950 n. Chr") # early 1950 AD
        expected = "1950/1950"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearWithPrefixBC(self):
        span = self.matcher.match("Anfang 1950 v") # early 1950 BC
        expected = "-1949/-1949"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchYearWithPrefixBP(self):
        span = self.matcher.match("Anfang 1950 BP") #early 1950 BP
        expected = "0050/0050"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearWithSuffixAD(self):
        span = self.matcher.match("1950 n. Chr") # 1950 AD
        expected = "1950/1950"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearWithSuffixBC(self):
        span = self.matcher.match("1950 v") # 1950 BC
        expected = "-1949/-1949"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchYearWithSuffixBP(self):
        span = self.matcher.match("1950 BP") # 1950 BP
        expected = "0050/0050"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearToYearAD(self):
        span = self.matcher.match("1200 bis 1500 n. Chr") # 1200 to 1500 AD
        expected = "1200/1500"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchYearToYearBC(self):
        span = self.matcher.match("1500 bis 1200 v") # 1500 to 1200 BC"
        expected = "-1499/-1199"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearToYearBP(self):
        span = self.matcher.match("1200 bis 1500 BP") # 1200 to 1500 BP
        expected = "0500/0800"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchLoneDecade(self):
        span = self.matcher.match("1950er Jahre") # 1950's
        expected = "1950/1959"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())    

    def test_matchDecadeToDecade(self):
        span = self.matcher.match("1950er bis 1960er Jahre") # 1950's to 1960's
        expected = "1950/1969"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())  

    def test_matchNamedPeriod(self):
        span = self.matcher.match("Völkerwanderungszeit") # Migration period
        expected = "0375/0586"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchNamedToNamedPeriod(self):
        span = self.matcher.match("Völkerwanderungszeit bit Mittelalter") # Migration to Medieval
        expected = "0375/1500"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())        

    
if __name__ == '__main__':
    unittest.main()
