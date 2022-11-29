"""
=============================================================================
Project   : ARIADNEplus
Package   : yearspanmatcher
Module    : util.py 
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru 
Contact   : ceri.binding@southwales.ac.uk
Summary   : Misc useful utility functions, but no longer used in this package
Imports   : N/A
Example   : 
License   : https://github.com/cbinding/yearspans/blob/main/LICENSE.md
=============================================================================
History
02/06/2020 CFB Initially created script
=============================================================================
"""
# correctly identify numbers (as isnumeric returns false for negatives and decimals)
# from https://lerner.co.il/2019/02/17/pythons-str-isdigit-vs-str-isnumeric/ comments


def isnumber(value):
    ss = str(value).strip()
    if len(ss) == 0:
        return False
    if ss[0] == "-" or ss[0] == "+":
        ss = ss[1:]
    if ss.find(".") == ss.rfind("."):
        ss = ss.replace(".", "")
    return ss.isdigit()

# try to parse integer value without error


def tryParseInt(value):
    val = None
    if value is not None:
        try:
            val = int(value)  # , True
        except ValueError:
            val = val  # value #, False
    return val
