"""
=============================================================================
Project   : ARIADNEplus
Package   : yearspans
Module    : test-yearspanmatcher_es.py
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Summary   : Unit tests for YearSpanMatcher modules
Imports   : unittest, YearSpanMatcherES, YearSpan
Example   :
License   : https://github.com/cbinding/yearspans/blob/main/LICENSE.md
=============================================================================
History
14/02/2020 CFB Initially created script
=============================================================================
"""
import unittest

#import sys
# sys.path.append("..")

from yearspanmatcher import YearSpan, YearSpanMatcherES


class TestYearSpanMatcherES(unittest.TestCase):
    matcher = YearSpanMatcherES()

    def test_matchMonthYearAD(self):
        span = self.matcher.match("Enero de 1066 d.C.")  # January 1066 AD
        expected = "1066/1066"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchMonthYearBC(self):
        span = self.matcher.match("Enero de 1066 a.C.")  # January 1066 BC
        expected = "-1065/-1065"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchMonthYearBP(self):
        span = self.matcher.match("Enero de 1066 BP")  # January 1066 BP
        expected = "0934/0934"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchSeasonYearAD(self):
        span = self.matcher.match("Primavera 1066 d.C.")  # Spring 1066 AD
        expected = "1066/1066"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchSeasonYearBC(self):
        span = self.matcher.match("Primavera 1066 a.C.")  # Spring 1066 BC
        expected = "-1065/-1065"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchSeasonYearBP(self):
        span = self.matcher.match("Primavera 1066 BP")  # Spring 1066 BP
        expected = "0934/0934"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchOrdinalCenturyAD(self):
        # Early Eleventh Century AD
        span = self.matcher.match("Principios del siglo XI d.C.")
        expected = "1001/1040"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchOrdinalCenturyBC(self):
        # Early Eleventh Century BC
        span = self.matcher.match("Principios del siglo XI a.C.")
        expected = "-1099/-1059"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchOrdinalToOrdinalCenturyAD(self):
        # early eleventh to late twelfth century AD
        span = self.matcher.match(
            "principios del siglo XI a finales del siglo XII d.C.")
        expected = "1001/1200"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchOrdinalToOrdinalCenturyBC(self):
        # early twelfth to late eleventh century BC
        span = self.matcher.match(
            "principios del siglo XII a finales del siglo XI a.C.")
        expected = "-1199/-1000"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchOrdinalMillenniumAD(self):
        # late 1st millennium AD
        span = self.matcher.match("finales del primer milenio d.C.")
        expected = "0600/1000"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchOrdinalMillenniumBC(self):
        # late 1st millennium BC
        span = self.matcher.match("finales del primer milenio antes de Cristo")
        expected = "-0399/0000"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchOrdinalToOrdinalMillenniumAD(self):
        # late 1st to early 2nd millennium AD
        span = self.matcher.match(
            "finales del 1 ° a principios del 2 ° milenio d.C.")
        expected = "0600/1400"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearWithPrefixAD(self):
        span = self.matcher.match("principios de 1950 d.C.")  # early 1950 AD
        expected = "1950/1950"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearWithPrefixBC(self):
        span = self.matcher.match("principios de 1950 a.C.")  # early 1950 BC
        expected = "-1949/-1949"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearWithPrefixBP(self):
        span = self.matcher.match("principios de 1950 BP")  # early 1950 BP
        expected = "0050/0050"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearWithSuffixAD(self):
        span = self.matcher.match("1950 d.C.")  # 1950 AD
        expected = "1950/1950"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearWithSuffixBC(self):
        span = self.matcher.match("1950 a.C.")  # 1950 BC
        expected = "-1949/-1949"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearWithSuffixBP(self):
        span = self.matcher.match("1950 BP")  # 1950 BP
        expected = "0050/0050"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearToYear1AD(self):
        span = self.matcher.match("1255 - 7 d.C.")  # 1255 - 7 AD
        expected = "1255/1257"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearToYear2AD(self):
        span = self.matcher.match("1250 - 57 d.C.")  # 1250 - 57 AD
        expected = "1250/1257"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearToYear4AD(self):
        span = self.matcher.match("1200-1500 d.C.")  # 1200 - 1500 AD
        expected = "1200/1500"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearToYearBC(self):
        span = self.matcher.match("1500-1200 a.C.")  # 1500 - 1200 BC
        expected = "-1499/-1199"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearToYearBP(self):
        span = self.matcher.match("1200 - 1500 BP")  # 1200 - 1500 BP
        expected = "0500/0800"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchLoneDecade(self):
        span = self.matcher.match("la década de 1950")  # 1950's
        expected = "1950/1959"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchDecadeToDecade(self):
        # late 1950's to late 1960's
        span = self.matcher.match(
            "finales de la década de 1950 hasta finales de la década de 1960")
        expected = "1950/1969"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchNamedPeriod(self):
        span = self.matcher.match("Alta Edad Media")  # http://n2t.net/ark:/99152/p0qhb66m983
        expected = "0400/0699"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchNamedToNamedPeriod(self):
        span = self.matcher.match(
            "Alta Edad Media a la Baja Edad Media")  # http://n2t.net/ark:/99152/p0qhb66fp7h
        expected = "0400/1499"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())


if __name__ == '__main__':
    unittest.main()
