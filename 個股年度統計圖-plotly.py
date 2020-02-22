import requests
import json,csv
import pandas as pd
import os
import matplotlib.pyplot as plt
import time
import plotly
import plotly.io as pio
import plotly.graph_objects as go
from plotly.graph_objs import Scatter,Layout


#顯示中文字
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False

#將民國年轉為西元年
def convertDate(date):
    str1 = str(date)
    yearstr = str1[:3]
    realyear = str(int(yearstr)+ 1911)
    realdate = realyear + str1[4:6] + str1[7:9]
    return realdate

#將個位數數字轉為兩位數 ex. 1->01
def twodigit(n):
    if (n<10) :
        retstr = "0" + str(n)
    else:
        retstr = str(n)
    return retstr

#拆開網址
stockNo = input('股票代碼')
year = input('西元年度')
urlfront = "https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date="
urlend = "01&stockNo="

#為抓取股票名稱(title)所用的url及資料
url_for_title = urlfront + year + '01' + urlend + stockNo
res_for_title = requests.get(url_for_title)
data_for_title = json.loads(res_for_title.text)
title = data_for_title['title'][12:-6].strip()
filepath = title + (stockNo) + '-' + year +"年個股統計圖.csv"

#開啟檔案，如果檔案不存在就建立檔案
if not os.path.isfile(filepath):
    #跑迴圈取得1~12月的資料
    for i in range(1,13):
        #合併網址
        url = urlfront + year + twodigit(i) + urlend + stockNo
        res = requests.get(url)
        jdata = json.loads(res.text)              
        
        #開啟csv檔案 "a"在結尾處附加覆寫
        outputfile = open(filepath, 'a', newline='', encoding='utf-8-sig')
        outputwriter = csv.writer(outputfile)

        #i =1 時填入資料
        if i ==1:
            outputwriter.writerow(jdata['fields'])
        for dataline in (jdata['data']):
            outputwriter.writerow(dataline)
        time.sleep(0.5)
    outputfile.close()

#以pandas開啟csv檔案
pdstock = pd.read_csv(filepath, encoding='utf-8-sig')

data = [
    Scatter(x=pdstock['日期'] , y=pdstock['收盤價'], name='收盤價'),
    Scatter(x=pdstock['日期'] , y=pdstock['最低價'], name='最低價'),
    Scatter(x=pdstock['日期'] , y=pdstock['最高價'], name='最高價')
]

#書上寫的此段程式碼無法執行，尚未找到原因
# plotly.offline.iplot({
#     'data':data,
#     'Layout': Layout(title='股票代碼:' + stockNo + '-' + year + '年個股統計圖')
# })

#於plotly官方網站上找到的方法
fig = go.Figure(
    data=data,
    layout_title_text=title + year + '年個股統計圖'
)
#未寫此行程式碼前，瀏覽器會顯示"127.0.0.1"無法連線
fig.write_html(title + year + '年統計圖.html', auto_open=True)
