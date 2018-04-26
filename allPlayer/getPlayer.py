#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-3-8 下午4:49
# @Author  : mj
# @Site    : 
# @File    : getPlayer.py

import time
import requests
from lxml import etree
import csv


# request 方法
def request(url, headers):
    # html = requests.get(url, headers)
    # return html
    try:
        html = requests.get(url, headers)
    except:
        time.sleep(5)
        html = request(url, headers)
    finally:
        return html

# def getFullName(url):
#     headers = {}
#     html = request(url, headers)
#     selector = etree.HTML(html.text)
#     fulName = selector.xpath('//*[@id="content"]/div[3]/div[2]/h1/text()')
#     # print(fulName)
#     print(fulName)
#     return fulName


def getFullName(url):
    headers = {}
    if url in map.keys():
        fullName = map[url]
        return fullName
    else:
        html = request(url, headers)
        selector = etree.HTML(html.text)
        fullName = selector.xpath('//*[@id="content"]/div[3]/div[2]/h1/text()')
        map.update({url:fullName})
        return map[url]


headers = {

}

# startgameid = 400899375
startgameid = 400900521
# endgameid = 400900000
endgameid = 400900608
basicurl = 'http://www.espn.com/nba/boxscore?gameId='
for id in range(startgameid,endgameid):

    map = {}

    url = basicurl+"{}".format(id)
    # print(url)
    html = request(url, headers)
    selector = etree.HTML(html.text)
    # NBA 队名
    # index = 0 客队
    # index = 1 主队
    teamname = selector.xpath('//span[@class="short-name"]/text()')
    print(teamname)
    # info
    # 比赛状态
    finalStates = selector.xpath('//span[@class="game-time status-detail"]/text()')
    print(finalStates)
    ###############
    if teamname == [] or finalStates[0].strip() == 'Postponed':
        pass
    else:
        home = teamname[1]
        # 主队
        another = teamname[0]
        # 客队
        print(url)

        score = selector.xpath('//tr/td[@class="final-score"]/text()')
        print(score)
        # keduiScore = score[0].strip()
        # homeScore = score[1].strip()
        # print(type(keduiScore))
        # teamname = teamname+[keduiScore,homeScore]
        # 客队先发
        keduiX = selector.xpath('//*[@id="gamepackage-boxscore-module"]/div/div[1]/div/div[1]/table/tbody[1]/tr')
        for x in keduiX:
            name = x.xpath('td/a/span[@class="abbr"]/text()')
            position = x.xpath('td/span[@class="position"]/text()')
            nameUrl = x.xpath('td/a/@href')
            data = x.xpath('td/text()')

            if nameUrl != []:
                name = getFullName(nameUrl[0])
                print(position,name)
                if name != []:
                    # print(name)
                    with open(r'%s.csv' % (name[0]), 'a') as w:
                        writer_k = csv.writer(w)
                        writer_k.writerow(name + position +[another]+ [id] + ['1'] + data )
                else:
                    pass

        keduiT = selector.xpath('//*[@id="gamepackage-boxscore-module"]/div/div[1]/div/div[1]/table/tbody[2]/tr')
        # 客队替补
        for t in keduiT:
            name = t.xpath('td/a/span[@class="abbr"]/text()')
            position = t.xpath('td/span[@class="position"]/text()')
            nameUrl = t.xpath('td/a/@href')
            data = t.xpath('td/text()')
            if nameUrl != []:
                name = getFullName(nameUrl[0])
                print(position, name)
                if name != []:
                    # print(name)
                    with open(r'%s.csv' % (name[0]), 'a') as w:
                        writer_k = csv.writer(w)
                        writer_k.writerow(name + position +[another]+ [id] + ['0'] + data )
                else:
                    pass
            # if name != [] and nameUrl != [] :
            #     name = getFullName(nameUrl[0])
            #     with open(r'%s.csv' % (name[0]), 'a') as w:
            #         writer_k = csv.writer(w)
            #         writer_k.writerow(name + position + [another] +[id] + ['0'] + data)

        homeX = selector.xpath('//*[@id="gamepackage-boxscore-module"]/div/div[2]/div/div[1]/table/tbody[1]/tr')
        # 主队先发
        for x in homeX:
            name = x.xpath('td/a/span[@class="abbr"]/text()')
            position = x.xpath('td/span[@class="position"]/text()')
            nameUrl = x.xpath('td/a/@href')
            data = x.xpath('td/text()')
            if nameUrl != []:
                name = getFullName(nameUrl[0])
                print(position, name)
                if name != []:
                    with open(r'%s.csv' % (name[0]), 'a') as w:
                        writer_k = csv.writer(w)
                        writer_k.writerow(name + position +[home]+ [id] + ['1'] + data )
                else:
                    pass
            # if name != [] and nameUrl != []:
            #     name = getFullName(nameUrl[0])
            #     with open(r'%s.csv' % (name[0]), 'a') as w:
            #         writer_h = csv.writer(w)
            #         writer_h.writerow(name + position +[home] +[id] + ['1'] + data )
        #
        homeT = selector.xpath('//*[@id="gamepackage-boxscore-module"]/div/div[2]/div/div[1]/table/tbody[2]/tr')
        # 主队替补
        for t in homeT:
            name = t.xpath('td/a/span[@class="abbr"]/text()')
            position = t.xpath('td/span[@class="position"]/text()')
            nameUrl = t.xpath('td/a/@href')
            data = t.xpath('td/text()')
            if nameUrl != []:
                name = getFullName(nameUrl[0])
                print(position, name)
                if name != []:
                    with open(r'%s.csv' % (name[0]), 'a') as w:
                        writer_k = csv.writer(w)
                        writer_k.writerow(name + position +[home]+ [id] + ['0'] + data )
                else:
                    pass
            # if name != [] and nameUrl != []:
            #     name = getFullName(nameUrl[0])
            #     with open(r'%s.csv' % (name[0]), 'a') as w:
            #         writer_h = csv.writer(w)
            #         writer_h.writerow(name + position +[home] + [id] + ['0'] + data)
        time.sleep(10)