import time
import pandas as pd
from datetime import datetime, timedelta
from fpldb.logger.logger import logger
from fpldb.utils.typesUtil import PlayerPosition
from fpldb.api.officialFPL.officialFPLApi import OfficialFPLApi
from fpldb.api.liveFPLScrape.liveFPLScrape import LiveFPLScrape
from fpldb.dashboardService.analytics.basicAnalytics import BasicAnalytics

class LiveFPLDatastore:

    def __init__(self):
        self.playerData = {}
        self.fixtureData = {}
        self.bestInEachPosition = {}

    def setPlayerData(self, data):
        self.playerData = data

    def setBIEPData(self, data):
        self.bestInEachPosition = data

    def setFixtureData(self, data):
        self.fixtureData = data

    def getPlayersData(self):
        return self.playerData

    def getBIEPData(self):
        return self.bestInEachPosition

    def getFixturesData(self):
        return self.fixtureData

    def getPlayerLiveData(self, playerId):
        return self.playerData.get(playerId, None)

    def getFixtureLiveData(self, fixtureId):
        return self.fixtureData.get(fixtureId, None)

    def getAllFixtures(self):
        return list(self.fixtureData.values())

    def isEmpty(self):
        return not (len(self.playerData) and len(self.fixtureData))

class LiveFPLAverageCollector():

    scrappedData = None
    sleepTime = None

    @staticmethod
    def isEmpty():
        if LiveFPLAverageCollector.scrappedData is None or LiveFPLAverageCollector.scrappedData.isEmpty():
            return True
        return False

    @staticmethod
    def saveData(a):
        LiveFPLAverageCollector.scrappedData.top10KAvg = a['top10KAvg']
        LiveFPLAverageCollector.scrappedData.top10KHitsAvg = a['top10KHitsAvg']
        LiveFPLAverageCollector.scrappedData.top10KHitsInclAvg = a['top10KHitsInclAvg']
        LiveFPLAverageCollector.scrappedData.overallAvg = a['overallAvg']
        LiveFPLAverageCollector.scrappedData.overallHitsAvg = a['overallHitsAvg']
        LiveFPLAverageCollector.scrappedData.overallHitsInclAvg = a['overallHitsInclAvg']
        LiveFPLAverageCollector.scrappedData.gw = a['gameweekNumber']

    @staticmethod
    def run(dataStore, sleepTime = 300):

        LiveFPLAverageCollector.scrappedData = dataStore
        LiveFPLAverageCollector.sleepTime = sleepTime

        while True:
            if LiveFPLMatchDataCollector.isMatchPlaying() or LiveFPLAverageCollector.isEmpty():
                a = LiveFPLScrape.getLiveAverages()
                LiveFPLAverageCollector.saveData(a)
            time.sleep(LiveFPLAverageCollector.sleepTime)

