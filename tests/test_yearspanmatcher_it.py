"""
=============================================================================
Project   : ARIADNEplus
Package   : yearspans
Module    : test-yearspanmatcher_it.py
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Summary   : Unit tests for YearSpanMatcher modules
Imports   : unittest, relib, YearSpanMatcherIT, YearSpan
Example   :
License   : https://creativecommons.org/licenses/by/4.0/ [CC BY 4.0]
=============================================================================
History
14/02/2020 CFB Initially created script
=============================================================================
"""
import unittest
from yearspanmatcher import YearSpan, YearSpanMatcherIT


class TestYearSpanMatcherIT(unittest.TestCase):
    matcher = YearSpanMatcherIT()

    def test_matchMonthYearAD(self):
        span = self.matcher.match("Gennaio 1066 d.C.")  # January 1066 AD
        expected = "1066/1066"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchMonthYearBC(self):
        span = self.matcher.match("Gennaio 1066 a.C.")  # January 1066 BC
        expected = "-1065/-1065"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchMonthYearBP(self):
        span = self.matcher.match("Gennaio 1066 BP")  # January 1066 BP
        expected = "0934/0934"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchSeasonYearAD(self):
        span = self.matcher.match("Primavera 1066 d.C.")  # Spring 1066 AD
        expected = "1066/1066"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchSeasonYearBC(self):
        span = self.matcher.match("Primavera 1066 a.C.")  # Spring 1066 BC
        expected = "-1065/-1065"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchSeasonYearBP(self):
        span = self.matcher.match("Primavera 1066 BP")  # Spring 1066 BP
        expected = "0934/0934"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchCardinalCenturyAD(self):
        # Early 11th Century AD
        span = self.matcher.match("Inizio dell'XI secolo d.C.")
        expected = "1001/1040"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchCardinalCenturyBC(self):
        # Early 11th Century BC
        span = self.matcher.match("Inizio dell'XI secolo a.C.")
        expected = "-1099/-1059"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchOrdinalCenturyAD(self):
        # Early Eleventh Century AD
        span = self.matcher.match("Inizio undicesimo secolo d.C.")
        expected = "1001/1040"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchOrdinalCenturyBC(self):
        # Early Eleventh Century BC
        span = self.matcher.match("Inizio undicesimo secolo a.C.")
        expected = "-1099/-1059"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchCardinalToCardinalCenturyAD(self):
        # early 11th to late 12th century AD
        span = self.matcher.match(
            "inizio dell'XI alla fine del XII secolo d.C.")
        expected = "1001/1200"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchCardinalToCardinalCenturyBC(self):
        # early 12th to late 11th century BC
        span = self.matcher.match(
            "inizio del XII alla fine dell'XI secolo a.C.")
        expected = "-1199/-1000"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchOrdinalToOrdinalCenturyAD(self):
        # early eleventh to late twelfth century AD
        span = self.matcher.match(
            "inizio del undicesimo alla fine del dodicesimo secolo d.C.")
        expected = "1001/1200"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchOrdinalToOrdinalCenturyAD2(self):
        # between the 3rd and 4th centuries AD
        span = self.matcher.match("tra lo III e lo IV sec. d.C.")
        expected = "0201/0400"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchOrdinalToOrdinalCenturyBC(self):
        # early twelfth to late eleventh century BC
        span = self.matcher.match(
            "inizio del dodicesimo alla fine del undicesimo secolo a.C.")
        expected = "-1199/-1000"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchOrdinalMillenniumAD(self):
        # late 1st millennium AD
        span = self.matcher.match("fine I millennio d.C.")
        expected = "0600/1000"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchOrdinalMillenniumBC(self):
        # late 1st millennium BC
        span = self.matcher.match("fine I millennio a.C.")
        expected = "-0399/0000"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchOrdinalToOrdinalMillenniumAD(self):
        # late 1st to early 2nd millennium AD
        span = self.matcher.match(
            "fine del I all'inizio del II millennio d.C.")
        expected = "0600/1400"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearWithPrefixAD(self):
        span = self.matcher.match("inizio del 1950 d.C.")  # early 1950 AD
        expected = "1950/1950"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearWithPrefixBC(self):
        span = self.matcher.match("inizio del 1950 a.C.")  # early 1950 BC
        expected = "-1949/-1949"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearWithPrefixBP(self):
        span = self.matcher.match("inizio del 1950 BP")  # early 1950 BP
        expected = "0050/0050"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearWithSuffixAD(self):
        span = self.matcher.match("1950 d.C.")  # 1950 AD
        expected = "1950/1950"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearWithSuffixBC(self):
        span = self.matcher.match("1950 a.C.")  # 1950 BC
        expected = "-1949/-1949"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearWithSuffixBP(self):
        span = self.matcher.match("1950 BP")  # 1950 BP
        expected = "0050/0050"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearToYear1AD(self):
        span = self.matcher.match("1255 - 7 d.C.")  # 1255 - 7 AD
        expected = "1255/1257"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearToYear2AD(self):
        span = self.matcher.match("1250 - 57 d.C.")  # 1250 - 57 AD
        expected = "1250/1257"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearToYear4AD(self):
        span = self.matcher.match("1200 - 1500 d.C.")  # 1200 - 1500 AD
        expected = "1200/1500"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearToYearBC(self):
        span = self.matcher.match("1500 - 1200 a.C.")  # 1500 - 1200 BC
        expected = "-1499/-1199"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchYearToYearBP(self):
        span = self.matcher.match("1200 - 1500 BP")  # 1200 - 1500 BP
        expected = "0500/0800"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchLoneDecade(self):
        span = self.matcher.match("primi anni 1850")  # Early 1850's
        expected = "1850/1859"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchDecadeToDecade(self):
        # early 1850's to late 1860's
        span = self.matcher.match("inizio del 1850 alla fine del 1860")
        expected = "1850/1869"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchNamedPeriod(self):
        span = self.matcher.match("Romana")  # Roman
        expected = "0350/0600"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())

    def test_matchNamedToNamedPeriod(self):
        span = self.matcher.match("Romana a medievale")  # Roman to Medieval
        expected = "0350/1350"
        self.assertEqual(expected, (span or YearSpan()).toISO8601span())


if __name__ == '__main__':
    unittest.main()
