"""
=============================================================================
Project   : ARIADNEplus
Package   : yearspans
Module    : test_yearspanmatcher_cy.py
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Summary   : Unit tests for YearSpanMatcher modules
Imports   : unittest, YearSpanMatcherCY, YearSpan
Example   :
License   : https://creativecommons.org/licenses/by/4.0/ [CC BY 4.0]
=============================================================================
History
14/02/2020 CFB Initially created script
=============================================================================
"""
import unittest
from yearspanmatcher import YearSpanMatcherCY, YearSpan


class TestYearSpanMatcherCY(unittest.TestCase):
    matcher = YearSpanMatcherCY()

    def test_matchMonthYearAD(self):
        span = self.matcher.match("Ionawr 1066 OC")  # January 1066 AD
        expected = "1066/1066"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchMonthYearBC(self):
        span = self.matcher.match("Ionawr 1066 CC")  # January 1066 BC
        expected = "-1065/-1065"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchMonthYearBP(self):
        span = self.matcher.match("Ionawr 1066 CP")  # January 1066 BP
        expected = "0934/0934"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchSeasonYearAD(self):
        span = self.matcher.match("Haf 1066 OC")  # Summer 1066 AD
        expected = "1066/1066"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchSeasonYearBC(self):
        span = self.matcher.match("Haf 1066 CC")  # Summer 1066 BC
        expected = "-1065/-1065"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchSeasonYearBP(self):
        span = self.matcher.match("Haf 1066 CP")  # Summer 1066 BP
        expected = "0934/0934"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchCardinalCenturyAD(self):
        # early 11th century AD
        span = self.matcher.match("dechrau'r 11eg ganrif OC")
        expected = "1001/1040"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchCardinalCenturyBC(self):
        # early 11th century BC
        span = self.matcher.match("dechrau'r 11eg ganrif CC")
        expected = "-1099/-1059"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchOrdinalCenturyAD(self):
        # early 11th century AD
        span = self.matcher.match("Dechrau'r unfed ar ddeg ganrif OC")
        expected = "1001/1040"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchOrdinalCenturyBC(self):
        # early 11th century BC
        span = self.matcher.match("Dechrau'r unfed ar ddeg ganrif CC")
        expected = "-1099/-1059"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchCardinalToCardinalCenturyAD(self):
        # early 11th to late 12th century AD
        span = self.matcher.match("dechrau'r 11eg i ddiwedd y 12fed ganrif OC")
        expected = "1001/1200"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchCardinalToCardinalCenturyBC(self):
        # early twelfth to late eleventh century BC
        span = self.matcher.match("dechrau'r 11eg i ddiwedd y 12fed ganrif CC")
        expected = "-1100/-1099"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchOrdinalToOrdinalCenturyAD(self):
        # early eleventh to late twelfth century AD
        span = self.matcher.match(
            "dechrau'r unfed ar ddeg ganrif a diwedd y ddeuddegfed ganrif OC")
        expected = "1001/1200"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchOrdinalToOrdinalCenturyBC(self):
        # early twelfth to late eleventh century BC
        span = self.matcher.match(
            "dechrau'r ddeuddegfed ganrif i ddiwedd yr unfed ar ddeg ganrif CC")
        expected = "-1199/-1000"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchCardinalMillenniumAD(self):
        # late 1st millennium AD
        span = self.matcher.match("diwedd y mileniwm 1af OC")
        expected = "0600/1000"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchCardinalMillenniumBC(self):
        # late 1st millennium BC
        span = self.matcher.match("diwedd y mileniwm 1af CC")
        expected = "-0399/0000"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchOrdinalMillenniumAD(self):
        # late first millennium AD
        span = self.matcher.match("diwedd y mileniwm cyntaf OC")
        expected = "0600/1000"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchOrdinalMillenniumBC(self):
        # late first millennium BC
        span = self.matcher.match("diwedd y mileniwm cyntaf CC")
        expected = "-0399/0000"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchOrdinalToOrdinalMillenniumAD(self):
        # late 1st to early 2nd millennium AD
        span = self.matcher.match("diwedd y 1af i ddechrau'r 2il mileniwm OC")
        expected = "0600/1400"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearWithPrefixAD(self):
        span = self.matcher.match("dechrau 1950 OC")  # early 1950 AD
        expected = "1950/1950"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearWithPrefixBC(self):
        span = self.matcher.match("dechrau 1950 CC")  # early 1950 BC
        expected = "-1949/-1949"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearWithPrefixBP(self):
        span = self.matcher.match("dechrau 1950 CP")  # early 1950 BP
        expected = "0050/0050"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearWithSuffixAD(self):
        span = self.matcher.match("1950 OC")  # 1950 AD
        expected = "1950/1950"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearWithSuffixBC(self):
        span = self.matcher.match("1950 CC")  # 1950 BC
        expected = "-1949/-1949"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearWithSuffixBP(self):
        span = self.matcher.match("1950 CP")  # 1000 BP
        expected = "0050/0050"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearToYearAD(self):
        span = self.matcher.match("1200 i 1500 OC")  # 1200 to 1500 AD
        expected = "1200/1500"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearToYearBC(self):
        span = self.matcher.match("1500 i 1200 CC")  # 1200 to 1500 BC
        expected = "-1499/-1199"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearToYearBP(self):
        span = self.matcher.match("1200 i 1500 CP")  # 1200 to 1500 BP
        expected = "0500/0800"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchLoneDecade(self):
        span = self.matcher.match("1950au")  # 1950's
        expected = "1950/1959"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchDecadeToDecade(self):
        span = self.matcher.match("1950au i 1960au")  # 1950's to 1960's
        expected = "1950/1969"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchNamedPeriod(self):
        span = self.matcher.match("Edwardaidd")  # Edwardian
        expected = "1902/1910"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchNamedToNamedPeriod(self):
        # Medieval to Edwardian
        span = self.matcher.match("Canoloesol i Edwardaidd")
        expected = "1066/1910"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())


if __name__ == '__main__':
    unittest.main()
