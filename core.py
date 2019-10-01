import requests
import pandas as pd
from pandas.io.json import json_normalize
from urllib import parse
import os
import matplotlib.pyplot as plt


API = "your_API_key"
classifieds_list = []


class Classified:

    def __init__(self, auto_id):
        self.auto_id = auto_id

        self.value = Classified._search_ids_param(auto_id)

        self.classifieds_list = Classified._get_classified_list(self.value)

    @staticmethod
    def _get_search_url(j_dict):
        url_for_search = f"https://developers.ria.com/auto/search?api_key={API}&"
        full_search_url = url_for_search + parse.urlencode(j_dict)
        return full_search_url

    @staticmethod
    def _get_classified_details(auto_id):
        classified_details_url = f"https://developers.ria.com/auto/info?api_key={API}&auto_id={auto_id}"

        return requests.get(classified_details_url).json()

    @staticmethod
    def _get_classified_list(dict1):
        jf = requests.get(Classified._get_search_url(dict1)).json()

        id_total = jf["result"]["search_result"]["count"]
        total_pages = round((id_total // 100) + (id_total % 100 > 0)) - 1

        page = 0
        while page <= total_pages:
            p = requests.get(Classified._get_search_url(dict1) + f"&page={page}").json()

            id_shown = p["result"]["search_result"]["ids"]
            classifieds_list.extend(id_shown)
            page += 1

        return classifieds_list

    @staticmethod
    def _search_ids_param(other):
        auto_info = Classified._get_classified_details(other)
        search_dict = {}

        category_id = auto_info["autoData"]["categoryId"]
        search_dict["category_id"] = category_id

        mark_id = auto_info["markId"]
        search_dict["marka_id[0]"] = mark_id

        model_id = auto_info["modelId"]
        search_dict["model_id[0]"] = model_id

        search_dict["countpage"] = "100"

        return search_dict

    @staticmethod
    def get_csv_file():
        def gen_list():
            for i in classifieds_list:
                yield i

        df = pd.DataFrame()

        for ids in gen_list():
            gcd = Classified._get_classified_details(ids)
            dfs = json_normalize(gcd)
            df = df.append(dfs, ignore_index=True)

        return df.to_csv("data/data.csv")

    @staticmethod
    def get_excel_file(filename):
        file_path = os.path.abspath("data/data.csv")
        excel_name = filename + ".xlsx"
        if os.path.exists(file_path):
            with pd.ExcelWriter(excel_name) as writer:
                pd.read_csv(file_path).to_excel(writer, sheet_name='Sheet1', index=False)
                writer.save()
        else:
            Classified.get_csv_file()
            Classified.get_excel_file(filename)


def _get_table():
    df = pd.read_csv("data/data.csv")
    age = df["autoData.year"]
    all_years = list(set(age))
    all_years.sort()
    table = pd.DataFrame(columns=[])

    for i in all_years:
        year = df["autoData.year"] == i

        average_cost = df[year]["USD"].mean()
        average_race = df[year]["autoData.raceInt"].mean()
        cost_loosing = (average_cost / average_race) * 10
        table = table.append({"Year": i, "Cost": average_cost}, ignore_index=True)

    return table


def show_table():
    table = _get_table()

    x = table.Year
    y = table.Cost

    plt.plot(x, y)
    plt.show()


if __name__ == "__main__":
    pass
