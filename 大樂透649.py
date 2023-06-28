#https://www.taiwanlottery.com.tw/Lotto/Lotto649/history.aspx
import datetime
import random
import time
import mysql.connector as mysql
from bs4 import  BeautifulSoup
from selenium.webdriver.support import  expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
def getData(year,month):
    global brower
    brower.get('https://www.taiwanlottery.com.tw/Lotto/Lotto649/history.aspx')
    radio = brower.find_element(By.ID, 'Lotto649Control_history_radYM')
    radio.click()
    select_year = Select(brower.find_element(By.ID, 'Lotto649Control_history_dropYear'))
    select_year.select_by_value(f'{year}')
    select_month = Select(brower.find_element(By.ID, 'Lotto649Control_history_dropMonth'))
    select_month.select_by_value(f'{month}')
    btn=brower.find_element(By.ID, 'Lotto649Control_history_btnSubmit')
    btn.click()
    datas=[]
    try:
        #WebDriverWait  等待避免抓到空白
        WebDriverWait(brower,20,0.5).until(EC.presence_of_element_located((By.TAG_NAME,'td')))
        soup=BeautifulSoup(brower.page_source,'html.parser')
        tables=soup.find_all('table',class_="td_hm")
        for table in tables:
            tds=table.find_all("td",class_="td_w")
            u=tds[1].text.replace('\n','').split('/')
            e=str(tds[2].text).split('/')
            sale=str(tds[3].text).replace(',','')
            total=str(tds[4].text).replace(',','')
            t=[tds[0].text,f'{1911+int(u[0])}-{u[1]}-{u[2]}',f'{1911+int(e[0])}-{e[1]}-{e[2]}',int(sale),int(total)]
            for i in range(12,19):
                t.append(int(tds[i].text))
            m=int(str(tds[35].text).replace(',',''))+int(str(tds[36].text).replace(',',''))+int(str(tds[37].text).replace(',',''))+int(str(tds[38].text).replace(',',''))
            t.append(m)
            datas.append(t)
            # for i,td in enumerate(tds):
            #     print(i,td.text)
    except:
        print('time out')

    return datas

ops=Options()
ops.add_argument('--headless')
ops.add_argument('--disable-gpu')
service=Service(ChromeDriverManager().install())
ops.add_experimental_option('detach',True)#brower與程式分離,才不會程式節塑就自動關閉brower
brower=webdriver.Chrome(service=service,options=ops)


conn=mysql.connect(host='localhost',user='yy010',password='dkgbfdoyyy010',database='cloud')
cursor=conn.cursor()
cmd="insert into 大樂透649彙整 (期數,開獎日期,截止日期,銷售金額,獎金總額,n1,n2,n3,n4,n5,n6,spn,累計至下次) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
for i in range(107,datetime.datetime.now().year+1-1911):
    if i == 112:
        s=datetime.datetime.now().month+1
    else:
        s=13

    for j in range(1,s):
        datas=getData(i,j)
        datas.reverse()
        cursor.executemany(cmd,datas)
        conn.commit()
        time.sleep(random.randint(3,8)+random.random())
        print(f'{i}年{j}月已完成')
conn.close()

