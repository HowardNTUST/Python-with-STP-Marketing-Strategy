# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 11:37:22 2020

@author: Ivan
"""

import pandas as pd
import platform

# 判斷是甚麼作業系統
theOS = list(platform.uname())[0]
if theOS == 'Windows':
    theOS = '\\'
    ecode = 'utf-8-sig'
else:
    theOS = '/'
    secode = 'utf-8'

#讀取檔案
comment_Data = pd.read_csv('data' + theOS + '運動內衣_留言資料.csv',encoding = ecode)


#--- 進行取代
#先取代全形字母
comment_Data['商品規格'] = comment_Data['商品規格'].str.replace('Ｓ','S')
comment_Data['商品規格'] = comment_Data['商品規格'].str.replace('Ｍ','M')
comment_Data['商品規格'] = comment_Data['商品規格'].str.replace('Ｌ','L')

#從最大的開始取代（大尺碼）
comment_Data['商品規格'] = comment_Data['商品規格'].str.replace('XXXXXXXXL','8@')
comment_Data['商品規格'] = comment_Data['商品規格'].str.replace('8XL','8@')
comment_Data['商品規格'] = comment_Data['商品規格'].str.replace('XXXXXXXL','7@')
comment_Data['商品規格'] = comment_Data['商品規格'].str.replace('7XL','7@')
comment_Data['商品規格'] = comment_Data['商品規格'].str.replace('XXXXXXL','6@')
comment_Data['商品規格'] = comment_Data['商品規格'].str.replace('6XL','6@')
comment_Data['商品規格'] = comment_Data['商品規格'].str.replace('XXXXXL','5@')
comment_Data['商品規格'] = comment_Data['商品規格'].str.replace('5XL','5@')
comment_Data['商品規格'] = comment_Data['商品規格'].str.replace('XXXXL','4@')
comment_Data['商品規格'] = comment_Data['商品規格'].str.replace('4XL','4@')
comment_Data['商品規格'] = comment_Data['商品規格'].str.replace('XXXL','3@')
comment_Data['商品規格'] = comment_Data['商品規格'].str.replace('3XL','3@')
comment_Data['商品規格'] = comment_Data['商品規格'].str.replace('XXL','2@')
comment_Data['商品規格'] = comment_Data['商品規格'].str.replace('2XL','2@')
comment_Data['商品規格'] = comment_Data['商品規格'].str.replace('XL','1@')

#從最小的開始取代（小尺碼）
comment_Data['商品規格'] = comment_Data['商品規格'].str.replace('XXS','3~')
comment_Data['商品規格'] = comment_Data['商品規格'].str.replace('3XS','3~')
comment_Data['商品規格'] = comment_Data['商品規格'].str.replace('XS','2~')

#取代特殊顏色
comment_Data['商品規格'] = comment_Data['商品規格'].str.replace('深灰','1#')
comment_Data['商品規格'] = comment_Data['商品規格'].str.replace('熒光綠','2#')
comment_Data['商品規格'] = comment_Data['商品規格'].str.replace('軍綠色','3#')
comment_Data['商品規格'] = comment_Data['商品規格'].str.replace('酒紅','4#')
comment_Data['商品規格'] = comment_Data['商品規格'].str.replace('深藍','5#')
comment_Data['商品規格'] = comment_Data['商品規格'].str.replace('墨綠','6#')
comment_Data['商品規格'] = comment_Data['商品規格'].str.replace('粉橘','7#')
comment_Data['商品規格'] = comment_Data['商品規格'].str.replace('紫粉','8#')
comment_Data['商品規格'] = comment_Data['商品規格'].str.replace('棗紅','9#')
comment_Data['商品規格'] = comment_Data['商品規格'].str.replace('寶藍','10#')

comment_Data['商品規格'] = comment_Data['商品規格'].str.replace('桃紅','桃')

color = ['黑','白','灰','綠','粉色','膚','橘','藍','紫色','咖啡色','焦糖','桃','紅'
         ,'黃','藏青','1#','2#','3#','4#','5#','6#','7#','8#','9#','10#']
size = ['8@','7@','6@','5@','4@','3@','2@','1@','L','M','S','2~','3~']

def evaluation(thestr):
    return eval(thestr)

# 把欄位的內容放入evaluation方法進行轉換
comment_Data['商品規格'] = comment_Data['商品規格'].apply(evaluation)
comment_Data['商品規格']

allpro = comment_Data['商品規格'].sum()#結果加總
allpro 

allpro = pd.DataFrame(allpro)
allpro.dropna(inplace=True)

#--- 創造市場SKU統計表
matrix=[]
for c in color:
    container=[]
    for s in size:
        container.append(
            len(allpro[ allpro[0].str.contains(c) &
                        allpro[0].str.contains(s)
                       ])
            )
    matrix.append(container)
        
buyer = pd.DataFrame(matrix)
buyer.columns = ['8XL','7XL','6XL','5XL','4XL','3XL','2XL','XL','L','M','S','XS','2XS']
buyer.index = ['黑','白','灰','綠','粉色','膚','橘','藍','紫色','咖啡色','焦糖','桃','紅','黃','藏青',
         '深灰','熒光綠','軍綠色','酒紅','深藍','墨綠','粉橘','紫粉','棗紅','寶藍']


#--- SKU尺寸百分比
buyer_precent = buyer.sum(axis = 0)/buyer.sum(axis = 0).sum()
buyer_precent = pd.DataFrame(buyer_precent,columns = ['SKU尺寸百分比'])





