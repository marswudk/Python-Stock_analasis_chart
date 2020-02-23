# Python-Stock_analasis_chart
##　從台灣證券交易所，抓取「個股日成交資訊」，繪製成月統計圖及年統計圖

專題目標：
* 從證券交易所-個股月成交資訊取得個股的歷史資料，並繪製成分析圖
* 分別使用matplot 及 plotly模組來繪圖

---

前言：
以鴻海(2317)2019年為例，因為網站使用JS渲染，所以無法直接取得資料。透過F12檢查發現，
在選擇年份查詢後，網站加入了兩筆資料
![](https://i.imgur.com/kBtwwZJ.png)
    分別是STOCK_DAY? & zh.json?
個別查看後得知股票資訊都在STOCK_DAY中

1. 因為網址組成是西元年，而回傳的資料中為民國年，所以要將民國年轉為西元年
```
def convertDate(date):
    str1 = str(date)
    yearstr = str1[:3]
    realyear = str(int(yearstr)+ 1911)
    realdate = realyear + str1[4:6] + str1[7:9]
    return realdate
```

2. 先抓2019年1月，將個股資料匯入檔案，建立CSV檔


3. 資料匯入沒問題後，對網址跑迴圈，加入整年的資料
```
#將個位數數字轉為兩位數 ex. 1->01
def twodigit(n):
    if (n<10) :
        retstr = "0" + str(n)
    else:
        retstr = str(n)
    return retstr
```

5. 因為要在結尾處繼續加上資料，覆寫方式使用'a'

6. 以pandas 開啟含有個股資料的csv檔，並加以繪圖，其中要顯示中文字除了要更改字體設定外，還要加入
```
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False
```

```
try:
    figure = pdstock.plot(x='日期', y = ['收盤價','最低價','最高價'],title='股票代碼:' + stockNo + "-" + year + "年度" )
except Exception as e:
    print(e)
plt.show(figure)
```
![](https://i.imgur.com/3FDP5r3.png)

7. 改以plotly模組繪圖，優點是可以動態顯示日期及股價，較容易觀察每天的股價資訊。

8. 將資料存在data變數，最後用plotly的繪圖語法畫出2019年鴻海的資料統計圖

```
#以pandas開啟csv檔案
pdstock = pd.read_csv(filepath, encoding='utf-8-sig')

data = [
    Scatter(x=pdstock['日期'] , y=pdstock['收盤價'], name='收盤價'),
    Scatter(x=pdstock['日期'] , y=pdstock['最低價'], name='最低價'),
    Scatter(x=pdstock['日期'] , y=pdstock['最高價'], name='最高價')
]

fig = go.Figure(
    data=data,
    layout_title_text=title + year + '年個股統計圖'
)
#未寫此行程式碼前，瀏覽器會顯示"127.0.0.1"無法連線
fig.write_html(title + year + '年統計圖.html', auto_open=True)

```
