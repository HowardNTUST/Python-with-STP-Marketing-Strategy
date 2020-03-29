# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 10:41:04 2020

@author: Ivan
"""

from tqdm import tqdm
import pandas as pd
import numpy as np
import platform
from sklearn.cluster import KMeans
crub = 10 #總共要分成幾群
clf = KMeans(n_clusters=crub)
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False
colors = ['#d9f776','#76f794','#9476f7','#f776d9','#e70e4b','#76d9f7','#f79476','#fbccbe','#befbcc','#fbbeed']
  

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

#統一相同意義的Tag
product_Data['Tag'] = product_Data['Tag'].str.replace("'#無鋼圈內衣'","'#無鋼圈'")
product_Data['Tag'] = product_Data['Tag'].str.replace("'#舒適'","'#舒服'")
product_Data['Tag'] = product_Data['Tag'].str.replace("'#運動內衣',","")
product_Data['Tag'] = product_Data['Tag'].str.replace("'#運動bra',","")
product_Data['Tag'] = product_Data['Tag'].str.replace("'#運動上衣',","")

#Kmeans分群演算法繪圖
def Kmeans(df, classification):
    #開始訓練
    clf.fit(df[classification].values.tolist())
    
    #取得預測結果
    df['類群'] = clf.labels_
    
    plt.figure(figsize=(20,15))
    for i in range(crub):
       a = df[df['類群']==i] 
       plt.scatter(a['價格'], a['歷史銷售量'], s=50, c=colors[i],label = i, alpha=.5)
    plt.legend(bbox_to_anchor=(1.03, 0.8), loc=2) # 設置圖例
    plt.ylabel('歷史銷售量',fontsize=40,fontproperties=myfont)
    plt.xlabel('價格',fontsize=40,fontproperties=myfont) 
    plt.title('Kmeans顧客分群',fontsize=60,fontproperties=myfont) 
    
    return df['類群']
    
# 範例，理解用  
Kmeans(df = product_Data, classification = ['價格', '歷史銷售量'])


KmeansData = product_Data[['商品ID','價格','歷史銷售量','Tag']]

#--- 計算每個文章的tag
def evaluation(thestr):
    return eval(thestr)

allpro = KmeansData['Tag'].apply(evaluation)
allpro = allpro.sum()
allpro = pd.DataFrame(allpro)
allpro.dropna(inplace=True)

count=0
for i in tqdm(allpro[0].value_counts().index):
    KmeansData['c'+str(count)] = np.where(KmeansData['Tag'].str.contains(i),1,0)
    count = count+1
    
product_Data['類群'] = Kmeans(df = KmeansData, classification = ['c'+str(x) for x in range(count)])


#--- 消費者購買力剖析
comment_Data.columns
comment_Data['使用者ID'].value_counts()
comment_Data = pd.merge(comment_Data, product_Data[['商品ID','類群']], 
                  how='left', on=['商品ID'])

consumerPower = comment_Data[['使用者ID','價格','類群']].groupby("使用者ID").sum()
consumerPower = pd.concat([consumerPower,
                           comment_Data[['使用者ID','價格']].groupby("使用者ID").mean()], axis=1)
consumerPower.columns = ['總購買金額','類群','頻均購買金額']

for i in range(crub):
    getdata = consumerPower[consumerPower['類群']==i]
    plt.scatter(getdata['頻均購買金額'],getdata['總購買金額'], 
                color=colors[i], 
                label = i,
                alpha=0.5)
plt.title("消費者購買力分析圖",fontsize=60,fontproperties=myfont)#標題
plt.xlabel("平均購買金額",fontsize=40,fontproperties=myfont)#y的標題
plt.ylabel("總購買金額",fontsize=40,fontproperties=myfont) #x的標題
plt.legend(bbox_to_anchor=(1.03, 0.8), loc=2) # 設置圖例
plt.grid(True) # grid 開啟
plt.tight_layout()


#--- Tag使用排行
for  cla in product_Data['類群'].value_counts().index:
    data = product_Data[product_Data['類群']==cla]
    tag = []
    count = []
    for i in data['Tag'].tolist():
        for j in eval(i):
            if not(j in tag):
                tag.append(j)
                count.append(1)
            else:
                count[tag.index(j)] = count[tag.index(j)]+1
    dic = {
           'Tag':tag,
           '總使用數量':count
           }
    TagData = pd.DataFrame(dic)
    TagData = TagData.sort_values(by=['總使用數量'], ascending = False)

    #繪圖
    plt.bar(TagData['Tag'][:10],TagData['總使用數量'][:10],
            color=colors[2],
            alpha=0.5)
    plt.title("第"+str(cla)+"群Tag排名",fontsize=30,fontproperties=myfont)#標題
    plt.ylabel("總使用數量",fontsize=20,fontproperties=myfont)#y的標題
    plt.xlabel("Tag",fontsize=20,fontproperties=myfont) #x的標題
    plt.xticks(fontsize=10,rotation=90,fontproperties=myfont)
    plt.tight_layout()
    plt.savefig('群組'+str(cla)+'.png', dpi=300)
    plt.close()


for i in range(10):
    print('第'+str(i)+'群： '+str(product_Data[product_Data['類群']==i]['歷史銷售量'].sum()))
    
for i in range(10):
    print('第'+str(i)+'群： '+str(product_Data[product_Data['類群']==i]['歷史銷售量'].sum()/product_Data['歷史銷售量'].sum()*100))