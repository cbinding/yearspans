"""
=============================================================================
Project   : ARIADNEplus
Package   : yearspans
Module    : test-yearspanmatcher_no.py
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Summary   : Unit tests for YearSpanMatcher modules
Imports   : unittest, relib, YearSpanMatcherNO, YearSpan
Example   :
License   : https://github.com/cbinding/yearspans/blob/main/LICENSE.md
=============================================================================
History
14/02/2020 CFB Initially created script
=============================================================================
"""
import unittest
from yearspanmatcher import YearSpan, YearSpanMatcherNO


class TestYearSpanMatcherNO(unittest.TestCase):
    matcher = YearSpanMatcherNO()

    def test_matchMonthYearAD(self):
        span = self.matcher.match("Januar 1066 e.Kr.")  # January 1066 AD
        expected = "1066/1066"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchMonthYearBC(self):
        span = self.matcher.match("Januar 1066 f.Kr.")  # January 1066 BC
        expected = "-1065/-1065"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchMonthYearBP(self):
        span = self.matcher.match("Januar 1066 BP")  # January 1066 BP
        expected = "0934/0934"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchSeasonYearAD(self):
        span = self.matcher.match("Vår 1066 e.Kr.")  # Spring 1066 AD
        expected = "1066/1066"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchSeasonYearBC(self):
        span = self.matcher.match("Vår 1066 f.Kr.")  # Spring 1066 BC
        expected = "-1065/-1065"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchSeasonYearBP(self):
        span = self.matcher.match("Vår 1066 BP")  # Spring 1066 BP
        expected = "0934/0934"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchCardinalCenturyAD(self):
        # Early 11th Century AD
        span = self.matcher.match("Tidlig på 1100-tallet e.Kr.")
        expected = "1001/1040"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchCardinalCenturyBC(self):
        # Early 11th Century BC
        span = self.matcher.match("Tidlig på 1100-tallet f.Kr.")
        expected = "-1099/-1059"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchOrdinalCenturyAD(self):
        # Early Eleventh Century AD
        span = self.matcher.match("Tidlig ellevte århundre e.Kr.")
        expected = "1001/1040"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchOrdinalCenturyBC(self):
        # Early Eleventh Century BC
        span = self.matcher.match("Tidlig ellevte århundre f.Kr.")
        expected = "-1099/-1059"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchCardinalToCardinalCenturyAD(self):
        # early 11th to late 12th century AD
        span = self.matcher.match("tidlig på 1100 til sent 1200-tallet e.Kr.")
        expected = "1001/1200"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchCardinalToCardinalCenturyBC(self):
        # early 12th to late 11th century BC
        span = self.matcher.match(
            "tidlig på 12. til slutten av det 11. århundre f.Kr.")
        expected = "-1199/-1000"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchOrdinalToOrdinalCenturyAD(self):
        # early eleventh to late twelfth century AD
        span = self.matcher.match(
            "tidlig på ellevte til slutten av det tolvte århundre e.Kr.")
        expected = "1001/1200"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchOrdinalToOrdinalCenturyBC(self):
        # early twelfth to late eleventh century BC
        span = self.matcher.match(
            "tidlig på tolvte til slutten av 11. århundre f.Kr.")
        expected = "-1199/-1000"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchOrdinalMillenniumAD(self):
        # late 1st millennium AD
        span = self.matcher.match("sent 1. årtusen e.Kr.")
        expected = "0600/1000"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchOrdinalMillenniumBC(self):
        # late 1st millennium BC
        span = self.matcher.match("sent 1. årtusen f.Kr.")
        expected = "-0399/0000"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchOrdinalToOrdinalMillenniumAD(self):
        # late 1st to early 2nd millennium AD
        span = self.matcher.match("sent 1. til tidlig 2. årtusen e.Kr.")
        expected = "0600/1400"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearWithPrefixAD(self):
        span = self.matcher.match("tidlig 1950 e.Kr.")  # early 1950 AD
        expected = "1950/1950"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearWithPrefixBC(self):
        span = self.matcher.match("tidlig 1950 f.Kr.")  # early 1950 BC
        expected = "-1949/-1949"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearWithPrefixBP(self):
        span = self.matcher.match("tidlig 1950 BP")  # early 1950 BP
        expected = "0050/0050"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearWithSuffixAD(self):
        span = self.matcher.match("1950 e.Kr.")  # 1950 AD
        expected = "1950/1950"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearWithSuffixBC(self):
        span = self.matcher.match("1950 f.Kr.")  # 1950 BC
        expected = "-1949/-1949"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearWithSuffixBP(self):
        span = self.matcher.match("1950 BP")  # 1950 BP
        expected = "0050/0050"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearToYear1AD(self):
        span = self.matcher.match("1255 - 7 e.Kr.")  # 1255 - 7 AD
        expected = "1255/1257"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearToYear2AD(self):
        span = self.matcher.match("1250 - 57 e.Kr.")  # 1250 - 57 AD
        expected = "1250/1257"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearToYear4AD(self):
        span = self.matcher.match("1200 - 1500 e.Kr.")  # 1200 - 1500 AD
        expected = "1200/1500"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearToYearBC(self):
        span = self.matcher.match("1200 - 1500 f.Kr.")  # 1200 - 1500 BC
        expected = "-1499/-1199"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchYearToYearBP(self):
        span = self.matcher.match("1200 - 1500 BP")  # 1200 - 1500 BP
        expected = "0500/0800"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchLoneDecade(self):
        span = self.matcher.match("1950-tallet")  # 1950's
        expected = "1950/1959"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchDecadeToDecade(self):
        span = self.matcher.match("1950- til 1960-tallet")  # 1950's to 1960's
        expected = "1950/1969"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchNamedPeriod(self):
        span = self.matcher.match("vikingtid")  # http://n2t.net/ark:/99152/p04h98qjpf9 (Viking Age)
        expected = "0750/1050"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())

    def test_matchNamedToNamedPeriod(self):
        span = self.matcher.match(
            "vikingtid til høymiddelalder")  # Viking Age to High Middle Age
        expected = "0750/1350"
        self.assertEqual(expected, (span or YearSpan()).toISO8601())


if __name__ == '__main__':
    unittest.main()
