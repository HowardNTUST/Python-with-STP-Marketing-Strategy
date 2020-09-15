# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 16:53:43 2019

@author: howar
"""

import pandas as pd
import numpy as np
import jieba
jieba.set_dictionary('dict.txt.big')
from Self_sentiment import Self_sentiment
sentiment = Self_sentiment()
sentiment.load('MultinomialNB') 
import plotly.express as px
import plotly.tools as tls
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot


def calculate_sentiment_pos(KoreaDrama,movie,col ):
        
    
    mv_sent= []
    for j in movie:
        star = KoreaDrama[KoreaDrama[col].str.contains(j)]
        print('計算'+ j +'的情緒分析....')
        
        if len(star)!=0:
            sent_temp = []
            for sent in star[col]:
                dist = sentiment.sentiment(sent) 
                sent_temp.append(dist.prob('pos'))
                
            mv_sent.append(np.mean(sent_temp))
        else:
            mv_sent.append(0)
    return mv_sent

def plt_cp_product(removeword, movie, bean, 
                   drama_cost , KoreaDrama):
        
    import matplotlib.pyplot as plt
    
    # 將我們關心的影劇名稱加入jieba的字典裡面
    for i in movie:
        jieba.add_word(i)
    
    KoreaDrama['標題與內容'] = KoreaDrama['標題'] +  KoreaDrama['內容']

    
    for word in removeword:
        KoreaDrama['標題與內容'] = KoreaDrama['標題與內容'].str.replace(word,'')
    
    #所有文章和標題都串在一起
    # theSTR = KoreaDrama['標題'].sum() + KoreaDrama['內容'].sum()
    theSTR = KoreaDrama['標題與內容'].tolist() 
    theSTR = ''.join(theSTR )

    #切詞
    words = list(jieba.cut(theSTR))
    
    #以影劇為單位，去計算每個影劇，在所有資料中的聲量
    mv_voice= []
    for j in movie:
        mv_voice.append(words.count(j))
    
    # 計算聲量的平均
    avg=np.mean(mv_voice)
    
    
    #------------基礎點陣圖與cp值清單-----------------
    score_avg = np.mean(bean)
    
    #繪圖
    plt.figure()
    
    #判斷四個象限所在的位置，來決定顏色
    voice_list =[]
    bean_list = []
    axe_list = []
    for i in range(len(bean)):
        if bean[i]>score_avg and mv_voice[i] >avg:#第一象限
            color = 'blue'
            axe = '第一象限'
            
        elif bean[i]>score_avg and mv_voice[i] <= avg:#第四象限
            color = 'green'
            axe = '第四象限'
            
        elif bean[i]<=score_avg and mv_voice[i] > avg:#第三象限
            color = 'red'
            axe = '第二象限'
            
        else:#第二象限
            color = 'black'
            axe = '第三象限'
            
        plt.scatter(bean[i],mv_voice[i], color=color)
        
        voice_list.append(mv_voice[i])
        bean_list.append(bean[i])
        axe_list.append(axe)
        
        
    plt.axhline(avg, color='c', linestyle='dashed', linewidth=1) # 繪製平均線 
    plt.axvline(score_avg, color='c', linestyle='dashed', linewidth=1) # 繪製平均線    
    
    plt.title("scatter",fontsize=30)#標題
    plt.ylabel("frequency",fontsize=15)#y的標題
    plt.xlabel("ratings",fontsize=15) #x的標題
    plt.legend()
    plt.show()
    
    
    # 製作清單
    voice_df = pd.DataFrame(voice_list, columns = ['聲量']) 
    bean_df = pd.DataFrame(bean_list, columns = ['評分'] ) 
    axe_df = pd.DataFrame(axe_list, columns = ['象限'] )     
    final1 = pd.concat([voice_df,bean_df,axe_df], axis = 1)
    final1['劇名']  = movie
    
    # 問題：請問要將final1輸出csv？ 名稱為：評分與聲量圖.csv
    final1.to_csv('評分與聲量圖.csv', encoding = 'cp950')
    
    
    #------------成本效益評估分析-----------------
    
    # 問題：我們可不可以加入每一則影劇的成本？（read_csv）
   
    
    # 計算聲量的平均，之後當做Y軸的分割線
    avg_cost=np.mean(drama_cost['cost'])
    
    fig = plt.figure(figsize=(15,10))
    voice_list =[]
    cost_list = []
    axe_list = []
    for i in range(len(drama_cost['cost'])):
        if drama_cost['cost'][i]>avg_cost and mv_voice[i] >avg:#第一象限
            color = 'blue'
            axe = '第一象限'
            
        elif drama_cost['cost'][i]>avg_cost and mv_voice[i] <= avg:#第四象限
            color = 'green'
            axe = '第四象限'
            
        elif drama_cost['cost'][i]<=avg_cost and mv_voice[i] > avg:#第三象限
            color = 'red'
            axe = '第二象限'
            
        else:#第二象限
            color = 'black'
            axe = '第三象限'
            
        plt.scatter(drama_cost['cost'][i],mv_voice[i], color=color, s = drama_cost['cost'][i]/10000)
        
        voice_list.append(mv_voice[i])
        cost_list.append(drama_cost['cost'][i])
        axe_list.append(axe)
        
        
    plt.axhline(avg, color='c', linestyle='dashed', linewidth=1) # 繪製平均線 
    plt.axvline(avg_cost, color='c', linestyle='dashed', linewidth=1) # 繪製平均線    
    
    plt.title("Cost-effectiveness analysis",fontsize=30)#標題
    plt.ylabel("frequency",fontsize=15)#y的標題
    plt.xlabel("cost",fontsize=15) #x的標題
    plt.legend()
    plt.show()
    fig.savefig('成本效益評估分析.png')
    
    
    # 製作清單
    voice_df = pd.DataFrame(voice_list, columns = ['聲量（關注程度）']) 
    cost_df = pd.DataFrame(cost_list, columns = ['成本'] ) 
    axe_df = pd.DataFrame(axe_list, columns = ['象限'] )     
    final1 = pd.concat([voice_df,cost_df,axe_df], axis = 1)
    final1['劇名']  = movie
    final1.to_csv('成本效益評估分析.csv', encoding = 'cp950')
    
    # 動態圖製作 - 成本效益評估分析
    fig = px.scatter(final1, x="成本", y="聲量（關注程度）", color="象限",
                     size='成本', hover_data=['劇名'])
    
    fig.update_layout(
            
            title = '成本效益評估分析',
            shapes=[
            
            # 設定X軸
            dict({
                'type': 'line',
                'x0': avg_cost,
                'y0': -10,
                'x1': avg_cost,
                'y1': final1['聲量（關注程度）'].max()*1.1,
                'line': {
                    'color': '#FF00FF',
                    'width': 5
                }}),
        
            # 設定Y軸
            dict({
                'type': 'line',
                'x0': 0,
                'y0': avg,
                'x1': final1['成本'].max()*1.1,
                'y1': avg,
                'line': {
                    'color': '#FF00FF',
                    'width': 5
                }})
        
        ])
    
    plot(fig, filename='成本效益評估分析.html')
    
    
    #--------------情緒分析圖------------#
    
    # 我們可不可以加入正負面聲量？
    from Self_sentiment import Self_sentiment
    sentiment = Self_sentiment()
    sentiment.load('MultinomialNB') 
    
    # 範例 
    content_self = '資料來源百百款，種類繁複，有些由人們所產生，有些則由機器所產生；有些資料存放在企業內部，極其珍貴，有些資料則屬於外部來源，讓資料科學家可以信手拈來。'
    
    dist= sentiment.sentiment(content_self)
    
    dist
    
    dist.prob('pos')   
    
    # 統計正負輿情 範例
    j = '來自星星的你'
    star = KoreaDrama[KoreaDrama['標題與內容'].str.contains(j)]
    star 
    dist= sentiment.sentiment(star['標題與內容'].iloc[0])
    dist.prob('pos') 
    
    # 計算不同韓劇的情緒分數
    from cp import calculate_sentiment_pos
    mv_sent = calculate_sentiment_pos(KoreaDrama=KoreaDrama,
                            movie=movie,
                            col='標題與內容' )
    mv_sent
    
    final1['情緒分數'] = mv_sent
    
    final1['評分'] = bean
    
    final1.to_csv('成本效益與情緒評估分析.csv', encoding = 'cp950')
    
    # 問題：將「動態圖製作 - 成本效益評估分析」的size變成「情緒分析」
    # title變成 「成本效益與情緒評估分析」
    fig = px.scatter(final1, x="成本", y="聲量（關注程度）", color="象限",
                     size='情緒分數', hover_data=['劇名'])
    
    fig.update_layout(
            
            title = '成本效益與情緒評估分析',
            shapes=[
            
            # 設定X軸
            dict({
                'type': 'line',
                'x0': avg_cost,
                'y0': -10,
                'x1': avg_cost,
                'y1': final1['聲量（關注程度）'].max()*1.1,
                'line': {
                    'color': '#FF00FF',
                    'width': 5
                }}),
        
            # 設定Y軸
            dict({
                'type': 'line',
                'x0': 0,
                'y0': avg,
                'x1': final1['成本'].max()*1.1,
                'y1': avg,
                'line': {
                    'color': '#FF00FF',
                    'width': 5
                }})
        
        ])
    
        
    plot(fig, filename='成本效益與情緒評估分析.html')
    return final1 
