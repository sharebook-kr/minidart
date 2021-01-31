# 분기, 반기, 사업보고서의 접수번호를 얻는 클래스
# 2011년 (IFRS) 적용 이후 시점의 데이터만 사용 
import requests
import pandas as pd

class Receipt:
    def __init__(self, key, corp_code="00126380", begin="20110101"):
        url = "https://opendart.fss.or.kr/api/list.json"
        params = {
            "crtfc_key": key, 
            "corp_code": corp_code,
            "bgn_de": begin, 
            "last_reprt_at": "Y",
            "pblntf_ty": "A",                   # 정기공시
            "pblntf_detail_ty": "A001",         # 사업보고서
            "page_count": 100
        }

        resp = requests.get(url, params=params)
        data = resp.json()
        data_list = data['list']
        self.data = pd.DataFrame(data_list)

    def get_year_fs_receipts(self):
        cond = self.data['rm'] == "연"
        df = self.data[cond]
        asc_df = df[::-1]     # ascending order
        asc_df['year'] = asc_df["report_nm"].str[-8:-4]    # year 
        data = asc_df[['year', 'rcept_no']]
        data.set_index('year', inplace=True)
        return data


if __name__ == "__main__":
    key = ""
    receipt = Receipt(key)
    df = receipt.get_year_fs_receipts()
    print(df)