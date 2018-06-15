#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-6-12 下午1:49
# @Author  : mj
# @Site    : 
# @File    : xgboost_multi.py

from collections import Counter


import xgboost as xgb
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


def data_merge():
    """"""
    data = []
    file = "../Power/multiClass/day"
    for i in range(1, 16):
        fullfilePath = file + str(i) + ".csv"
        data.append(pd.read_csv(fullfilePath, sep=','))
    data = pd.concat(data, ignore_index=False)
    # ignore_index 保留原来的index
    data.to_csv("../Power/multi.csv")



if __name__ == "__main__":

    """
    train xgboost for power system dataSets for multi classification
    """

    # merge 15 data
    # data_merge()

    print('-' * 30 + 'load data' + '-' * 30)
    file = "../Power/multi.csv"
    data = pd.read_csv(file, sep=',')
    # print(data.describe())

    y = data['marker']
    del data['marker']
    X = data

    print('-' * 30 + 'label encoder ' + '-' * 30)
    le = LabelEncoder().fit(y)
    y = le.transform(y)
    print(le.classes_)
    print(Counter(y))

    print('-' * 30 + 'split train & test  ' + '-' * 30)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(X_train.shape, y_train.shape)
    print(X_test.shape, y_test.shape)

    print('-' * 30 + 'create xgb matrix  ' + '-' * 30)
    xg_train = xgb.DMatrix(X_train, label=y_train)
    xg_test = xgb.DMatrix(X_test)

    print('-' * 30 + 'set xgb params  ' + '-' * 30)
    param = {}
    # use softmax multi-class classification
    param['objective'] = 'multi:softmax'
    # scale weight of positive examples
    param['eta'] = 0.1
    param['max_depth'] = 2
    param['silent'] = 1
    param['nthread'] = 4
    param['num_class'] = 37

    watchlist = [(xg_train, 'train')]
    num_round = 50

    print('-' * 30 + 'train' + '-' * 30)
    bst = xgb.train(param,
                    xg_train,
                    num_round,
                    watchlist)
    print('-' * 30 + 'predict' + '-' * 30)

    y_pred = bst.predict(xg_test)

    print('-' * 30 + 'make p_r  ' + '-' * 30)

    p_r = classification_report(y_test, y_pred)
    print(p_r)