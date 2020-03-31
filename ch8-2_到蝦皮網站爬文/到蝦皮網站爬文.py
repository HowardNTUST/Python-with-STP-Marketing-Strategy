# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 10:32:04 2020

@author: Ivan
"""

import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time
from tqdm import tqdm
import time
import re
import random

keyword = '運動內衣'
page = 1

#封包標頭檔
my_headers = {'authority' : 'shopee.tw',
     'method': 'GET',
     'path': '/api/v1/item_detail/?item_id=1147052312&shop_id=17400098',
     'scheme': 'https',
     'accept': '*/*',
     'accept-encoding': 'gzip, deflate, br',
     'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
     'cookie': '_ga=GA1.2.1087113924.1519696808; SPC_IA=-1; SPC_F=SDsFai6wYMRFvHCNzyBRCvFIp92UnuU3; REC_T_ID=f2be85da-1b61-11e8-a60b-d09466041854; __BWfp=c1519696822183x3c2b15d09; __utmz=88845529.1521362936.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _atrk_siteuid=HEgUlHUKcEXQZWpB; SPC_EC=-; SPC_U=-; SPC_T_ID="vBBUETICFqj4EWefxIdZzfzutfKhrgytH2wyevGxiObL3hFEfy0dpQSOM/yFzaGYQLUANrPe7QZ4hqLZotPs72MhLd8aK0qhIwD5fqDrlRs="; SPC_T_IV="IpxA2sGrOUQhMH4IaolDSA=="; cto_lwid=2fc9d64c-3cfd-4cf9-9de7-a1516b03ed79; csrftoken=EDL9jQV76T97qmB7PaTPorKtfMlU7eUO; bannerShown=true; _gac_UA-61915057-6=1.1529645767.EAIaIQobChMIwvrkw8bm2wIVkBiPCh2bZAZgEAAYASAAEgIglPD_BwE; _gid=GA1.2.1275115921.1529896103; SPC_SI=2flgu0yh38oo0v2xyzns9a2sk6rz9ou8; __utma=88845529.1087113924.1519696808.1528465088.1529902919.7; __utmc=88845529; appier_utmz=%7B%22csr%22%3A%22(direct)%22%2C%22timestamp%22%3A1529902919%7D; _atrk_sync_cookie=true; _gat=1',
     'if-none-match': "55b03-9ff4fb127aff56426f5ec9022baec594",
     'referer': 'https://shopee.tw/6-9-%F0%9F%87%B0%F0%9F%87%B7%E9%9F%93%E5%9C%8B%E9%80%A3%E7%B7%9A-omg!%E6%96%B0%E8%89%B2%E7%99%BB%E5%A0%B4%F0%9F%94%A5%E4%BA%A4%E5%8F%89%E7%BE%8E%E8%83%8CBra%E5%BD%88%E5%8A%9B%E8%83%8C%E5%BF%83-i.17400098.1147052312',
     'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
     'x-api-source': 'pc',
     'x-requested-with': 'XMLHttpRequest'
      }   

#專門用來請求蝦皮
def request_shopee(keyword, page):
    url = 'https://shopee.tw/api/v2/search_items/?by=relevancy&keyword=' + keyword + '&limit=100&newest=' + str(page*100) + '&order=desc&page_type=search&version=2'
    #開始請求
    list_req = requests.get(url,headers = my_headers)
    soup = BeautifulSoup(list_req.content, "html.parser")
    #將扒下來的文字轉成Json
    getjson=json.loads(soup.text)
    
    return getjson['items']

# 進入每個商品，抓取賣家更細節的資料（商品文案、SKU）
def goods_detail(item_id, shop_id):
    url = 'https://shopee.tw/api/v2/item/get?itemid=' + str(item_id) + '&shopid=' + str(shop_id)
    r = requests.get(url,headers = my_headers)
    st= r.text.replace("\\n","^n")
    st=st.replace("\\t","^t")
    st=st.replace("\\r","^r")
    
    gj=json.loads(st)
    return gj

# 進入每個商品，抓取買家留言
def goods_comments(item_id, shop_id):
    url = 'https://shopee.tw/api/v1/comment_list/?item_id='+ str(item_id) + '&shop_id=' + str(shop_id) + '&offset=0&limit=200&flag=1&filter=0'
    r = requests.get(url,headers = my_headers)
    st= r.text.replace("\\n","^n")
    st=st.replace("\\t","^t")
    st=st.replace("\\r","^r")
    
    gj=json.loads(st)
    return gj['comments']





container = pd.DataFrame()
container_comm = pd.DataFrame()
for i in tqdm(range(page)):
    commentlist = pd.DataFrame()
    articles = []
    SKU = []
    tags = []
    items=pd.DataFrame(request_shopee(keyword='運動內衣', page=i)) #先取得100個產品
    
    # 查看request_shopee爬下來的資料
    items2 = items[['itemid','shopid','name', 'price']]
    
    
    #一個一個產品進去抓
    for itemid, shopid, name, price in zip(items['itemid'].tolist(), items['shopid'].tolist(), items['name'].tolist(), items['price'].tolist()):
        print('正在爬取商品： ' + name[:30] + '...')
        product=goods_detail(item_id = itemid, shop_id = shopid)['item']
        
        
        #取得資料
        articles.append(product['description'])
        SKU.append(product['models'])
        tags.append(product['hashtag_list'])
        

        #評論詳細資料
        iteComment = goods_comments(item_id = itemid, shop_id = shopid)
        userid = [] #使用者ID
        anonymous = [] #是否匿名
        commentTime = [] #留言時間
        is_hidden = [] #是否隱藏
        orderid = [] #訂單編號
        comment_rating_star = [] #給星
        comment = [] #留言內容
        product_SKU = [] #商品規格
        
        for comm in iteComment:
            userid.append(comm['userid'])
            anonymous.append(comm['anonymous'])
            commentTime.append(comm['ctime'])
            is_hidden.append(comm['is_hidden'])
            orderid.append(comm['orderid'])
            comment_rating_star.append(comm['rating_star'])
            comment.append(comm['comment'])
            
            p=[]
            for pro in comm['product_items']:
                try:
                    p.append(pro['model_name'])
                except:
                    p.append(None)
            product_SKU.append(p)
        
        comment_dic = pd.DataFrame({
            '使用者ID':userid,
            '是否匿名':anonymous,
            '留言時間':commentTime,
            '是否隱藏':is_hidden,
            '訂單編號':orderid,
            '給星':comment_rating_star,
            '留言內容':comment,
            '商品規格':product_SKU
            })
    
        container_comm = pd.concat([container_comm,comment_dic], axis=0)
        print(len(container_comm))

    #做成欄位
    items['articles'] = articles
    items['SKU'] = SKU
    items['hashtag_list'] = tags
    
    
    container = pd.concat([container,items], axis=0)
    time.sleep(random.randint(10,20))
    
container.to_csv(keyword +'_商品資料.csv', encoding = 'utf-8-sig') #Mac使用utf-8   
container_comm.to_csv(keyword +'_留言資料.csv', encoding = 'utf-8-sig') #Mac使用utf-8 



