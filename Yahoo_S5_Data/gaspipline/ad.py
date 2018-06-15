#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-6-12 下午8:51
# @Author  : mj
# @Site    : 
# @File    : ad.py

import sys
from collections import Counter
from time import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Power_SCADA import AnomalyDetection
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import auc, roc_curve


def eval(y_true, y_pred):
    # print(y_true)
    # print(y_pred)
    fpr, tpr, threshold = roc_curve(y_true, y_pred)  ###计算真正率和假正率
    roc_auc = auc(fpr, tpr)  ###计算auc的值
    plt.figure()
    lw = 2
    plt.figure(figsize=(10, 10))
    plt.plot(fpr, tpr, color='darkorange',
             lw=lw, label='ROC curve (area = %0.2f)' % roc_auc)  ###假正率为横坐标，真正率为纵坐标做曲线
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic example')
    plt.legend(loc="lower right")
    plt.show()



if __name__ == '__main__':
    """
    if len(sys.argv) != 2:
        print("Usage: XGboost for Power System Intrusion Detection ")
        print("Usage: python3 ad.py <multi, binary>")
        exit(-1)
        
    """
    print(sys.argv)

    object_argv = 'binary'

    if object_argv  == 'binary':
        file = './Power/binary.csv'
        print('binary classification\t\nfile path :{}'.format(file))

    if object_argv == 'multi':
        file = './Power/multi.csv'
        print('multi classification\t\nfile path: {}'.format(file))

    print("load data")
    data = pd.read_csv(file, sep=',')
    y = data['marker']
    del data['marker']
    print('label encoder')
    le = LabelEncoder().fit(y)
    y = le.transform(y, )
    print("label Counter{}".format(Counter(y)))

    myad = AnomalyDetection(object_argv, num_round=500)
    print(myad.__str__())
    myad.XGbooster_predict(data=data, y=y)
    myad.eval()
    y_true, y_pred = myad.xgbResult()
    print(y_true.shape, y_pred.shape)



