import  requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import sqlite3
import os
url=input('輸入要爬的PTT網址(未輸入自動搜尋Gossiping版): ')
if url in locals():
    print("找到網址!開始搜尋...")
else:
    print("沒偵測到輸入...自動搜尋Gossiping")
    url="https://www.ptt.cc/bbs/Gossiping/index.html"
cookie={"cookie": "over18=1;"}
ids=[]
rec=[]
titles=[]
dates=[]
c = sqlite3.connect('PTT.db')
try:
    page=int(input('輸入要爬幾頁: '))
except:
    print("未輸入數字或輸入不正確,預設輸入一頁")
    page=1
print("創立PTT_SQL....")
try:
    c.execute('''CREATE TABLE PTT
                (RECOMMEND INT,
                NAME TEXT,
                TITLE TEXT,
                DATE TEXT)''')
    print("建立完成")
except:
    print("SQL以建立過")
for i in range(page):
    rq=requests.get(url,headers=cookie)
    soup=bs(rq.text,'html.parser')
    sel=soup.select("div.r-ent")
    u=soup.select('div.btn-group.btn-group-paging a')
    url = "https://www.ptt.cc"+ u[1]["href"]
    print('當前網頁',url)
    for s in sel:
        ids.append(s.find(class_='author').string)
        try:
            rec.append(s.find('span').string)
        except:
            rec.append('0')
        try:
            titles.append(s.find('a').string)
        except:
            titles.append("本文已被刪除")
        dates.append(s.find('div',class_='date').string)
    for newid,newrec,newtitle,newdate in zip(ids,rec,titles,dates):
        print(newid,newrec,newtitle,newdate)
        c.execute("insert into PTT values (?,?,?,?)",(newrec,newid,newtitle,newdate))
ptt_dict={'ID':ids,
                    '推文數':rec,
                    '標題':titles,
                    '日期':dates}
#print(ptt_dict)
ptt_df=pd.DataFrame(ptt_dict)
ptt_df.to_csv("PTT.csv",encoding="utf_8_sig")
c.commit()

continueDB=input('是否要查詢資料庫(Y or N): ')
if continueDB=="Y"or"y":
    rows=c.execute("select * from PTT;")
    for row in rows:
        for field in row:
            print("{}\t".format(field), end="")
        print()
    print("爬完了")
else:
    print("爬完了")

c.close()
