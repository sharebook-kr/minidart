import requests
import pandas as pd

def get_comp_info(key, corp_code="00126380"):
    url = "https://opendart.fss.or.kr/api/company.json"
    params = {"crtfc_key": key, "corp_code": corp_code}
    resp = requests.get(url, params=params)
    data = resp.json()
    return data


def get_fs(key, year, report_code="11011", corp_code="00126380"):
    params = {
        "crtfc_key": key, 
        "corp_code": corp_code, 
        "bsns_year": year, 
        "reprt_code": report_code, 
        "fs_div": "CFS"
    }

    url = "https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json"
    resp = requests.get(url, params=params)
    data = resp.json()
    data_list = data['list']
    df = pd.DataFrame(data_list)
    return df


def get_raw_fs():
    # raw finanical statement
    pass


if __name__ == "__main__":
    key = ""

    # company basic information
    sec = get_comp_info(key)
    print(sec, type(sec))

    # Financial Statements from 2015
    sec_fs_2019 = get_fs(key, "2019")
    print(sec_fs_2019.head())