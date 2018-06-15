#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-6-5 下午5:20
# @Author  : mj
# @Site    : 
# @File    : test.py

import hashlib
from time import time
from collections import Counter

import numpy as np
import pandas as pd
import xgboost as xgb
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold
from sklearn import preprocessing
from sklearn.metrics import classification_report



def test_set_check(identifier, test_radio, hash=hashlib.md5):
    return hash(np.int64(identifier)).digest()[-1] < 256 * test_radio

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

def use_KFlod(X, n_splits):
    """
    K-折交叉验证,未完成
    :param X:
    :param y:
    :param n_splits:
    :return:
    """
    cv = StratifiedKFold(n_splits=n_splits,shuffle=True, random_state=None)
    for train_index, test_index in cv.split(X):

    # cv = KFold(n_splits=n_splits, shuffle=True)
    # for train_index, test_index in cv.split(X, y):
        print(train_index, test_index)
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        print(len(train_index), len(test_index))

        # X_train, X_test = X[train_index], X[test_index]
        # y_train, y_test = y[train_index], y[test_index]
        # print(X_train.shape, y_train.shape)
        # print(X_test.shape, y_test.shape)

def dataPre(X, y):
    """

    :param X:
    :param y:
    :return:
    """

    return X, y


def train_xgb():
    """
    :param X_train:
    :param y_train:
    :return:
    """
    print("-----------create DMatrix-----------")
    xg_train = xgb.DMatrix(X_train, label=y_train)
    xg_test = xgb.DMatrix(X_test, label=y_test)

    # setup parameters for xgboost
    param = {}
    # use softmax multi-class classification
    param['objective'] = 'multi:softmax'
    # scale weight of positive examples
    param['eta'] = 0.2
    param['max_depth'] = 2
    param['silent'] = 1
    param['nthread'] = 4
    param['num_class'] = 8

    watchlist = [(xg_train, 'train')]
    num_round = 30
    print('-' * 30 + 'train' + '-'*30)
    bst = xgb.train(param,
                    xg_train,
                    num_round,
                    watchlist)
    print('-' * 30 + 'predict' + '-'*30)
    y_pred = bst.predict(xg_test)

    return y_pred

if __name__ == "__main__":

    filePath = "../ModbusRTUfeatureSetsV2/Multiclass FeatureSets/MulticlassResponseInjectionV2.csv"
    # filePath = "/home/hmj/PycharmProjects/Jupyter Notebook/Gas Pipeline/GasData.csv"
    data = pd.read_csv(filePath, sep=',')
    y = data[' Label']
    # del data[' Label']

    """
    按照9:1切分数据集
    三种方式 
    """


    """
    Object 数据统计信息
    
    10个Object类型的字段
    Address CommandResponse ControlMode ControlScheme FunctionCode InvalidDataLength InvalidFunctionCode PumpState SolenoidState
    
    print(Counter(data['Address'])) 
    # Counter({'0x4': 29308, '0x0': 1})
    print(Counter(data['CommandResponse']))
    # Counter({'Response': 29304, 'X': 5})
    print(Counter(data['ControlMode'])) 
    # Counter({'X': 29309})
    print(Counter(data['ControlScheme']))
    # Counter({'X': 29309})
    print(Counter(data['FunctionCode'])) 
    # Counter({'0x3': 15274, '0x10': 14034, '0x40': 1})
    print(Counter(data['InvalidDataLength'])) 
    # Counter({'X': 29306, 'InvalidDataLength': 3})
    print(Counter(data['InvalidFunctionCode'])) 
    # Counter({'X': 29308, 'InvalidFunctionCode': 1})
    print(Counter(data['PumpState'])) 
    # Counter({'X': 14039, 'OnPumpState': 11737, 'OffPumpState': 3533})
    print(Counter(data['SolenoidState'])) 
    # Counter({'X': 14039, 'OffSolenoidState': 8314, 'OnSolenoidState': 6956})
    print(Counter(data[' Label']))  
    # Counter({'Good': 28070, 'Slow': 306, 'Fast': 225, 'Burst': 217, 'Setpoint': 171, 'Wave': 168, 'Negative': 119, 'Single': 33})
    
    数字类型变量 float64(2) int64(15)
     
    """

    print('-' *30 + '标签属性转化' + '-' * 30)
    # 16进制属性
    Columns_0x = ['Address', 'FunctionCode']
    # 标签属性 包括结果标签
    Columns = ['CommandResponse', 'ControlMode', 'ControlScheme', 'InvalidDataLength', 'InvalidFunctionCode', 'PumpState', 'SolenoidState', ' Label']
    for column in Columns:
        """所有Object属性全部用LabelEncoder处理"""
        labelencoder = preprocessing.LabelEncoder()
        labelencoder.fit(data[column])
        print(labelencoder.classes_)
        data[column] = labelencoder.transform(data[column])
    print('-' * 30 + '转化16进制地址属性' + '-' * 30)
    for column in Columns_0x:
        data[column] = data[column].map(lambda x: int(x, 16))
    # print(data.info())

    print('-' * 30 + '切分数据集' + '-' * 30)
    # 1. use_KFlod(data, 10)
    # 2. use_Random_Split(data, y)

    train_set, test_set = split_train_test(data, test_ratio=0.2)
    # 列名
    # print(train_set.columns)
    # 输出列信息
    # print(train_set.info())

    data.to_csv("./data.csv")

    y_train = train_set[' Label']
    del train_set[' Label']
    X_train = train_set

    y_test = test_set[' Label']
    del test_set[' Label']
    X_test = test_set

    # X_train.to_csv("./train.csv")
    # X_test.to_csv("./test.csv")
    print(X_train.shape, y_train.shape)
    print(X_test.shape, y_test.shape)
    # print(X_train)
    print('-' * 30 + '训练XGBoost, 得到结果 y_pred ' + '-' * 30)
    start_time = time()
    y_pred = train_xgb()
    print("time:" + str(time() - start_time) + "s")
    target_names = ['Burst', 'Fast', 'Good', 'Negative', 'Setpoint', 'Single', 'Slow', 'Wave']
    print('-' * 30 + '计算每个类别的 Precision Recall f1-score ' + '-' * 30)
    P_R = classification_report(y_test, y_pred, target_names=target_names)
    print(P_R)