# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 13:32:06 2020

@author: Ivan
"""
import pandas as pd
import platform
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False
colrogroup = ['#427f8f','#4a8fa1','#559db0','#66a7b8','#77b1c0','#89bbc8','#9ac5d0','#bdd9e0','#cee3e8','#e0edf0']


# 判斷是甚麼作業系統
theOS = list(platform.uname())[0]
if theOS == 'Windows':
    theOS = '\\'
    ecode = 'utf-8-sig'
else:
    theOS = '/'
    secode = 'utf-8'
    
myfont = FontProperties(fname='tools'+ theOS + 'msj.ttf')

#讀取檔案
comment_Data = pd.read_csv('data' + theOS + '運動內衣_留言資料.csv',encoding = ecode)
product_Data = pd.read_csv('data' + theOS + '運動內衣_商品資料.csv',encoding = ecode)

#--- 商品價格與銷售量分析圖
plt.scatter(product_Data['價格'],product_Data['歷史銷售量'], 
            color=colrogroup[0],
            alpha=0.5)
plt.title("商品價格與銷售量分析圖",fontsize=30)#標題
plt.ylabel("銷售量",fontsize=20)#y的標題
plt.xlabel("價格",fontsize=20) #x的標題
plt.grid(True) # grid 開啟
plt.tight_layout()


#--- 商品評分評價比較圖
product_Data_melt_zero = product_Data[product_Data['評分']>3]
plt.scatter(product_Data_melt_zero['評分'],product_Data_melt_zero['評價數量'], 
            color=colrogroup[0],
            alpha=0.5)
plt.title("商品評分與評價數量分析圖",fontsize=30)#標題
plt.ylabel("評價數量",fontsize=20)#y的標題
plt.xlabel("評分",fontsize=20) #x的標題
plt.grid(True) # grid 開啟
plt.tight_layout()


#--- 消費者購買力剖析
comment_Data.columns
comment_Data['使用者ID'].value_counts()

consumerPower = comment_Data[['使用者ID','價格']].groupby("使用者ID").sum()
consumerPower = pd.concat([consumerPower,
                           comment_Data[['使用者ID','價格']].groupby("使用者ID").mean()], axis=1)
consumerPower.columns = ['總購買金額','平均購買金額']

plt.scatter(consumerPower['平均購買金額'],consumerPower['總購買金額'], 
            color=colrogroup[0], 
            alpha=0.5)
plt.title("消費者購買力分析圖",fontsize=30)#標題
plt.xlabel("平均購買金額",fontsize=20)#y的標題
plt.ylabel("總購買金額",fontsize=20) #x的標題
plt.grid(True) # grid 開啟
plt.tight_layout()


#--- 消費者購買力剖析（價格區間）
consumerPower_Interval = pd.DataFrame(consumerPower['平均購買金額'].value_counts())
consumerPower_Interval.sort_index(inplace=True)

plt.plot(consumerPower_Interval.index,consumerPower_Interval['平均購買金額'],color=colrogroup[0])
plt.title("消費者購買力剖析（價格區間）",fontsize=30)#標題
plt.xlabel("平均購買金額",fontsize=20)#y的標題
plt.ylabel("人數",fontsize=20) #x的標題
plt.grid(True) # grid 開啟
plt.tight_layout()


#--- Tag使用排行
tag = []
count = []
like = []
sale = []
for i,l,h in zip(product_Data['Tag'].tolist(), product_Data['喜愛數量'].tolist() ,product_Data['歷史銷售量'].tolist()):
    for j in eval(i):
        if not(j in tag):
            tag.append(j)
            count.append(1)
            like.append(l)
            sale.append(h)
        else:
            count[tag.index(j)] = count[tag.index(j)]+1
            like[tag.index(j)] = like[tag.index(j)]+l
            sale[tag.index(j)] = sale[tag.index(j)]+h
            
dic = {
       'Tag':tag,
       '總使用數量':count,
       '總喜歡數':like,
       '總銷量':sale
       }
TagData = pd.DataFrame(dic)
TagData = TagData.sort_values(by=['總使用數量'], ascending = False)

plt.bar(TagData['Tag'][:10], TagData['總使用數量'][:10])
plt.title("Tag使用排行",fontsize=30)#標題
plt.xlabel("Tag名稱",fontsize=20)#y的標題
plt.ylabel("總使用數量",fontsize=20) #x的標題
plt.xticks(fontsize=10,rotation=90)
plt.tight_layout()


#--- Tag的喜歡與總銷量比較圖
plt.scatter(TagData['總喜歡數'],TagData['總銷量'],color=colrogroup[0])
plt.title("Tag的喜歡與總銷量比較圖",fontsize=30)#標題
for i,j,t in zip(TagData['總喜歡數'],TagData['總銷量'],TagData['Tag']):
    if i > 6000 and j > 125000:
        plt.text(i, j, t, fontsize=10 ) # 最後一天的點上方的標籤文字
plt.xlabel("總喜歡數",fontsize=20)#y的標題
plt.ylabel("總銷量",fontsize=20) #x的標題
plt.grid(True) # grid 開啟
plt.tight_layout()


