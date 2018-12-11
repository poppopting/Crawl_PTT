
# coding: utf-8

# In[5]:


import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
import urllib
import os
from os.path import join
import certifi
import urllib3


# In[13]:


#先找到網址
def geturl(start,end):
    dic = {}  #建字典 蒐集 標題:網址
    reg = re.compile("公告|<.+>")  #把公告弄掉
    while start>end:
        url = "https://www.ptt.cc/bbs/sex/index{}.html".format(start)#把網址編號format進去
        web=requests.get(url,cookies={'over18': '1'})
        doc = BeautifulSoup(web.text, 'html.parser')   #傳入網址及cookies  doc為網頁原始碼
        #防呆措施(異常處理)
        if doc.select('title')[0].text=='500 - Internal Server Error' or doc.text=='404 page not found\n':
            print(url,"is wrong page")
              
        #print(doc)
        for i in doc.select(".r-ent .title"):
            if len(i.find_all('a'))>0:  #找出有網址的 避開已刪除貼文
                info=i.find_all('a')
                title=info[0].text
                link0=info[0].get('href')
                link='https://www.ptt.cc'+link0
                if not reg.findall(title) and link: #如果title不是公告(compile)或<>
                    dic[title] = link #在字典裡加 title link
        start = start-1
                
    return(dic)


# In[1]:


def get_img_url(url,path,push_filter=None):
    # make dir:
    try:
        os.mkdir(path) #創建目錄
    except FileExistsError:
        pass

    #pyquery
    web=requests.get(url,cookies={'over18': '1'})
    doc = BeautifulSoup(web.text, 'html.parser')
    
 
    #push_filter:
    if push_filter:
        push_number=0
        for i in  doc.select("span.push-tag"):
            text=i.text
            if text=="推 ":              #計算推數
                push_number+=1
        if push_number<push_filter:   #span開頭 push-tag結尾
            return None  #如果推數回傳小於指定值 就回傳none
    
    
    #fild img url:
    re_img = re.compile("htt.+imgur.+[jpg|jpeg]{0,1}")  #找圖的縮網址
    re_jpg = re.compile(".jp.*g$")  #找jp_g結尾
    content = doc.select("#main-content")[0].text.split("發信站: 批踢踢實業坊(ptt.cc)")[0]  #把正文的文字抓下來 (正文也就是在批踢踢實業坊以前)
    imgs = re_img.findall(content)  #從正文中找縮圖網址
    if not imgs:  #如果沒東西 返回0
        return 0
    
    # create folder
    title = doc.select("title")[0].text.split(" - ")[0]   #找出標題 因為" - "後面是看板分類
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

            http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
            http.request('GET', img)   #請求驗證 不然會SLE error 或insecurewarning
            request = requests.get(img)
            local_path = 'C:/Users/Guan-Ting Chen/'+path+"/"+title+"/"+name
            #改用open下載 避免用request.urlretrivey造成unicode error
            with open(local_path, 'wb') as file:    #把圖載下來 丟進title的資料夾取名為nmae
                file.write(request.content)



    except:
        print("url : ",url)
        print("title",title)


# In[15]:


def crawler(start,end,path,push_filter=None) :
    res= geturl(start,end)
    for url in res.values():
        get_img_url(url,path,push_filter)
    


# In[18]:


crawler(3800,3798,"gog",10)


# In[19]:


#如果網址亂輸入
#超出現有數字
crawler(38000,37998,"gog",10)

