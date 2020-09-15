# Importing the libraries
#from util import get_dummies
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier
from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score, precision_recall_curve, roc_curve, auc

import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False  
from matplotlib.font_manager import FontProperties 
import seaborn as sns 
myfont=FontProperties(fname='Microsoft JhengHei',size=14) 
sns.set(font=myfont.get_family()) 
sns.set_style("darkgrid",{"font.sans-serif":['Microsoft JhengHei']}) 


def get_dummies(dummy, dataset):
    ''''
    make variables dummies
    ref：http://blog.csdn.net/weiwei9363/article/details/78255210
    '''
    dummy_fields = list(dummy)
    for each in dummy_fields:
        dummies = pd.get_dummies( dataset.loc[:, each], prefix=each ) 
        dataset = pd.concat( [dataset, dummies], axis = 1 )
    
    fields_to_drop = dummy_fields
    dataset = dataset.drop( fields_to_drop, axis = 1 )
    return dataset
    

#-------------- modeling-------------------
def model(clf, plot_name,X_train,y_train,X_test,y_test) :
    model_ = clf.fit(X_train, y_train)
    y_pred = model_.predict(X_test)
    y_pred_prob = model_.predict_proba(X_test)[:,1]
    print("Training Accuracy = {:.3f}".format(model_.score(X_train, y_train)))
    print("Test Accuracy = {:.3f}".format(model_.score(X_test, y_test)))
#    print("ROC_AUC_score : %.6f" % (roc_auc_score(y_test, y_pred)))
    #Confusion Matrix
    print(confusion_matrix(y_test, y_pred))
    print("____________________{}分類報告____________________".format(plot_name))
    print(classification_report(y_test, y_pred))
    
    precision, recall, threshold = precision_recall_curve(y_test, y_pred_prob)
    fpr, tpr, _ = roc_curve(y_test, y_pred_prob)
    roc_auc = auc(fpr, tpr)
    
    #Plot Curves
    closest_zero = np.argmin(np.abs(threshold))
    closest_zero_p = precision[closest_zero]
    closest_zero_r = recall[closest_zero]
    fig, (ax1, ax2) = plt.subplots(nrows = 1, ncols = 2, figsize = [10,5])
    
    #Precision-Recall Curve
    ax1.plot(precision, recall)
    ax1.plot(closest_zero_p, closest_zero_r, 'o', markersize = 8, fillstyle = 'none', c = 'r')
    ax1.set_xlabel('Precision')
    ax1.set_ylabel('Recall')
    ax1.set_title(plot_name+" Precision-Recall Curve")

    #ROC Curve
    ax2.plot(fpr, tpr, label= 'ROC curve (AUC Score = {:0.3f}; Test Acc = {:0.3f})'.format((roc_auc), model_.score(X_test, y_test)))
    ax2.plot([0, 1], [0, 1], c = 'r', lw=2, linestyle='--')
    ax2.set_xlabel('False Positive Rate')
    ax2.set_ylabel('True Positive Rate')
    ax2.set_title(plot_name+' ROC curve')
    ax2.legend(loc = 'lower right')
    plt.tight_layout()
    
    fig.savefig(plot_name+'.png', dpi=300)  
    return confusion_matrix(y_test, y_pred), model_  







def predicted_profit_calculation(profit, cost, model_confusion_matrix):
    # 在全市場，客戶真實會購買的機率
    p_P = (model_confusion_matrix[1,:].sum()) / model_confusion_matrix.sum()

    #  在全市場，客戶真實不會購買的機率
    p_N = 1- p_P

    # 在p_P下，預測客戶會購買的期望獲利與成本
    p_P_profit = (model_confusion_matrix[1,1]/model_confusion_matrix[1,:].sum()) 
    p_P_cost = 1-p_P_profit


    # 在p_N下，預測客戶會不會購買的期望獲利與成本
    p_N_profit = (model_confusion_matrix[0,0]/model_confusion_matrix[0,:].sum()) 
    p_N_cost = 1-p_N_profit

    rf_profit_each_customer = p_P * (profit * p_P_profit + 0 * p_P_cost)+ p_N * (0 * p_N_profit + cost * p_N_cost )
    return rf_profit_each_customer