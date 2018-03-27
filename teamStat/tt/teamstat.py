#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-2-16 下午8:37
# @Author  : mj
# @Site    :
# @File    : nbaTeamstats.py

import time
import requests
from lxml import etree
import csv


def request(url, headers):
    try:
        html = requests.get(url, headers)
    except:
        time.sleep(30)
        html = request(url,headers)
    finally:
        return html





headers = {

}

startgameid = 400899375
endgameid = 400900608


basicurl = 'http://www.espn.com/nba/matchup?gameId='
for id in range(startgameid,endgameid):

    url = basicurl+"{}".format(id)
    # print(url)
    html = request(url,headers)

    html.encoding = 'utf-8'
    selector = etree.HTML(html.text)
    teamname = selector.xpath('//span[@class="short-name"]/text()')

    finalStates = selector.xpath('//span[@class="game-time status-detail"]/text()')
    print(finalStates)



    if teamname == [] or  finalStates[0].strip() == 'Postponed':
        pass
    else:
        print(url)
        info = []
        # 客队
        another = []
        # 主队
        home = []
        keduiScore = 0
        homeScore = 0
        score = selector.xpath('//tr/td[@class="final-score"]/text()')
        print(score)
        keduiScore = score[0].strip()
        homeScore = score[1].strip()

        # 1. FG Made-Attempted	总命中数
        FGMade_Attempted = selector.xpath("//tr[@data-stat-attr='fieldGoalsMade-fieldGoalsAttempted']/td/text()")
        # print(FGMade_Attempted)
        info.append(FGMade_Attempted[0].strip())
        another.append(FGMade_Attempted[1].strip())
        home.append(FGMade_Attempted[2].strip())

        # 2 Field Goal %	命中率
        fieldGoal = selector.xpath("//tr[@data-stat-attr='fieldGoalPct']/td/text()")
        # print(fieldGoal)
        info.append(fieldGoal[0].strip())
        another.append(fieldGoal[1].strip())
        home.append(fieldGoal[2].strip())

        # 3 3PT Made-Attempted	三分球命中数
        threePointAttempted = selector.xpath("//tr[@data-stat-attr='threePointFieldGoalsMade-threePointFieldGoalsAttempted']/td/text()")
        # print(threePointAttempted)
        info.append(threePointAttempted[0].strip())
        another.append(threePointAttempted[1].strip())
        home.append(threePointAttempted[2].strip())

        # 4 Three Point %	三分球命中率
        threePointFieldGoalPct = selector.xpath("//tr[@data-stat-attr='threePointFieldGoalPct']/td/text()")
        # print(threePointFieldGoalPct)
        info.append(threePointFieldGoalPct[0].strip())
        another.append(threePointFieldGoalPct[1].strip())
        home.append(threePointFieldGoalPct[2].strip())

        # 5 FT Made-Attempted	 罚球
        FT = selector.xpath("//tr[@data-stat-attr='freeThrowsMade-freeThrowsAttempted']/td/text()")
        # print(FT)
        info.append(FT[0].strip())
        another.append(FT[1].strip())
        home.append(FT[2].strip())

        # 6 Free Throw %	 罚球命中率
        freeThrowPct = selector.xpath("//tr[@data-stat-attr='freeThrowPct']/td/text()")
        # print(freeThrowPct)
        info.append(freeThrowPct[0].strip())
        another.append(freeThrowPct[1].strip())
        home.append(freeThrowPct[2].strip())

        # 7 Total Rebounds	总篮板数
        totalRebounds = selector.xpath("//tr[@data-stat-attr='totalRebounds']/td/text()")
        # print(totalRebounds)
        info.append(totalRebounds[0].strip())
        another.append(totalRebounds[1].strip())
        home.append(totalRebounds[2].strip())

        # 8 Offensive Rebounds	进攻篮板
        offRebounds = selector.xpath("//tr[@data-stat-attr='offensiveRebounds']/td/text()")
        # print(offRebounds)
        info.append(offRebounds[0].strip())
        another.append(offRebounds[1].strip())
        home.append(offRebounds[2].strip())

        # 9 Defensive Rebounds	防守篮板
        defRebounds = selector.xpath("//tr[@data-stat-attr='defensiveRebounds']/td/text()")
        # print(defRebounds)
        info.append(defRebounds[0].strip())
        another.append(defRebounds[1].strip())
        home.append(defRebounds[2].strip())

        # 10 Assists 助攻
        assists = selector.xpath("//tr[@data-stat-attr='assists']/td/text()")
        # print(assists)
        info.append(assists[0].strip())
        another.append(assists[1].strip())
        home.append(assists[2].strip())

        # 11 Steals	抢断
        steals = selector.xpath("//tr[@data-stat-attr='steals']/td/text()")
        # print(steals)
        info.append(steals[0].strip())
        another.append(steals[1].strip())
        home.append(steals[2].strip())

        # 12 Blocks	盖帽
        blocks = selector.xpath("//tr[@data-stat-attr='blocks']/td/text()")
        # print(blocks)
        info.append(blocks[0].strip())
        another.append(blocks[1].strip())
        home.append(blocks[2].strip())

        # 13 Total Turnovers	失误数
        totalTurnovers = selector.xpath("//tr[@data-stat-attr='totalTurnovers']/td/text()")
        # print(totalTurnovers)
        info.append(totalTurnovers[0].strip())
        another.append(totalTurnovers[1].strip())
        home.append(totalTurnovers[2].strip())

        # 14 Points Off Turnovers	利用失误转化得分
        pointsOffTurnovers = selector.xpath("//tr[@data-stat-attr='turnoverPoints']/td/text()")
        # print(pointsOffTurnovers)
        info.append(pointsOffTurnovers[0].strip())
        another.append(pointsOffTurnovers[1].strip())
        home.append(pointsOffTurnovers[2].strip())

        # 15 Fast Break Points	快攻得分
        fastPoints = selector.xpath("//tr[@data-stat-attr='fastBreakPoints']/td/text()")
        # print(fastPoints)
        info.append(fastPoints[0].strip())
        another.append(fastPoints[1].strip())
        home.append(fastPoints[2].strip())

        # 16 Points in Paint	内线得分
        pointsInPoint = selector.xpath("//tr[@data-stat-attr='pointsInPaint']/td/text()")
        # print(pointsInPoint)
        info.append(pointsInPoint[0].strip())
        another.append(pointsInPoint[1].strip())
        home.append(pointsInPoint[2].strip())

        # 17 Personal Fouls	犯规数
        fouls = selector.xpath("//tr[@data-stat-attr='fouls']/td/text()")
        # print(fouls)
        info.append(fouls[0].strip())
        another.append(fouls[1].strip())
        home.append(fouls[2].strip())

        # 18 Technical Fouls	技术犯规
        techFouls = selector.xpath("//tr[@data-stat-attr='technicalFouls']/td/text()")
        # print(techFouls)
        info.append(techFouls[0].strip())
        another.append(techFouls[1].strip())
        home.append(techFouls[2].strip())

        # 19 Flagrant Fouls	违体犯规
        flagrantFouls = selector.xpath("//tr[@data-stat-attr='flagrantFouls']/td/text()")
        # print(flagrantFouls)
        info.append(flagrantFouls[0].strip())
        another.append(flagrantFouls[1].strip())
        home.append(flagrantFouls[2].strip())

        print(info)
        print(another)
        print(home)

        with open(r'%s.csv' %(teamname[0]),'a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([id])
            writer.writerow([teamname[0], teamname[1]])
            writer.writerow([keduiScore,homeScore])
            writer.writerow(info)
            writer.writerow(another)
            writer.writerow(home)
            writer.writerow([])

        with open(r'%s.csv' %(teamname[1]),'a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([id])
            writer.writerow([teamname[0], teamname[1]])
            writer.writerow([keduiScore, homeScore])
            writer.writerow(info)
            writer.writerow(another)
            writer.writerow(home)
            writer.writerow([])

    time.sleep(10)