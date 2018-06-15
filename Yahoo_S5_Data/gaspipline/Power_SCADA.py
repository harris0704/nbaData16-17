#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-6-12 下午8:21
# @Author  : mj
# @Site    : 
# @File    : Power_SCADA.py

import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import auc, roc_curve
import matplotlib.pyplot as plt
from xgboost import DMatrix


class AnomalyDetection():

    # params 设置booster参数
    _params = {}

    def __init__(self, object, num_round=300):

        """
        xg_train
        xg_test

        Learning task params:
        objective   目标函数
        eval_metric 评价指标
        seed        随机数种子 (用于模型复现)

        y_pred 预测结果
        y_true
        """
        self.xg_train = None
        self.xg_test = None

        if object == 'binary':
            self.objective = 'binary:logistic'
            self.classes = 2
        else:
            self.objective = 'multi:softmax'
            self.classes = 37
        self.seed = 42

        # The number of rounds for boosting
        self.num_round = num_round
        self.early_stopping_rounds = None

        self.y_pred = None
        self.y_ture = None


    def __str__(self):
        s = self.objective
        if self.xg_train != None:
            s = s + 'train data loaded!'
        else:
            s = s + 'train data need to be loaded!'

        if self.xg_test != None:
            s = s + 'train data loaded!'
        else:
            s = s + 'train data need to be loaded!'


        return s

    def _setter(self, eta, max_depth):
        """
        设置 booster 参数
        参数放在 _params

        具体参数:
        eta 学习率
        max_depth
        subsample

        """
        self._params['eta'] = eta
        self._params['max_depth'] = max_depth
        self._params['subsample'] = 0.8

        self._params['nthread'] = 4
        self._params['silent'] = 1



    def train_xgb(self, data, y, max_depth):

        """

        :param data:
        :param y:
        :param max_depth:
        :return:
        """
        self._setter(eta=0.1, max_depth=max_depth)

        X_train, X_test, y_train, y_test = train_test_split(data, y, test_size=0.2, random_state=42)
        print('X_train.shape:\t {}\n'.format(X_train.shape) + 'y_train.shape:\t{}\n'.format(y_train.shape))
        print('X_test.shape:\t{}\n'.format(X_test.shape) + 'y_test.shape:\t{}\n'.format(y_test.shape))

        self.xg_train = DMatrix(X_train, label=y_train)
        self.xg_test = DMatrix(X_test)
        self.y_ture = y_test

        watchlist = [(self.xg_train, 'train')]
        print(type(self.xg_train))
        print("train XGboost")
        bst = xgb.train(self._params,
                        self.xg_train,
                        self.num_round
                        # self.early_stopping_rounds
                        # watchlist = [(self.xg_train, 'train')]
                        )

        return bst

    def XGbooster_predict(self, data, y):

        self.y_pred = self.train_xgb(data, y, max_depth=6)\
            .predict(self.xg_test)

        print(self.y_pred)

        return self.y_pred


    def xgbResult(self):
        """

        :return: y_true, y_pred
        """
        return self.y_ture, self.y_pred

    def logisticOutput(self):

        """
        将XGboost leaves data one hot encoder

        :return:
        """

    def eval(self):

        fpr, tpr, threshold = roc_curve(self.y_ture, self.y_pred)  ###计算真正率和假正率
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
        plt.savefig("result1.png")
        plt.show()



