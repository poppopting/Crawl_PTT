
# coding: utf-8

# In[ ]:


import requests
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
from collections import Counter
import re
import urllib
import os


# In[ ]:


#先找到網址
def geturl(start,end):
    dic = {}  #建字典 蒐集 標題:網址
    reg = re.compile("公告|<.+>")  #把公告弄掉
    while start>end:
        url = "https://www.ptt.cc/bbs/sex/index{}.html".format(start) #把網址編號format進去
        doc = pq(url,cookies={'over18': '1'})   #傳入網址及cookies  doc為網頁原始碼
        doc.make_links_absolute()  #化為絕對連結
        print(type(doc))
        #print(doc)
        for i in doc(".r-ent .title").items():  #找出標題 但依然是原始碼不過是標題那段的原始碼
            title = i.text() #只截取出文字
            link = i("a").attr("href") #從class a 中獲取 herf的內容
            if not reg.findall(title) and link: #如果title不是公告(compile)或<>
                dic[title] = link #在字典裡加 title link
        start = start-1
                
    return(dic)


# In[ ]:


def get_img_url(url,path,push_filter=None):
    # make dir:
    try:
        os.mkdir(path) #創建目錄
    except FileExistsError:
        pass

    #pyquery
    doc = pq(url,cookies={'over18':'1'})
    
    
    #push_filter:
    if push_filter:
        if len(re.findall('推',doc("span.push-tag").text()))<push_filter:   #span開頭 push-tag結尾
            return None  #如果推數回傳小於指定值 就回傳none
    
    
    #fild img url:
    re_img = re.compile("htt.+imgur.+[jpg|jpeg]{0,1}")  #找圖的縮網址
    re_jpg = re.compile(".jp.*g$")  #找jp_g結尾
    content = doc("#main-content").text().split("發信站: 批踢踢實業坊(ptt.cc)")[0]  #把正文的文字抓下來 (正文也就是在批踢踢實業坊以前)
    imgs = re_img.findall(content)  #從正文中找縮圖網址
    if not imgs:  #如果沒東西 返回0
        return 0
    
    # create folder
    title = doc("title").text().split(" - ")[0]   #找出標題 因為" - "後面是看板分類
    #cut all symbols:
    title = "".join(re.findall("[\u4e00-\u9fa5_a-zA-Z0-9]",title)) #把中括號刪掉
    # make dir for imgs:
    try:
        os.mkdir(os.path.join(path, title)) #在path下用title名建資料夾
    except FileExistsError:   #如果資料夾名重複的話
        for i in range(100):
            try:
                os.mkdir(os.path.join(path, title+str(i+1))) #就把檔名改成title+數字(從1開始)
            except:
                pass #重回try繼續試
            else:
                break 
    ##  
    try:
        for num,img in enumerate(imgs): #enumerate 列出數據及數據index(預設為0)
            if not re_jpg.findall(img): #如果網址後面不是jp_g結尾
                img = img+".jpg"
            if not re.findall("i\.imgur",img):  #如果img找不到i\.imgur
                img = "i.imgur".join(img.split("imgur"))
            name = "img"+str(num+1)+".jpg"  #取檔名
            urllib.request.urlretrieve(img, os.path.join(os.path.join(path, title), name)) #把圖載下來 丟進title的資料夾取名為nmae
    except:
        print("url : ",url)
        print("title",title)


# In[ ]:


res = geturl(3800,3700)
for url in res.values():
    get_img_url(url,"sex_capture3",50) 

