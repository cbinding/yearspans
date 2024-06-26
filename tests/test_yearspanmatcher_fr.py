"""
=============================================================================
Project   : ARIADNEplus
Package   : yearspans
Module    : test_yearspanmatcher_fr.py
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Summary   : Unit tests for YearSpanMatcher modules
Imports   : unittest, YearSpan, YearSpanMatcherFT,
Example   :
License   : https://github.com/cbinding/yearspans/blob/main/LICENSE.md
=============================================================================
History
14/02/2020 CFB Initially created script
=============================================================================
"""
import unittest
from yearspanmatcher import YearSpan, YearSpanMatcherFR


class TestYearSpanMatcherFR(unittest.TestCase):
    matcher = YearSpanMatcherFR()

    def test_matchMonthYearAD(self):
        span = self.matcher.match("janvier 1066 AD")
        expected = "1066/1066"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchMonthYearBC(self):
        span = self.matcher.match("janvier 1066 BC")
        expected = "-1065/-1065"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchMonthYearBP(self):
        span = self.matcher.match("janvier 1066 BP")
        expected = "0934/0934"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchSeasonYearAD(self):
        span = self.matcher.match("printemps 1066 AD")
        expected = "1066/1066"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchSeasonYearBC(self):
        span = self.matcher.match("printemps 1066 BC")
        expected = "-1065/-1065"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchSeasonYearBP(self):
        span = self.matcher.match("printemps 1066 BP")
        expected = "0934/0934"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchCardinalCenturyAD(self):
        span = self.matcher.match("Début du 11e siècle après JC")
        expected = "1001/1040"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchCardinalCenturyBC(self):
        span = self.matcher.match("Début du 11e siècle avant JC")
        expected = "-1099/-1059"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchOrdinalCenturyAD(self):
        span = self.matcher.match("début du XIe siècle après JC")
        expected = "1001/1040"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchOrdinalCenturyBC(self):
        span = self.matcher.match("Début du XIe siècle av.")
        expected = "-1099/-1059"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchCardinalToCardinalCenturyAD(self):
        span = self.matcher.match("début 11ème à fin 12ème siècle après JC")
        expected = "1001/1200"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchCardinalToCardinalCenturyBC(self):
        span = self.matcher.match("début du XIIe à la fin du XIe siècle av.")
        expected = "-1199/-1000"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchOrdinalToOrdinalCenturyAD(self):
        span = self.matcher.match(
            "début du XIe à la fin du XIIe siècle après JC")
        expected = "1001/1200"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchOrdinalToOrdinalCenturyBC(self):
        span = self.matcher.match("début du XIIe à la fin du XIe siècle av.")
        expected = "-1199/-1000"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchOrdinalMillenniumAD(self):
        span = self.matcher.match("fin du 1er millénaire après JC")
        expected = "0600/1000"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchOrdinalMillenniumBC(self):
        span = self.matcher.match("fin du 1er millénaire avant JC")
        expected = "-0399/0000"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchOrdinalToOrdinalMillenniumAD(self):
        span = self.matcher.match(
            "fin du 1er au début du 2e millénaire après JC")
        expected = "0600/1400"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearWithPrefixAD(self):
        span = self.matcher.match("début 1950 AD")
        expected = "1950/1950"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearWithPrefixBC(self):
        span = self.matcher.match("début 1950 avant JC")
        expected = "-1949/-1949"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearWithPrefixBP(self):
        span = self.matcher.match("début 1950 BP")
        expected = "0050/0050"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearWithSuffixAD(self):
        span = self.matcher.match("1950 AD")
        expected = "1950/1950"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearWithSuffixBC(self):
        span = self.matcher.match("1950 av. JC")
        expected = "-1949/-1949"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearWithSuffixBP(self):
        span = self.matcher.match("1950 BP")
        expected = "0050/0050"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearToYearAD(self):
        span = self.matcher.match("1200 à 1500 AD")
        expected = "1200/1500"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearToYearBC(self):
        span = self.matcher.match("1500 à 1200 avant JC")
        expected = "-1499/-1199"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearToYearBP(self):
        span = self.matcher.match("1200 à 1500 BP")
        expected = "0500/0800"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchLoneDecade(self):
        span = self.matcher.match("les années 1950")
        expected = "1950/1959"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchDecadeToDecade(self):
        span = self.matcher.match("Années 1950 à 1960")
        expected = "1950/1969"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchNamedPeriod(self):
        span = self.matcher.match("Renaissance")
        expected = "1500/1699"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchNamedToNamedPeriod(self):
        span = self.matcher.match("XIe siècle à XIIe siècle")
        expected = "1000/1199"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())


if __name__ == '__main__':
    unittest.main()
