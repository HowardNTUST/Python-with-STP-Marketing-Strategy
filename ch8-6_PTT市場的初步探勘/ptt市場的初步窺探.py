# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 13:11:24 2020

@author: Ivan
"""
import pandas as pd
import numpy as np
import platform
from opencc import OpenCC
from geolite2 import geolite2
geo = geolite2.reader()
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False
colrogroup = ['#427f8f','#4a8fa1','#559db0','#66a7b8','#77b1c0','#89bbc8','#9ac5d0','#bdd9e0','#cee3e8','#e0edf0']
colorcompetitor = ['#d9f776','#76f794','#9476f7','#f776d9','#e70e4b','#76d9f7','#f79476','#fbccbe','#befbcc','#fbbeed']
 

# 判斷是甚麼作業系統
theOS = list(platform.uname())[0]
if theOS == 'Windows':
    theOS = '\\'
    ecode = 'utf-8-sig'
else:
    theOS = '/'
    ecode = 'utf-8'
myfont = FontProperties(fname='tools'+ theOS + 'msj.ttf')

alldata = pd.read_csv('data'+theOS+'pttData.csv',encoding = ecode)

#--- 挑出提到「運動內衣」相關的標題、文章
underwearData = alldata[alldata['標題'].str.contains("運動內衣") |
                        alldata['標題'].str.contains("運動bra") |
                        alldata['內文'].str.contains("運動內衣") |
                        alldata['內文'].str.contains("運動bra") 
                        ]

#--- 運動內衣文章來源
boardName = underwearData['版名'].value_counts()
plt.pie(boardName.values, #各比例
        explode= [x//len(boardName)*0.3 for x in range(len(boardName),0,-1)], #散開程度
        labels=boardName.index, #標籤
        autopct='%1.1f%%', #數值格式
        shadow=True, #陰影
        colors = colrogroup, #顏色
        textprops={'fontsize': 14}, #文字大小
        startangle=90 ) #轉向角度）
plt.title("運動內衣文章來源（共"+str(len(underwearData))+"篇）",fontsize=30,fontproperties=myfont)#標題
plt.axis('equal')# 讓圓餅圖畫出來是圓形
plt.tight_layout()



#--- 判斷IP位置
def IP_info(ip):
    try:
        x = geo.get(ip)
        getCH = x['country']['names']['zh-CN']
        
        return OpenCC('s2t').convert(getCH) if x is not None else np.nan
    except:
        if ('(' in ip)  and (')' in ip):
            ip = ip.replace('(','')
            ip = ip.replace(')','')
            return ip
        else:
            return np.nan
        
underwearData['IP位置'] = underwearData['IP位置'].apply(IP_info)

showlocat = underwearData['IP位置'].value_counts()
plt.bar(showlocat.index,showlocat.values,
            color=colrogroup[3],
            alpha=0.5)
plt.title("提到運動內衣的網友位置",fontsize=30,fontproperties=myfont)#標題
plt.ylabel("文章數量",fontsize=20,fontproperties=myfont)#y的標題
plt.xlabel("地區",fontsize=20,fontproperties=myfont) #x的標題
plt.tight_layout()

#--- 時間處理
underwearData['日期'] = underwearData['日期'].str.replace('Jan','1')
underwearData['日期'] = underwearData['日期'].str.replace('Feb','2')
underwearData['日期'] = underwearData['日期'].str.replace('Mar','3')
underwearData['日期'] = underwearData['日期'].str.replace('Apr','4') 
underwearData['日期'] = underwearData['日期'].str.replace('May','5')
underwearData['日期'] = underwearData['日期'].str.replace('Jun','6')
underwearData['日期'] = underwearData['日期'].str.replace('Jul','7')
underwearData['日期'] = underwearData['日期'].str.replace('Aug','8')
underwearData['日期'] = underwearData['日期'].str.replace('Sep','9')
underwearData['日期'] = underwearData['日期'].str.replace('Oct','10')
underwearData['日期'] = underwearData['日期'].str.replace('Nov','11')
underwearData['日期'] = underwearData['日期'].str.replace('Dec','12')

underwearData[['星期','日期待轉換']] = underwearData['日期'].str.split(n=1, expand=True)
underwearData['日期'] = pd.to_datetime(underwearData['日期待轉換'])
underwearData = underwearData.drop(columns=['日期待轉換'])

week = underwearData['星期'].value_counts()
plt.pie(week.values, #各比例
        explode= [x//len(week)*0.3 for x in range(len(week),0,-1)], #散開程度
        labels=week.index, #標籤
        autopct='%1.1f%%', #數值格式
        shadow=True, #陰影
        colors = colrogroup, #顏色
        textprops={'fontsize': 14}, #文字大小
        startangle=90 ) #轉向角度）
plt.title("文章時間",fontsize=30,fontproperties=myfont)#標題
plt.axis('equal')# 讓圓餅圖畫出來是圓形
plt.tight_layout()

    