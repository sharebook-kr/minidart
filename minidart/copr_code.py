import requests
import io
import zipfile
import xmltodict
import pandas as pd


class CorpCode:
    def __init__(self, key):
        url = "https://opendart.fss.or.kr/api/corpCode.xml"
        params = {"crtfc_key": key }
        resp = requests.get(url, params=params)

        bin_stream = io.BytesIO(resp.content)
        zfile = zipfile.ZipFile(bin_stream)
        xml = zfile.read("CORPCODE.xml").decode("utf-8")
        data= xmltodict.parse(xml)
        data = data['result']['list']
        self.df = pd.DataFrame(data)

    def get_corp_code(self, by_name=None, by_code=None):
        if by_name is None and by_code is None:
            print("조회할 종목이름 또는 종목코드를 입력하세요.")
            return None
        else:
            if by_name is not None:
                cond = self.df['corp_name'] == by_name
            else:
                cond = self.df['stock_code'] == by_code
            corp_code = self.df[cond]['corp_code'].values[0]
            return corp_code 


if __name__ == "__main__":
    key = ""
    corp_code = CorpCode(key=key)
    print(corp_code.get_corp_code(by_name="삼성전자"))
    print(corp_code.get_corp_code(by_code="005930"))