import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from io import BytesIO
import xlrd


def extract_dcm_no(receipt_no):
    url = f"http://dart.fss.or.kr/dsaf001/main.do?rcpNo={receipt_no}"
    resp = requests.get(url)
    html = resp.text 
    soup = BeautifulSoup(html, "html5lib")
    tags = soup.select("#north > div.view_search > ul > li:nth-child(1) > a")
    tag = tags[0]
    ret = tag.get("onclick")
    m = re.findall(r"[0-9]+", ret)
    dcm_no = m[1]
    return dcm_no


def download_xls(receipt_no, dcm_no):
    url = f"http://dart.fss.or.kr/pdf/download/excel.do?rcp_no={receipt_no}&dcm_no={dcm_no}&lang=ko"
    headers = {
        "Host": "dart.fss.or.kr",
        "Referer": f"http://dart.fss.or.kr/pdf/download/main.do?rcp_no={receipt_no}&dcm_no={dcm_no}",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0"
    }
    resp = requests.get(url, headers=headers) 
    content = resp.content

    #bytes = io.BytesIO(content).read()
    #wb = xlrd.open_workbook(file_contents=bytes)
    #sheet_names = wb.sheet_names()
    #print(sheet_names)
    xls_filename = f"{receipt_no}.xls"
    with open(xls_filename, "wb") as f:
        f.write(BytesIO(content).getbuffer())


if __name__ == "__main__":
    rcp_no = "20120330002110"
    dcm_no = extract_dcm_no(rcp_no)

    # download xls
    download_xls(rcp_no, dcm_no)




