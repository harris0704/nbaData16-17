#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-6-11 下午7:32
# @Author  : mj
# @Site    : 
# @File    : XGboost.py

from time import time
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import roc_curve,auc
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score


if __name__ == "__main__":

    dataPath = "../Power/binary.csv"
    data = pd.read_csv(dataPath, sep=',')
    del data['id']

    y = data['marker']
    del data['marker']
    X = data

    le = preprocessing.LabelEncoder().fit(y)
    print(le.classes_)
    y = le.transform(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print(X_train.shape, y_train.shape)
    print(X_test.shape, y_test.shape)

    print("-----------create DMatrix-----------")
    xg_train = xgb.DMatrix(X_train, label=y_train)
    xg_test = xgb.DMatrix(X_test, label=y_test)

    print("train xgb")
    param = {}
    # use softmax multi-class classification
    #
    param['objective'] = 'binary:logistic'
    # scale weight of positive examples
    param['eta'] = 0.1
    param['max_depth'] = 8
    param['silent'] = 1
    param['nthread'] = 4
    # param['num_class'] = 2

    watchlist = [(xg_train, 'train')]
    num_round = 256
    print('-' * 30 + 'train' + '-' * 30)
    bst = xgb.train(param,
                    xg_train,
                    num_round,
                    watchlist)

    y_pred = bst.predict(xg_test)

    print(y_pred)
    # print(recall_score(y_test, y_pred))
    fpr, tpr, threshold = roc_curve(y_test, y_pred)  ###计算真正率和假正率
    p, r, threshold = precision_recall_curve(y_test, y_pred)
    print(p)
    print(r)
    print(threshold)

    print("-" * 80)
    print("roc curve")
    fpr, tpr, threshold = roc_curve(y_test, y_pred)
    print(fpr)
    print(tpr)
    print(threshold)

    # print("{}".format())格式化输出