"""
=============================================================================
Package   : rematch2
Module    : PeriodoData.py
Classes   : PeriodoData
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Project   : 
Summary   : PeriodoData class
Imports   : json, os, urllib, jsonpath
Example   : pd = PeriodoData();
            authorities = pd.get_authority_list();
            periods = pd.get_period_list("p0kh9ds"); # HE Periods list
License   : https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History
17/06/2022 CFB Initially created script
27/10/2023 CFB type hints added for function signatures
28/02/2024 CFB locate periodo cache file with vocabulary patterns
26/04/2028 CFB Always use cache file if present
=============================================================================
"""
import json
import os
from jsonpath_ng import jsonpath
from jsonpath_ng.ext import parse

from os.path import exists
from urllib.request import urlopen
from pathlib import Path
import requests


class PeriodoData:
    """gets and manipulates Perio.do data"""

    # default data sources
    #PERIODO_URI = "https://n2t.net/ark:/99152/p0dataset.json"
    PERIODO_URI = "https://data.perio.do/dataset.json"
    CACHE_FILE_PATH = Path(__file__).parent
    CACHE_FILE_NAME = os.path.join(CACHE_FILE_PATH, "periodo-cache.json")
      
    def __init__(self):
        self._jsondata = None
        self.load()

    def load(self) -> None:
        """load data from cache or from url"""

        # if cache not present get Perio.do data from URI and store to cache
        if not exists(self.CACHE_FILE_NAME):
            data = PeriodoData._json_from_url(self.PERIODO_URI)
            PeriodoData._json_to_file(data, self.CACHE_FILE_NAME)
            
        # now get Perio.do data from the cache file
        self.jsondata = PeriodoData._json_from_file(self.CACHE_FILE_NAME)

    @property
    def jsondata(self):
        """Perio.do JSON data"""
        return self._jsondata

    @jsondata.setter
    def jsondata(self, new_value):
        self._jsondata = new_value

    @staticmethod
    def _json_from_url(url: str):
        """download JSON data from URL"""
       
        headers = {
            'Content-Type':'application/json',
            'Accept':'application/json',
        }
        # note 'pip install brotli' to make this work, as the
        # response from the Periodo dataset is brotli compressed
        response = requests.get(url, timeout=30, headers=headers)
        output = response.json()
        return output
        

    @staticmethod
    def _json_from_file(file_name: str):
        """load JSON data from file"""
        data = None
        with open(file_name, "r") as f:  # what if file doesn't exist?
            data = json.load(f)
        return data

    @staticmethod
    def _json_to_file(data, file_name: str):
        """write JSON data to file"""
        with open(file_name, "w") as f:
            json.dump(data, f, indent=3)
    
    # this is really versatile once we have the JSON data loaded...
    # pip3 install jmespath
    # see https://jmespath.org/tutorial.html

    def find(self, pattern:str=""):
        """find data by pattern, return JSON"""
        # result = jmespath.search(pattern, self.jsondata)
        jsonpath_expression = parse(pattern)
        result = jsonpath_expression.find(self.jsondata)
        # return json.dumps(result) # to return JSON string, not python object
        return result

    def count(self, pattern: str="") -> int:
        """get number of items matching the search pattern"""
        return length(self.find(pattern))

    # specialised properties based on .find
    # returns list of authority as [{id, label}]
    def get_authority_list(self, sorted: bool=True):
        # get list of authorities using jmespath:
        # lst = self.find("authorities.* | [?source.title != null].{id: id, label: @.source.title}")
        authorities = self.find("$.authorities.*.source[?(@.title != null)]")
        # print(authorities)
        lst = list(map(lambda item: {
            "id": item.value.get("id", ""),
            "label": item.value.get("title", "")
        }, authorities))
        # print(lst)
        # sort list if required
        if (sorted):
            lst.sort(key=lambda item: item["label"].lower())

        return lst

    # returns list of period labels as [{id: "123", label: "Iron Age", language: "en"}]

    def get_period_list(self, authorityID: str="*"):
        # labels = self.find(f"authorities.{ authorityID }.periods.*.{{id: id, label: label, language: languageTag, local: localizedLabels.* | []}}")
        periods = self.find(f"$.authorities.{ authorityID }.periods.*")

        lst = []
        BASE_URI = "http://n2t.net/ark:/99152/"
        for period in periods:
            id = period.value.get("id", "")

            uri = f"{BASE_URI}{ id }"
            label = period.value.get("label", "")
            language = period.value.get("languageTag", "")
            localized = period.value.get("localizedLabels", {}).items()
            min_year = period.value.get("start", {}).get("in", {}).get("year")
            max_year = period.value.get("stop", {}).get("in", {}).get("year")

            # main terms
            lst.append({
                "id": id,
                "uri": f"{BASE_URI}{id}",
                "label": label,
                "minYear": min_year,
                "maxYear": max_year,
                "language": language
            })

            # alt terms
            for localizedLanguage, localizedLabels in localized:
                for localizedLabel in localizedLabels:
                    if (localizedLabel != label):
                        lst.append({
                            "id": id,
                            "uri": f"{BASE_URI}{id}",
                            "label": localizedLabel,
                            "minYear": min_year,
                            "maxYear": max_year,
                            "language": localizedLanguage
                        })

        # localizedLabels = self.find(f"authorities.{ authorityID }.periods.*.localizedLabels.*.{{id: id, label: label, language: languageTag}}")
        # array of all localized labels in authority:
        # JMES: authorities.p0f65r2 | periods.* | [*].localizedLabels.* | [] | []
        # authorities.p0f65r2 | periods.*.{ id: id, label: label, local: localizedLabels.* | [] }
        # return(preferredLabels + localizedLabels)
        return lst
        # return self.find(f"authorities.{ authorityID }.periods.*.{{id: id, label: label, language: languageTag}}")


# This class may be tested as a standalone script using the parameters below
#  e.g. python PeriodoData.py
if __name__ == "__main__":
    pd = PeriodoData()
    # pd.load()
    # print(pd.authorities) # all authorities
    # print(pd.data) # this specific authority
    # print(pd.authority("p0qwjcd")) # this specific authority
    # print(pd.periods("p0qwjcd")) ## all periods for this authority
    # print(pd.find(f"authorities.p0qwjcd")) # free searching data
    # print(pd.period("p0qwjcd", "p0qwjcdnzt9")) # this period in this authority
    # authorityID = "p0qwjcd"
    # print(pd.find(f"authorities.{ authorityID }.periods")) # free searching data
    # print(pd.find("authorities.p0qwjcd.periods.*.{id: id, lbl: label}")) # free searching data
    # print(pd.find("authorities.* | source[].title"))
    # print(pd.find("authorities.*.id
    # print(pd.find("authorities.*.{key: id, lbl: @.source.title}"))
    # print(pd.find("authorities.* | [?source.title != null].{key: id, lbl: @.source.title}"))
    lst1 = pd.get_authority_list()
    # lst2 = pd.get_period_list("p0kh9ds") # "p0kh9ds" = HeritageData
    # PACTOLS chronology periods used in DOLIA data
    lst2 = pd.get_period_list("p02chr4")
    # lst = pd.get_period_list("p0h9ttq")
    print(lst1[0:2])
    #print(lst2)
    # PeriodoData._periods_to_pattern_file(lst2, "en-periodo-data.json")
    # print(pd.find("authorities.*.[@.source.title, id]"))

    # authority="p0qwjcd"
    # print(pd.find("authorities.{auth}.periods.*.{{id: id, label: label, language: languageTag}}".format(auth="p0kh9ds")))
