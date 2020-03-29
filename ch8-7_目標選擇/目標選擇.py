# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 21:28:37 2020

@author: Ivan
"""

import jieba
import pandas as pd
import platform
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
jieba.set_dictionary('tools'+theOS+'dict.txt.big')

alldata = pd.read_csv('data'+theOS+'pttData.csv',encoding = ecode)

#--- 挑出提到「運動內衣」相關的標題、文章
underwearData = alldata[alldata['標題'].str.contains("運動內衣") |
                        alldata['標題'].str.contains("運動bra") |
                        alldata['內文'].str.contains("運動內衣") |
                        alldata['內文'].str.contains("運動bra") 
                        ]
# 無意義字元列表，可以自行新增
removeword = ['span','class','f3','https','imgur','h1','_   blank','href','rel','nofollow','target','cdn','cgi','b4','jpg','hl','b1','f5','f4',
              'goo.gl','f2','email','map','f1','f6','__cf___','data','bbs''html','cf','f0','b2','b3','b5','b6','原文內容','原文連結','作者'
              '標題','時間','看板','<','>','，','。','？','—','閒聊','・','/',' ','=','\"','\n','」','「','！','[',']','：','‧','╦','╔','╗','║'
              ,'╠','╬','╬',':','╰','╩','╯','╭','╮','│','╪','─','《','》' ,'.','、','（','）','　','*','※','~','○','”','“','～','@','＋','\r'
              ,'▁',')','(','-','═','?',',','!','…','&',';','『','』','#','＝','＃','\\','\\n', '"', '的', '^', '︿','＠','$','＄','%','％',
              '＆','＊','＿','+',"'",'{','}','｛','｝','|','｜','．','‵','`','；','●','§','※','○','△','▲','◎','☆','★','◇','◆','□','■','▽',
              '▼','㊣','↑','↓','←','→','↖','XD','XDD','QQ','【','】'
              ]
#--- 移除無意義字元列
for word in removeword:
    underwearData['標題'] = underwearData['標題'].str.replace(word,'')
    underwearData['內文'] = underwearData['內文'].str.replace(word,'')

#--- 取代空值
underwearData['標題'] = underwearData['標題'].fillna('')
underwearData['內文'] = underwearData['內文'].fillna('')
  

# 在屁股加上空白，防止字詞被創造
underwearData['標題'] = underwearData['標題'] + ' '
underwearData['內文'] = underwearData['內文'] + ' '
i=underwearData['所有留言'].iloc[0]

theSTR = underwearData['標題'].sum() + underwearData['內文'].sum()

for i in underwearData['所有留言']:
    for j in eval(i):
        theSTR = theSTR + j['content'] + ' '


#--- 切詞
words = list(jieba.cut(theSTR, cut_all=False))
# 計算關鍵字數量
tag = pd.DataFrame({'tag':words})
tag = pd.DataFrame(tag['tag'].value_counts())

#--- 原始資料擷取
import re
findword = '元女'
for m in re.finditer(findword, theSTR):
    print(theSTR[m.start()-50 : m.start()] +'【'+findword+'】'+theSTR[m.start()+1: m.start()+50]+'\n')
    