class LiveFPLMatchDataCollector():

    liveDatastore = None
    gw = None
    sleepTime = None
    staticTeamData = OfficialFPLApi.getStaticTeamData()
    staticPlayerData = OfficialFPLApi.getStaticPlayerData()

    @staticmethod
    def isMatchPlaying(offset = 300, retryEnabled = True, retrySleepTime = 5, retryCount = 5):
        while True and retryEnabled and retryCount > 0:
            try:
                fixtureList = OfficialFPLApi.getFixtures(LiveFPLMatchDataCollector.gw)
                fixtureTimes = [(pd.to_datetime(x['kickoff_time']), pd.to_datetime(x['kickoff_time']) + timedelta(minutes = 115))  for x in fixtureList]
                for fixtureTime in fixtureTimes:
                    if fixtureTime[0] <= datetime.now(fixtureTime[0].tzinfo) and datetime.now(fixtureTime[1].tzinfo) <= fixtureTime[1]:
                        return True
                return False
            except Exception as e:
                time.sleep(retrySleepTime)
                retryCount -= 1
        raise Exception('No data returned from API')

    @staticmethod
    def run(datastore, gw, sleepTime = 120):

        LiveFPLMatchDataCollector.liveDatastore = datastore
        LiveFPLMatchDataCollector.gw = gw
        LiveFPLMatchDataCollector.sleepTime = sleepTime

        while True:
            if LiveFPLMatchDataCollector.isStoreEmpty() or LiveFPLMatchDataCollector.isMatchPlaying():
                livePlayerData, liveFixtureData = LiveFPLMatchDataCollector.getLiveData()
                simulatedBonusPoints = LiveFPLMatchDataCollector.simulateBonusPoints(liveFixtureData)
                LiveFPLMatchDataCollector.updateLivePlayerData(livePlayerData, simulatedBonusPoints)
                LiveFPLMatchDataCollector.saveLiveData(livePlayerData, liveFixtureData)

                bestInEachPosition = {}
                BasicAnalytics.getBestInEachPositionLive(bestInEachPosition, LiveFPLMatchDataCollector.liveDatastore.getPlayersData())
                LiveFPLMatchDataCollector.liveDatastore.setBIEPData(bestInEachPosition)
            time.sleep(LiveFPLMatchDataCollector.sleepTime)

    @staticmethod
    def getStatFromFixtureStats(data, stat='bps'):
        for item in data:
            if item['identifier'] == stat:
                return item

    @staticmethod
    def simulateBonusPoints(liveFixtureData):
        scoreChart = {
            0 : 3,
            1 : 2,
            2 : 1
        }
        bonusMap = {}
        for fixture in liveFixtureData:
            kickOffTime = pd.to_datetime(fixture['kickoff_time'])
            if fixture['finished'] != True and kickOffTime <= datetime.now(kickOffTime.tzinfo):
                activeBps = LiveFPLMatchDataCollector.getStatFromFixtureStats(fixture['stats'])
                awayHomeBps = []
                bpsMap = {}
                if activeBps is not None:
                    if 'a' in activeBps:
                        awayHomeBps.extend(activeBps['a'])
                    if 'h' in activeBps:
                        awayHomeBps.extend(activeBps['h'])
                    for p in awayHomeBps:
                        if p['value'] in bpsMap:
                            bpsMap[p['value']].append(p['element'])
                        else:
                            bpsMap[p['value']] = [p['element']]
                    bpsList = sorted(bpsMap.keys(), reverse=True)
                    for idx, bps in enumerate(bpsList):
                        currentBonus = scoreChart.get(idx, -1)
                        if currentBonus == -1:
                            break
                        for player in bpsMap[bps]:
                            bonusMap[player] = {
                                'fixtureId': fixture['id'],
                                'bonus': currentBonus
                            }
        return bonusMap

    @staticmethod
    def updateLivePlayerData(livePlayerData, simulatedBonusPoints):
        playerMap = {x['id']:x for x in livePlayerData['elements']}
        for playerId in simulatedBonusPoints:
            playerData = playerMap[playerId]
            bonusData = simulatedBonusPoints[playerId]
            playerData['stats']['total_points'] += bonusData['bonus']
            playerData['stats']['provisional_bonus'] = bonusData['bonus']
            explainSection = playerData['explain']
            for fixtureData in explainSection:
                if fixtureData['fixture'] == bonusData['fixtureId']:
                    fixtureStats = fixtureData['stats']
                    fixtureStats.append({
                        'identifier':'provisional_bonus',
                        'points':bonusData['bonus'],
                        'value': bonusData['bonus'],
                    })
                    break

    @staticmethod
    def isStoreEmpty():
        return LiveFPLMatchDataCollector.liveDatastore.isEmpty()

    @staticmethod
    def getLiveData():
        livePlayerData = OfficialFPLApi.getLiveData(LiveFPLMatchDataCollector.gw)
        liveFixtureData = OfficialFPLApi.getFixtures(LiveFPLMatchDataCollector.gw)
        return livePlayerData, liveFixtureData

    @staticmethod
    def saveLiveData(livePlayerData, liveFixtureData):
        fixtureDict = {}
        for a in liveFixtureData:
            fixtureDict[a['id']] = LiveFPLMatchDataCollector.getFixtureInfo(a)
        LiveFPLMatchDataCollector.liveDatastore.setFixtureData(fixtureDict)
        playerDict = {}
        for playerData in livePlayerData['elements']:
            playerDict[playerData['id']] = LiveFPLMatchDataCollector.getPlayerInfo(playerData)
        LiveFPLMatchDataCollector.liveDatastore.setPlayerData(playerDict)

    @staticmethod
    def getTeamInfo(id):
        teamData = LiveFPLMatchDataCollector.staticTeamData[id]
        return {
            'name' : teamData['name'],
            'shortName' : teamData['short_name'],
            'code' : teamData['code']
        }

    @staticmethod
    def getStaticPlayerInfo(id):
        playerData = LiveFPLMatchDataCollector.staticPlayerData[id]
        return playerData

    @staticmethod
    def getWebNameForPlayerId(id):
        d = LiveFPLMatchDataCollector.getStaticPlayerInfo(id)
        return d['web_name']

    @staticmethod
    def getPhotoForPlayerId(id):
        d = LiveFPLMatchDataCollector.getStaticPlayerInfo(id)
        return d['photo']

    @staticmethod
    def getInfoFromStatsDict(data, index=0, sideDesignator='h'):
        if data['stats']:
            return [{'value' : x['value'],
                     'playerId' : x['element'],
                     'webName' : LiveFPLMatchDataCollector.getWebNameForPlayerId(x['element'])
                     }
                    for x in data['stats'][index][sideDesignator]]
        else:
            return []

    @staticmethod
    def collectPlayerTotalExplanation(data):
        info = []
        for item in data['explain']:
            d = {}
            d['fixtureId'] = item['fixture']
            d['fixtureTitle'] = LiveFPLMatchDataCollector.getFixtureTitle(item['fixture'])
            d['info'] = [
                {
                    'activity': x['identifier'],
                    'value': x['value'],
                    'points': x['points'],
                } for x in item['stats']
            ]
            info.append(d)
        return info

    @staticmethod
    def getFixtureTitle(id):
        f = LiveFPLMatchDataCollector.liveDatastore.getFixtureLiveData(id)
        return {
            'name': '{} v {}'.format(f['teamHome']['name'], f['teamAway']['name']),
            'shortName': '{} v {}'.format(f['teamHome']['shortName'], f['teamAway']['shortName'])
        }

    @staticmethod
    def getPlayerInfo(data):
        detail = {}
        detail['id'] = data['id']
        detail['totalPoints'] = data['stats']['total_points']
        detail['goals'] = data['stats']['goals_scored']
        detail['assists'] = data['stats']['assists']
        detail['cleanSheets'] = data['stats']['clean_sheets']
        detail['goalsConceded'] = data['stats']['goals_conceded']
        detail['ownGoals'] = data['stats']['own_goals']
        detail['penaltiesSaved'] = data['stats']['penalties_saved']
        detail['penaltiesMissed'] = data['stats']['penalties_missed']
        detail['yellowCards'] = data['stats']['yellow_cards']
        detail['redCards'] = data['stats']['red_cards']
        detail['saves'] = data['stats']['saves']
        detail['bonus'] = data['stats']['bonus']
        detail['provisionalBonus'] = data['stats'].get('provisional_bonus', 0)
        detail['bps'] = data['stats']['bps']
        detail['minutes'] = data['stats']['minutes']
        detail['explain'] = LiveFPLMatchDataCollector.collectPlayerTotalExplanation(data)
        detail['position'] = LiveFPLMatchDataCollector.getPlayerPosition(data['id'])
        return detail

    @staticmethod
    def getPlayerPosition(playerId):
        staticData = LiveFPLMatchDataCollector.staticPlayerData[playerId]
        elementType = staticData['element_type']
        return PlayerPosition.getPlayerPosition(elementType)

    @staticmethod
    def getFixtureInfo(data):
        detail = {}
        detail['gw'] = data['event']
        detail['finished'] = data['finished']
        detail['fixtureId'] = data['id']
        detail['kickoffTimeUTC'] = data['kickoff_time']
        detail['teamAwayId'] = data['team_a']
        detail['teamHomeId'] = data['team_h']
        detail['teamAway'] = LiveFPLMatchDataCollector.getTeamInfo(data['team_a'])
        detail['teamHome'] = LiveFPLMatchDataCollector.getTeamInfo(data['team_h'])
        detail['teamAwayScore'] = data['team_a_score']
        detail['teamHomeScore'] = data['team_h_score']
        detail['goalsScored'] = {
            'away': LiveFPLMatchDataCollector.getInfoFromStatsDict(data, index=0, sideDesignator='a'),
            'home': LiveFPLMatchDataCollector.getInfoFromStatsDict(data, index=0, sideDesignator='h'),
        }
        detail['assists'] = {
            'away': LiveFPLMatchDataCollector.getInfoFromStatsDict(data, index=1, sideDesignator='a'),
            'home': LiveFPLMatchDataCollector.getInfoFromStatsDict(data, index=1, sideDesignator='h'),
        }
        detail['ownGoals'] = {
            'away': LiveFPLMatchDataCollector.getInfoFromStatsDict(data, index=2, sideDesignator='a'),
            'home': LiveFPLMatchDataCollector.getInfoFromStatsDict(data, index=2, sideDesignator='h'),
        }
        detail['penaltiesSaved'] = {
            'away': LiveFPLMatchDataCollector.getInfoFromStatsDict(data, index=3, sideDesignator='a'),
            'home': LiveFPLMatchDataCollector.getInfoFromStatsDict(data, index=3, sideDesignator='h'),
        }
        detail['penaltiesMissed'] = {
            'away': LiveFPLMatchDataCollector.getInfoFromStatsDict(data, index=4, sideDesignator='a'),
            'home': LiveFPLMatchDataCollector.getInfoFromStatsDict(data, index=4, sideDesignator='h'),
        }
        detail['yellowCards'] = {
            'away': LiveFPLMatchDataCollector.getInfoFromStatsDict(data, index=5, sideDesignator='a'),
            'home': LiveFPLMatchDataCollector.getInfoFromStatsDict(data, index=5, sideDesignator='h'),
        }
        detail['redCards'] = {
            'away': LiveFPLMatchDataCollector.getInfoFromStatsDict(data, index=6, sideDesignator='a'),
            'home': LiveFPLMatchDataCollector.getInfoFromStatsDict(data, index=6, sideDesignator='h'),
        }
        detail['saves'] = {
            'away': LiveFPLMatchDataCollector.getInfoFromStatsDict(data, index=7, sideDesignator='a'),
            'home': LiveFPLMatchDataCollector.getInfoFromStatsDict(data, index=7, sideDesignator='h'),
        }
        detail['bonus'] = {
            'away': LiveFPLMatchDataCollector.getInfoFromStatsDict(data, index=8, sideDesignator='a'),
            'home': LiveFPLMatchDataCollector.getInfoFromStatsDict(data, index=8, sideDesignator='h'),
        }
        detail['bps'] = {
            'away': LiveFPLMatchDataCollector.getInfoFromStatsDict(data, index=9, sideDesignator='a'),
            'home': LiveFPLMatchDataCollector.getInfoFromStatsDict(data, index=9, sideDesignator='h'),
        }
        return detail
        
