#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-2-19 下午12:24
# @Author  : mj
# @Site    : 
# @File    : playbyplay.py

import time
import requests
from lxml import etree
import csv


def request(url, headers):
    try:
        html = requests.get(url, headers)
    except:
        time.sleep(30)
        html = request(url, headers)
    finally:
        return html

headers = {

}



startgameid = 400899375
endgameid = 400900608
# http://www.espn.com/nba/playbyplay?gameId=
basicurl = 'http://www.espn.com/nba/playbyplay?gameId='
for id in range(startgameid, endgameid):

    url = basicurl+"{}".format(id)
    # print(url)
    html = request(url, headers)

    html.encoding = 'utf-8'
    selector = etree.HTML(html.text)
    teamname = selector.xpath('//span[@class="short-name"]/text()')

    finalStates = selector.xpath('//span[@class="game-time status-detail"]/text()')
    print(finalStates)



    if teamname == [] or  finalStates[0].strip() == 'Postponed':
        pass
    else:
        print(url)

        keduiScore = 0
        homeScore = 0

        score = selector.xpath('//tr/td[@class="final-score"]/text()')
        print(score)
        keduiScore = score[0].strip()
        homeScore = score[1].strip()

        # filename = aVSb s:s
        filename = teamname[0]+" "+teamname[1]+" "+str(keduiScore)+":"+str(homeScore)

        print(filename)
        times = selector.xpath("//td[@class='time-stamp']/text()")
        play = selector.xpath("//td[@class='game-details']/text()")
        score = selector.xpath("//td[@class='combined-score']/text()")

        with open(r'%s.csv' %(filename),"w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["time", "play", "score"])
            for i in range(len(times)):
                writer.writerow([times[i], play[i], score[i]])

    time.sleep(10)
