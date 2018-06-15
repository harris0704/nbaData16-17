#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-6-8 上午1:57
# @Author  : mj
# @Site    : 
# @File    : KFlod.py


from collections import Counter
from time import time

import numpy as np
import pandas as pd

from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import GroupKFold
from sklearn.model_selection import RepeatedKFold
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn import preprocessing
from sklearn.metrics import classification_report
import xgboost as xgb


if __name__ == "__main__":
    print(time())
    train_filePath = "../Power/binary/data1.csv"
    test_filePath = "../Power/binary/data2.csv"

    train_data = pd.read_csv(train_filePath)
    print(train_data.head())
    y_train = train_data['marker']
    del train_data['marker']
    X_train = train_data

    test_data = pd.read_csv(test_filePath)
    y_test = test_data['marker']
    del test_data['marker']
    X_test = test_data

    labelencoder = preprocessing.LabelEncoder()
    labelencoder.fit(y_train)
    y_train = labelencoder.transform(y_train)
    y_test = labelencoder.transform(y_test)
    print("-----------create DMatrix-----------")
    xg_train = xgb.DMatrix(X_train, label=y_train)
    xg_test = xgb.DMatrix(X_test, label=y_test)

    # setup parameters for xgboost
    param = {}
    # use softmax multi-class classification
    param['objective'] = 'binary:logistic'
    # scale weight of positive examples
    param['eta'] = 0.2
    param['max_depth'] = 8
    param['silent'] = 1
    param['nthread'] = 4
    # param['num_class'] = 2
    param['random_state'] = 42

    watchlist = [(xg_train, 'train')]
    num_round = 32
    print('-' * 30 + 'train' + '-' * 30)
    bst = xgb.train(param,
                    xg_train,
                    num_round,
                    watchlist)
    print('-' * 30 + 'predict' + '-' * 30)
    y_pred = bst.predict(xg_test)

    # P_R = classification_report(y_test, y_pred)
    # print(P_R)


    """
    显示器 1279
   
    cpu+主板1679
    ssd760P(或HD) 369
    电源500W 299
    内存8G 498
    机箱先马 179
    """
    print(y_pred)