# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 19:53:02 2020

@author: Ivan
"""
import jieba
import pandas as pd
import numpy as np
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
jieba.set_dictionary('tools'+theOS+'dict.txt.big')

alldata = pd.read_csv('data'+theOS+'pttData.csv',encoding = ecode)
all_board = ['Shock_Absorber','Nike','Under_Armour','Decathlon','Adidas','Puma','iFit']

#--- 統一品牌字詞
thestr = [x for x in alldata.columns if alldata[x].dtype == object]

for check in thestr:
    alldata[check] = alldata[check].str.replace('nike','Nike')
    alldata[check] = alldata[check].str.replace('NIKE','Nike')
    alldata[check] = alldata[check].str.replace('耐吉','Nike')
    
    alldata[check] = alldata[check].str.replace('健工','健身工廠')
    
    alldata[check] = alldata[check].str.replace('Shock Absorber','Shock_Absorber')
    alldata[check] = alldata[check].str.replace('Shock absorber','Shock_Absorber')
    alldata[check] = alldata[check].str.replace('shock absorber','Shock_Absorber')
    alldata[check] = alldata[check].str.replace('SHOCK ABSORBER','Shock_Absorber')
    
    alldata[check] = alldata[check].str.replace('adidas','Adidas')
    alldata[check] = alldata[check].str.replace('ADIDAS','Adidas')
    alldata[check] = alldata[check].str.replace('addias','Adidas')
    
    alldata[check] = alldata[check].str.replace('Under Armour','Under_Armour')
    alldata[check] = alldata[check].str.replace('Under armour','Under_Armour')
    alldata[check] = alldata[check].str.replace('under armour','Under_Armour')
    alldata[check] = alldata[check].str.replace('UNDER ARMOUR','Under_Armour')
    alldata[check] = alldata[check].str.replace('UA','Under_Armour')
    
    alldata[check] = alldata[check].str.replace('triumph','Triumph')
    alldata[check] = alldata[check].str.replace('TRIUMPH','Triumph')
    alldata[check] = alldata[check].str.replace('黛安芬','Triumph')
    
    alldata[check] = alldata[check].str.replace('decathlon','Decathlon')
    alldata[check] = alldata[check].str.replace('DECATHLON','Decathlon')
    alldata[check] = alldata[check].str.replace('迪卡農','Decathlon')
    alldata[check] = alldata[check].str.replace('迪卡儂','Decathlon')
    
    alldata[check] = alldata[check].str.replace('Uniqlo','Uniqlo')
    alldata[check] = alldata[check].str.replace('uniqlo','Uniqlo')
    
    alldata[check] = alldata[check].str.replace('2xu','2XU')
    
    alldata[check] = alldata[check].str.replace('puma','Puma')
    alldata[check] = alldata[check].str.replace('PUMA','Puma')
    alldata[check] = alldata[check].str.replace('寶馬','Puma')
    
    alldata[check] = alldata[check].str.replace('LuluLemom','Lulu_Lemom')
    alldata[check] = alldata[check].str.replace('lulu lemon','Lulu_Lemom')
    alldata[check] = alldata[check].str.replace('Lulu Lemom','Lulu_Lemom')
    alldata[check] = alldata[check].str.replace('Lulu lemom','Lulu_Lemom')
    alldata[check] = alldata[check].str.replace('LULU LEMOM','Lulu_Lemom')
    alldata[check] = alldata[check].str.replace('Lulu lemom','Lulu_Lemom')
    
    alldata[check] = alldata[check].str.replace('Lorna Jane','Lorna_Jane')
    alldata[check] = alldata[check].str.replace('Lorna jane','Lorna_Jane')
    alldata[check] = alldata[check].str.replace('lorna jane','Lorna_Jane')
    alldata[check] = alldata[check].str.replace('LornaJane','Lorna_Jane')
    alldata[check] = alldata[check].str.replace('LORNA JANE','Lorna_Jane')
    
    alldata[check] = alldata[check].str.replace('Via sweat','Via_Sweat')
    alldata[check] = alldata[check].str.replace('Via Sweat','Via_Sweat')
    alldata[check] = alldata[check].str.replace('via sweat','Via_Sweat')
    alldata[check] = alldata[check].str.replace('ViaSweat','Via_Sweat')
    alldata[check] = alldata[check].str.replace('VIASWEAT','Via_Sweat')
    
    alldata[check] = alldata[check].str.replace('VcStyle','Vc_Style')
    alldata[check] = alldata[check].str.replace('VC STYLE','Vc_Style')
    alldata[check] = alldata[check].str.replace('Vc Style','Vc_Style')
    alldata[check] = alldata[check].str.replace('Vc style','Vc_Style')
    alldata[check] = alldata[check].str.replace('VC style','Vc_Style')
    alldata[check] = alldata[check].str.replace('VC STYLE','Vc_Style')
    
    alldata[check] = alldata[check].str.replace('IFIT','iFit')
    alldata[check] = alldata[check].str.replace('ifit','iFit')
    
    alldata[check] = alldata[check].str.replace('mizuno','Mizuno')
    alldata[check] = alldata[check].str.replace('MIZUNO','Mizuno')
    
    alldata[check] = alldata[check].str.replace('Calvin Klein','Calvin_Klein')
    alldata[check] = alldata[check].str.replace('Calvin klein','Calvin_Klein')
    alldata[check] = alldata[check].str.replace('calvin klein','Calvin_Klein')
    alldata[check] = alldata[check].str.replace('CALVIN KLEIN','Calvin_Klein')
    
    alldata[check] = alldata[check].str.replace('舒服','舒適')
    alldata[check] = alldata[check].str.replace('好穿','舒適')
    
    
#--- 挑出提到「運動內衣」相關的標題、文章
underwearData = alldata[alldata['標題'].str.contains("運動內衣") |
                        alldata['標題'].str.contains("運動bra") |
                        alldata['內文'].str.contains("運動內衣") |
                        alldata['內文'].str.contains("運動bra") 
                        ]

#先創造出所有關於keyword與品牌的相關欄位
all_keyword = ['舒適','好看','推薦','跑步','重訓','健身','訓練']
kepword_analysis_Data = underwearData[['文章編碼','標題','內文','所有留言']]
kepword_analysis_Data['allSTR'] = kepword_analysis_Data['標題'] + ' ' + kepword_analysis_Data['內文'] + ' ' + kepword_analysis_Data['所有留言']
kepword_analysis_Data = kepword_analysis_Data.drop(columns=['標題','內文','所有留言'])

#創造keyword欄位
for ak in all_keyword:
    kepword_analysis_Data[ak] = np.where(kepword_analysis_Data['allSTR'].str.contains(ak),1,0)
#創造品牌欄位
for ab in all_board:
    kepword_analysis_Data[ab] = np.where(kepword_analysis_Data['allSTR'].str.contains(ab),1,0)
  
#--- 關鍵字比較圖  
container1 = []
for ak in  all_keyword:
    container2 = []
    for ab in all_board:
        bvoice = len(kepword_analysis_Data[kepword_analysis_Data[ab] == 1])
        kword = len(kepword_analysis_Data[(kepword_analysis_Data[ak] == 1) & (kepword_analysis_Data[ab] == 1)])
        container2.append(kword/bvoice)
    container1.append(container2)

for i,c,k in zip(container1,colorcompetitor[:len(container1)], all_keyword):
    plt.plot(all_board, i, color=c, label=k, marker='o')
plt.title("關鍵字比較圖",fontsize=30)#標題
plt.xlabel("品牌名稱",fontsize=20)#y的標題
plt.ylabel("關鍵字分數",fontsize=20) #x的標題
plt.xticks(fontsize=10,rotation=90)
plt.grid(True) # grid 開啟
plt.legend(bbox_to_anchor=(1.03, 0.8), loc=2) #開啟圖例
plt.tight_layout()



#兩種比較
container1 = []
for ab in all_board:
    container2 = []
    bvoice = len(kepword_analysis_Data[kepword_analysis_Data[ab] == 1])
    for ak in  all_keyword:
        kword = len(kepword_analysis_Data[(kepword_analysis_Data[ak] == 1) & (kepword_analysis_Data[ab] == 1)])
        container2.append(kword/bvoice)
    container1.append(container2)

for i,c,k in zip(container1,colorcompetitor[:len(container1)], all_board):
    plt.plot(all_keyword, i, color=c, label=k, marker='o')
plt.title("關鍵字比較圖",fontsize=30)#標題
plt.xlabel("品牌名稱",fontsize=20)#y的標題
plt.ylabel("關鍵字分數",fontsize=20) #x的標題
plt.xticks(fontsize=10,rotation=90)
plt.grid(True) # grid 開啟
plt.legend(bbox_to_anchor=(1.03, 0.8), loc=2) #開啟圖例
plt.tight_layout()



#--- 關鍵字五線譜分析
for ak in all_keyword:
    container = []
    for ab in all_board:
        bvoice = len(kepword_analysis_Data[kepword_analysis_Data[ab] == 1])
        kword = len(kepword_analysis_Data[(kepword_analysis_Data[ak] == 1) & (kepword_analysis_Data[ab] == 1)])
        
        container.append(kword/bvoice)

    plt.axhline(np.mean(container)+2*(np.std(container)), color=colorcompetitor[0], linestyle='dashed', linewidth=1) # 繪製平均線
    plt.axhline(np.mean(container)+np.std(container), color=colorcompetitor[1], linestyle='dashed', linewidth=1) # 繪製平均線
    plt.axhline(np.mean(container), color=colorcompetitor[2], linewidth=1) # 繪製平均線
    plt.axhline(np.mean(container)-np.std(container), color=colorcompetitor[3], linestyle='dashed', linewidth=1) # 繪製平均線
    plt.axhline(np.mean(container)-2*(np.std(container)), color=colorcompetitor[5], linestyle='dashed', linewidth=1) # 繪製平均線
    
    plt.plot(all_board, container, color=colorcompetitor[4], label=k, marker='o')
    plt.title("關鍵字五線譜分析－ "+ak,fontsize=30)#標題
    plt.xlabel("品牌名稱",fontsize=20)#y的標題
    plt.ylabel("關鍵字分數",fontsize=20) #x的標題
    plt.xticks(fontsize=10,rotation=90)
    plt.tight_layout()
    plt.savefig("關鍵字五線譜分析－ " + ak + '.png', dpi=300)
    plt.close()


#--- 雷達圖
container1 = []
for ab in all_board:
    container2 = []
    bvoice = len(kepword_analysis_Data[kepword_analysis_Data[ab] == 1])
    for ak in  all_keyword:
        kword = len(kepword_analysis_Data[(kepword_analysis_Data[ak] == 1) & (kepword_analysis_Data[ab] == 1)])
        container2.append(kword/bvoice)
    container1.append(container2)
    
# 繪圖
fig=plt.figure(figsize=(20,20))
ax = fig.add_subplot(111, polar=True)

N = len(container2)
angles=np.linspace(0, 2*np.pi, N, endpoint=False) # 設置雷達圖的角度，用於平分切開一個圓面
angles=np.concatenate((angles,[angles[0]])) # 為了使雷達圖一圈封閉起來，需要下面的步驟

# 構造數據
for da,c,ab in zip(container1, colorcompetitor, all_board):
    value=np.concatenate((np.array(da), np.array([da[0]])),axis=0)
    ax.plot(angles, value, 'o-', linewidth=2, label = ab,color=c)# 繪製折線圖
    ax.fill(angles, value, alpha=0.25,color=c)# 填充顏色

ax.set_thetagrids(angles * 180/np.pi, all_keyword) # 添加每個特徵的標籤
ax.set_ylim(0,1)# 設置雷達圖的範圍

# 設定字子大小
for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
             ax.get_xticklabels() + ax.get_yticklabels()):
    item.set_fontsize(20)

plt.title('雷達圖',fontsize=30) # 添加標題
ax.grid(True) # 添加網格線
plt.legend(bbox_to_anchor=(1.03, 0.8), loc=2,prop={'size':20}) # 設置圖例
plt.show() # 顯示圖形


#--- 雷達圖2（單一關鍵字） 
for plotX in all_board: # 主
    ccolor=[]
    for plotY in all_board: # 副
        if plotY == 'Nike':
            ccolor.append('#0000FF')
        else:       
            if plotX == plotY:
                ccolor.append('#FF0000')
            else:
                ccolor.append('#AAAAAA')
    fig=plt.figure(figsize=(30,30))
    ax = fig.add_subplot(111, polar=True)
    
    N = len(container2)
    angles=np.linspace(0, 2*np.pi, N, endpoint=False) # 設置雷達圖的角度，用於平分切開一個圓面
    angles=np.concatenate((angles,[angles[0]])) # 為了使雷達圖一圈封閉起來，需要下面的步驟

    # 構造數據
    for da,c,ab in zip(container1, ccolor, all_board):
        value=np.concatenate((np.array(da), np.array([da[0]])),axis=0)
        ax.plot(angles, value, 'o-', linewidth=2, label = ab,color=c)# 繪製折線圖
        ax.fill(angles, value, alpha=0.25,color=c)# 填充顏色
    
    ax.set_thetagrids(angles * 180/np.pi, all_keyword) # 添加每個特徵的標籤
    ax.set_ylim(0,1)# 設置雷達圖的範圍
    
    # 設定字子大小
    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
                 ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(20)
    
    plt.title('雷達圖',fontsize=30) # 添加標題
    ax.grid(True) # 添加網格線
    plt.legend(bbox_to_anchor=(1.03, 0.8), loc=2,prop={'size':20}) # 設置圖例
    plt.tight_layout()
    plt.savefig('雷達圖－'+plotX+'.png', dpi=300)
    plt.close()

#--- GPS定位圖
matrix_of_board_and_key = pd.DataFrame(container1)
matrix_of_board_and_key.columns = all_keyword
matrix_of_board_and_key.index = all_board

theVoice = []
for b in all_board:
    theVoice.append(kepword_analysis_Data[b].sum()**4)
    
for i in matrix_of_board_and_key.columns:
    for j in matrix_of_board_and_key.columns:
        if i == j:
            break;
        else:
            plt.figure(figsize=(20,10))
            # 繪製圓點
            plt.scatter(matrix_of_board_and_key[i],matrix_of_board_and_key[j],
                        color=colorcompetitor[:len(all_board)],
                        s=theVoice,
                        alpha=0.5)
            
            # 加上文字註解
            for tx,ty,ab in zip(matrix_of_board_and_key[i],matrix_of_board_and_key[j], all_board):
                plt.text(tx,ty,ab, fontsize=30 )
                
            plt.axvline(matrix_of_board_and_key[i].mean(), color='c', linestyle='dashed', linewidth=1) # 繪製平均線    
            plt.axhline(matrix_of_board_and_key[j].mean(), color='c', linestyle='dashed', linewidth=1) # 繪製平均線 
            
            plt.title("GPS定位圖 "+i+" V.S "+j,fontsize=40)#標題
            plt.ylabel(j,fontsize=30)#y的標題
            plt.xlabel(i,fontsize=30) #x的標題
            plt.tight_layout()
            plt.savefig('GPS定位圖'+i+'v.s'+j+'.png', dpi=300)
            plt.close()