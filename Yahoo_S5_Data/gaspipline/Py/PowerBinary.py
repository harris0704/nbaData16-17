#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-6-11 下午3:55
# @Author  : mj
# @Site    : 
# @File    : PowerBinary.py

"""
try to use svc implements binary classification

"""
from time import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import classification_report


def data_merge():
    """"""
    data = []
    file = "../Power/binary/data"
    for i in range(1, 16):
        fullfilePath = file + str(i) + ".csv"
        data.append(pd.read_csv(fullfilePath, sep=','))
    data = pd.concat(data, ignore_index=False)
    # ignore_index 保留原来的index
    data.to_csv("../Power/binary2.csv")

def data_Pre():
    """svc 需要对数据进行标准化处理"""
    columns = data.columns
    # print(columns)
    i = 0
    # 将 所有的 inf 替换为 0
    where_are_inf= np.isinf(data)
    data[where_are_inf] = 0
    for col in columns :
        # label 无需标准化
        if col== 'marker': continue
        # print(i, col)
        i = i + 1
        # 先转化 np.nan np.inf 这类可能会出现异常的值
        data[col] = np.nan_to_num(data[col])
        data[col] = preprocessing.scale(data[col])
        print(i, col, data[col].mean(axis=0), data[col].std(axis=0))

def split_train_test(data, test_ratio):
    """
    自定义随机切分函数
    :param data:
    :param test_ratio:
    :return:
    """
    shuffled_indices = np.random.permutation(len(data))
    test_set_size = int(len(data) * test_ratio)
    test_indices = shuffled_indices[:test_set_size]
    train_indices = shuffled_indices[test_set_size:]

    return data.iloc[train_indices], data.iloc[test_indices]

def use_Random_Split(X, y, test_size=0.1):
    """
    使用sklearn中的切分函数来切分数据集,直接返回切分结果
    :param X:
    :param y:
    :return: X_train, y_train, X_test, y_test
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, test_size=test_size)

    return X_train, y_train, X_test, y_test



if __name__ == "__main__":

    """
    # merge 15 data.csv into a new data.csv
    print("merge all data.csv into a new data file")
    data_merge()
    """
    """load the data"""
    dataPath = "../Power/binary.csv"
    data = pd.read_csv(dataPath, sep=',')
    del data['id']
    """"
    # print(data.info())
    counter = data['marker'].value_counts()
    print(counter)
    
    Attack     55663   0 
    Natural    22714   1
    """
    """lable encoder"""
    le = LabelEncoder().fit(data['marker'])
    print(le.classes_)
    data['marker'] = le.transform(data['marker'])
    counter = data['marker'].value_counts()
    print(counter)

    """预处理数据"""
    data_Pre()

    """切分数据集为测试集和训练集"""
    # 4:1
    X_train, X_test = split_train_test(data, test_ratio=0.2)
    print(X_train.shape, X_test.shape)
    y_train = X_train['marker']
    del X_train['marker']
    y_test = X_test['marker']
    del X_test['marker']
    print(X_train.shape, y_train.shape)
    print(X_test.shape, y_test.shape)

    """train SVC"""

    svc_clf = SVC(C=1.0,
                  kernel='rbf',
                  gamma='auto',
                  decision_function_shape='ovo',
                  random_state=42)
    svc_clf.fit(X_train, y_train)
    """predict SVC"""
    y_pred = svc_clf.predict(X_test)

    print(y_pred)

    print(precision_score(y_test, y_pred))
    print(recall_score(y_test, y_pred))