# =============================================================================
# Package   : yearspans
# Module    : test_yearspanmatcher_fr.py
# Version   : Draft 0.1
# Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
# Contact   : ceri.binding@southwales.ac.uk
# Project   : ReMatch
# Summary   : Unit tests for YearSpanMatcher modules 
# Require   : 
# Imports   : unittest, YearSpan, YearSpanMatcherXX, 
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
from yearspanmatcher.yearspanmatcher_fr import YearSpanMatcherFR

class TestYearSpanMatcherFR(unittest.TestCase):
    matcher = YearSpanMatcherFR()

    def test_matchMonthYearAD(self):
        span = self.matcher.match("janvier 1066 AD")
        expected = "1066/1066"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchMonthYearBC(self):
        span = self.matcher.match("janvier 1066 BC")
        expected = "-1065/-1065"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchMonthYearBP(self):
        span = self.matcher.match("janvier 1066 BP")
        expected = "0934/0934"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchSeasonYearAD(self):
        span = self.matcher.match("printemps 1066 AD")
        expected = "1066/1066"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchSeasonYearBC(self):
        span = self.matcher.match("printemps 1066 BC")
        expected = "-1065/-1065"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchSeasonYearBP(self):
        span = self.matcher.match("printemps 1066 BP")
        expected = "0934/0934"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchCardinalCenturyAD(self):
        span = self.matcher.match("D??but du 11e si??cle apr??s JC")
        expected = "1001/1040"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchCardinalCenturyBC(self):
        span = self.matcher.match("D??but du 11e si??cle avant JC")
        expected = "-1099/-1059"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchOrdinalCenturyAD(self):
        span = self.matcher.match("d??but du XIe si??cle apr??s JC")
        expected = "1001/1040"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchOrdinalCenturyBC(self):
        span = self.matcher.match("D??but du XIe si??cle av.")
        expected = "-1099/-1059"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchCardinalToCardinalCenturyAD(self):
        span = self.matcher.match("d??but 11??me ?? fin 12??me si??cle apr??s JC")
        expected = "1001/1200"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchCardinalToCardinalCenturyBC(self):
        span = self.matcher.match("d??but du XIIe ?? la fin du XIe si??cle av.")
        expected = "-1199/-1000"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchOrdinalToOrdinalCenturyAD(self):
        span = self.matcher.match("d??but du XIe ?? la fin du XIIe si??cle apr??s JC")
        expected = "1001/1200"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchOrdinalToOrdinalCenturyBC(self):
        span = self.matcher.match("d??but du XIIe ?? la fin du XIe si??cle av.")
        expected = "-1199/-1000"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchOrdinalMillenniumAD(self):
        span = self.matcher.match("fin du 1er mill??naire apr??s JC")
        expected = "0600/1000"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchOrdinalMillenniumBC(self):
        span = self.matcher.match("fin du 1er mill??naire avant JC")
        expected = "-0399/0000"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchOrdinalToOrdinalMillenniumAD(self):
        span = self.matcher.match("fin du 1er au d??but du 2e mill??naire apr??s JC")
        expected = "0600/1400"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearWithPrefixAD(self):
        span = self.matcher.match("d??but 1950 AD")
        expected = "1950/1950"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearWithPrefixBC(self):
        span = self.matcher.match("d??but 1950 avant JC")
        expected = "-1949/-1949"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchYearWithPrefixBP(self):
        span = self.matcher.match("d??but 1950 BP")
        expected = "0050/0050"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearWithSuffixAD(self):
        span = self.matcher.match("1950 AD")
        expected = "1950/1950"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearWithSuffixBC(self):
        span = self.matcher.match("1950 av. JC")
        expected = "-1949/-1949"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchYearWithSuffixBP(self):
        span = self.matcher.match("1950 BP")
        expected = "0050/0050"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearToYearAD(self):
        span = self.matcher.match("1200 ?? 1500 AD")
        expected = "1200/1500"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())
    
    def test_matchYearToYearBC(self):
        span = self.matcher.match("1500 ?? 1200 avant JC")
        expected = "-1499/-1199"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearToYearBP(self):
        span = self.matcher.match("1200 ?? 1500 BP")
        expected = "0500/0800"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchLoneDecade(self):
        span = self.matcher.match("les ann??es 1950")
        expected = "1950/1959"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())    

    def test_matchDecadeToDecade(self):
        span = self.matcher.match("Ann??es 1950 ?? 1960")
        expected = "1950/1969"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())  

    def test_matchNamedPeriod(self):
        span = self.matcher.match("georgienne")
        expected = "1714/1837"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchNamedToNamedPeriod(self):
        span = self.matcher.match("georgienne ?? victorienne")
        expected = "1714/1901"  
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())


if __name__ == '__main__':
    unittest.main()
