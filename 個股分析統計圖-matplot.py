import requests
import json,csv
import pandas as pd
import os
import matplotlib.pyplot as plt
import time

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
#抓取日期欄位的總列數i
for i in range(len(pdstock['日期'])):
    #將日期格式轉換為西元年格式
    pdstock['日期'][i] = convertDate(pdstock['日期'][i])
    
#將日期欄位的資料型態改為日期格式
pdstock['日期'] = pd.to_datetime(pdstock['日期'])

#繪製圖形
try:
    figure = pdstock.plot(x='日期', y = ['收盤價','最低價','最高價'],title= title + year + '年個股統計圖' )
except Exception as e:
    print(e)
plt.show(figure)


