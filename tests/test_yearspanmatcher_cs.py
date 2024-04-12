"""
=============================================================================
Project   : ATRIUM
Package   : yearspans
Module    : test-yearspanmatcher_cs.py
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Summary   : Unit tests for YearSpanMatcher modules
Imports   : unittest, relib, YearSPan, YearSpanMatcherCS
Example   :
License   : https://github.com/cbinding/yearspans/blob/main/LICENSE.md
=============================================================================
History
05/04/2024 CFB Initially created script
=============================================================================
"""
import unittest
from yearspanmatcher import YearSpan, YearSpanMatcherCS


class TestYearSpanMatcherCS(unittest.TestCase):
    matcher = YearSpanMatcherCS()

    def test_matchMonthYearAD(self):
        span = self.matcher.match("lednu 1066 n. l.") # January 1066 AD
        expected = "1066/1066"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())
        
    def test_matchMonthYearBC(self):
        span = self.matcher.match("lednu 1066 př. n. l.") # January 1066 BC
        expected = "-1065/-1065"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchMonthYearBP(self):
        span = self.matcher.match("lednu 1066 BP") # January 1066 BP
        expected = "0934/0934"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchSeasonYearAD(self):
        span = self.matcher.match("jaře roku 1066 n. l.") # Spring 1066 AD
        expected = "1066/1066"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchSeasonYearBC(self):
        span = self.matcher.match("jaře roku 1066 př. n. l.") # Spring 1066 BC
        expected = "-1065/-1065"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchSeasonYearBP(self):
        span = self.matcher.match("jaře roku 1066 BP") # Spring 1066 BP
        expected = "0934/0934"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchCardinalCenturyAD(self):
        span = self.matcher.match("počátek 11. století našeho letopočtu") # Early 11th century AD
        expected = "1001/1040"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchCardinalCenturyBC(self):
        span = self.matcher.match("počátek 11. století př. n. l.") # Early 11th century BC
        expected = "-1099/-1059"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchOrdinalCenturyAD(self):
        span = self.matcher.match("počátek jedenáctého století našeho letopočtu") # early eleventh century AD
        expected = "1001/1040"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchOrdinalCenturyBC(self):
        span = self.matcher.match("Počátek jedenáctého století př. n. l.") # early eleventh century BC
        expected = "-1099/-1059"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchCardinalToCardinalCenturyAD(self):
        span = self.matcher.match("počátek 11. až konec 12. století n. l.") # early 11th to late 12th century AD
        expected = "1001/1200"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchCardinalToCardinalCenturyBC(self):
        span = self.matcher.match("počátek 12. až konec 11. století př. n. l.") # early 12th to late 11th century BC
        expected = "-1199/-1000"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchOrdinalToOrdinalCenturyAD(self):
        span = self.matcher.match("počátek jedenáctého až konec dvanáctého století našeho letopočtu") #early eleventh to late twelfth century AD
        expected = "1001/1200"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchOrdinalToOrdinalCenturyBC(self):
        span = self.matcher.match("počátek dvanáctého až konec jedenáctého století př. n. l.") # early twelfth to late eleventh century BC
        expected = "-1199/-1000"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchOrdinalMillenniumAD(self):
        span = self.matcher.match("konec 1. tisíciletí našeho letopočtu") #late 1st millennium AD
        expected = "0600/1000"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchOrdinalMillenniumBC(self):
        span = self.matcher.match("konec 1. tisíciletí př. n. l.") # late 1st millennium BC
        expected = "-0399/0000"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchOrdinalToOrdinalMillenniumAD(self):
        span = self.matcher.match("konec 1. až začátek 2. tisíciletí našeho letopočtu") # late 1st to early 2nd millennium AD
        expected = "0600/1400"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearWithPrefixAD(self):
        span = self.matcher.match("počátek roku 1950 n. l.") # early 1950 AD
        expected = "1950/1950"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearWithPrefixBC(self):
        span = self.matcher.match("počátek roku 1950 př. n. l.") # early 1950 BC
        expected = "-1949/-1949"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearWithPrefixBP(self):
        span = self.matcher.match("počátek roku 1950 BP") # early 1950 BP
        expected = "0050/0050"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearWithSuffixAD(self):
        span = self.matcher.match("1950 n. l.") # 1950 AD
        expected = "1950/1950"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearWithSuffixBC(self):
        span = self.matcher.match("1950 př. n. l.") # 1950 BC
        expected = "-1949/-1949"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearWithSuffixBP(self):
        span = self.matcher.match("1950 BP") # 1950 BP
        expected = "0050/0050"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearWithTolerance1(self):
        span = self.matcher.match("1600-25+17")
        expected = "1575/1617"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearWithTolerance2(self):
        span = self.matcher.match("1600±17") # 1600±17
        expected = "1583/1617"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearToYear1AD(self):
        span = self.matcher.match("1255 - 7 n. l.") # 1255 - 7 AD
        expected = "1255/1257"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearToYear2AD(self):
        span = self.matcher.match("1250 - 57 n. l.") # 1250 - 57 AD
        expected = "1250/1257"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearToYear4AD(self):
        span = self.matcher.match("1200 - 1500 n. l.") # 1200 - 1500 AD
        expected = "1200/1500"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearToYearBC(self):
        span = self.matcher.match("1500 - 1200 př. n. l.") # 1500 - 1200 BC
        expected = "-1499/-1199"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearToYearBP(self):
        span = self.matcher.match("1200 - 1500 BP") # 1200 - 1500 BP
        expected = "0500/0800"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchLoneDecade(self):
        span = self.matcher.match("50. léta 20. století") # 1950's
        expected = "1950/1959"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchDecadeToDecade(self):
        span = self.matcher.match("50. až 60. léta 20. století") # 1950's to 1960's
        expected = "1950/1969"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchNamedPeriod(self):
        span = self.matcher.match("raný středověk 2") # http://n2t.net/ark:/99152/p0wctqtz4h3
        expected = "0651/0800"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())
    
    '''
    def test_matchNamedToNamedPeriod(self):
        span = self.matcher.match("Medieval to Edwardian")
        expected = "1066/1910"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())
    '''

if __name__ == '__main__':
    unittest.main()
