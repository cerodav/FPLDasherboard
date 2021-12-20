from collections import defaultdict
from datetime import datetime, timedelta

import pandas as pd
from threading import Thread
from fpldb.database.model.enums import MatchStatus
from fpldb.database.model.core import SquadStatus, ChipType
from fpldb.dashboardService.dataCollectors.liveFPLAverageDataStore import LiveFPLAverageDataStore
from fpldb.dashboardService.analytics.basicAnalytics import BasicAnalytics
from fpldb.utils.coreUtils import CoreUtils
from fpldb.utils.typesUtil import PlayerPosition
from fpldb.dashboardService.handlers.baseHandler import BaseHandler
from fpldb.logger.logger import logger
from fpldb.utils.pickleUtil import PickleUtil
from fpldb.dashboardService.classicLeagueDatastore import ClassicLeagueDatastore
from fpldb.dashboardService.dataCollectors.liveEPLDataCollector import LiveFPLMatchDataCollector, LiveFPLDatastore, LiveFPLAverageCollector


class ClassicLeagueLiveHandler(BaseHandler):

    liveFPLAverageDataStore = LiveFPLAverageDataStore()
    liveFPLDatastore = LiveFPLDatastore()
    Thread(target=LiveFPLMatchDataCollector.run, args=(liveFPLDatastore, CoreUtils.getGameweek())).start()
    Thread(target=LiveFPLAverageCollector.run, args=(liveFPLAverageDataStore, )).start()

    async def get(self):
        logger.info('[INCOMING] Request at {} '.format(self.request.path))
        parentPath = self.pathInfo[1].upper()
        try :
            if parentPath == 'CLASSICLEAGUE':
                leaugueId = self.pathInfo[2]
                response = self.calculateLiveStandingsForLeague(leaugueId)
            elif parentPath == 'LATESTSTATISTICS':
                response = self.getLatestStatisticsData()
            elif parentPath == 'GAMEWEEKDETAILS':
                response = self.getGameweekDetails()
            elif parentPath == 'LEAGUESTATISTICS':
                leaugueId = self.pathInfo[2]
                response = self.getLeagueStatisticsData(leaugueId)
            self.send_response(response)
            logger.info('[OUTGOING] Response for {} '.format(self.request.path))
        except Exception as e:
            logger.exception('[EXCEPTION] While trying to respond to query {}'.format(self.request.path))

    def getPlayerInfo(self, playerId):
        playerMetadata = self.staticPlayerData[playerId]
        returnObj =  {
            'id': playerId,
            'name' : playerMetadata['web_name'],
            'firstName': playerMetadata['first_name'],
            'teamCode' : playerMetadata['team_code'],
            'teamName' : self.staticTeamData[playerMetadata['team']]['name'],
        }
        return returnObj

    def getGameweekDetails(self):
        response = {}
        response['fixtures'] = self.collectFixtureInformationForDashboard()
        response['gameweek'] = self.getLatestStatisticsData()
        # response['dreamTeam'] = self.collectDreamTeamInformationForDashboard()
        return response

    def collectFixtureInformationForDashboard(self):
        data = self.liveFPLDatastore.getFixturesData()
        if data:
            return list(data.values())
        return None

    def getLeagueStatisticsData(self, leagueId):
        cacheData = PickleUtil.getDataFromPickle(CoreUtils.getStatsPickleFileName(CoreUtils.getGameweek(), leagueId))
        if cacheData:
            labelFixes = ['highestGWPoints', 'lowestGWPoints', 'totalPointsTimeseries', 'lowestBank', 'highestBank',
                          'lowestEventTransfers', 'highestEventTransfers', 'lowestEventTransfersCost',
                          'highestEventTransfersCost', 'lowestPointsOnBench', 'highestPointsOnBench', 'lowestNetValue',
                          'highestNetValue', 'mogwCounts', 'highestWildcardPoints', 'highestFreehitPoints',
                          'highestBboostPoints', 'highest3xcPoints']
            labelMap = {x.upper():x for x in labelFixes}
            response = {}
            for key in cacheData:
                if key.upper() in labelMap:
                    response[labelMap[key.upper()]] = cacheData[key]
            return response
        return None

    def getLatestStatisticsData(self):
        response = {}

        response['top10KAvg'] = self.liveFPLAverageDataStore.getTop10KAvg()
        response['top10KHitsAvg'] = self.liveFPLAverageDataStore.getTop10KHitsAvg()
        response['top10KHitsInclAvg'] = self.liveFPLAverageDataStore.getTop10KHitsInclAvg()
        response['overallAvg'] = self.liveFPLAverageDataStore.getOverallAvg()
        response['overallHitsAvg'] = self.liveFPLAverageDataStore.getOverallHitsAvg()
        response['overallHitsInclAvg'] = self.liveFPLAverageDataStore.getOverallHitsInclAvg()
        response['gameweekNumber'] = self.liveFPLAverageDataStore.getGameweek()

        response['bestAttacker'] = self.liveFPLDatastore.getBIEPData()[PlayerPosition.Attacker]
        response['bestMidfielder'] = self.liveFPLDatastore.getBIEPData()[PlayerPosition.Midfielder]
        response['bestDefender'] = self.liveFPLDatastore.getBIEPData()[PlayerPosition.Defender]
        response['bestGoalkeeper'] = self.liveFPLDatastore.getBIEPData()[PlayerPosition.Goalkeeper]
        response['bestAttacker'].update(self.getPlayerInfo(response['bestAttacker']['id']))
        response['bestMidfielder'].update(self.getPlayerInfo(response['bestMidfielder']['id']))
        response['bestDefender'].update(self.getPlayerInfo(response['bestDefender']['id']))
        response['bestGoalkeeper'].update(self.getPlayerInfo(response['bestGoalkeeper']['id']))

        return response

    def getCodeForChipUser(self, chipType):
        chipMap = {
            ChipType.Wildcard : 'WC',
            ChipType.TripleCap : 'TC',
            ChipType.Benchboost : 'BB',
            ChipType.Freehit : 'FH'
        }
        if chipType is not None:
            return chipMap[chipType]
        else:
            return '-'

    def calculatePLayersPlayed(self, teamData):
        activeChip = teamData['info']['activeChip']
        isBenchboost = activeChip == ChipType.Benchboost
        playedPlayers = 0
        playablePlayers = 11 if not isBenchboost else 15
        for playerItem in teamData['live']['squad']:
            if 'minutes' in playerItem:
                if playerItem['status'] == SquadStatus.Playing and playerItem['minutes'] > 0:
                    playedPlayers += 1
                if playerItem['status'] == SquadStatus.Bench and isBenchboost and playerItem['minutes'] > 0:
                    playedPlayers += 1
        return '{}/{}'.format(playedPlayers, playablePlayers)

    def updateDashboardDisplayTableFields(self, rank, team):

        captainName = None
        vicecaptainName = None
        for player in team['squad']:
            if player['isCaptain']:
                captainName = player['name']
            else:
                if player['isVCaptain']:
                    vicecaptainName = player['name']

        team['dashboardTable'] = {}
        item = team['dashboardTable']

        item['captaincy'] = {}
        item['captaincy']['upper'] = ''
        item['captaincy']['lower'] = captainName

        item['vicecaptaincy'] = {}
        item['vicecaptaincy']['upper'] = ''
        item['vicecaptaincy']['lower'] = vicecaptainName

        item['ranking'] = {}
        item['ranking']['upper'] = team['info']['lastRank'] - rank
        item['ranking']['lower'] = rank

        item['hits'] = {}
        item['hits']['upper'] = ''
        item['hits']['lower'] = team['info']['gwTransferCost'] * (-1)

        item['chip'] = {}
        item['chip']['upper'] = ''
        item['chip']['lower'] = self.getCodeForChipUser(team['info']['activeChip'])

        # playedCount = 0
        # for player in team['squad']:
        #     if player['minutes'] > 0:
        #         playedCount += 1
        item['playersPlayed'] = {}
        item['playersPlayed']['upper'] = ''
        item['playersPlayed']['lower'] = self.calculatePLayersPlayed(team)

        item['gwPoints'] = {}
        item['gwPoints']['upper'] = ''
        item['gwPoints']['lower'] = team['live']['currentGWTotalWithProvisionalBonus']

        item['totalPoints'] = {}
        item['totalPoints']['upper'] = ''
        item['totalPoints']['lower'] = team['live']['currentTotalWithProvisionalBonus']

        pName = team['info']['userName'].split()
        item['manager'] = {}
        item['manager']['upper'] = ' '.join(pName[1:])
        item['manager']['lower'] = pName[0]

        tName = team['info']['name']
        item['teamName'] = {}
        item['teamName']['upper'] = ''
        item['teamName']['lower'] = tName

    def getStaleClassicLeagueStandings(self, leagueId):

        cacheData = ClassicLeagueDatastore.getLeague(leagueId)
        if not cacheData:
            cacheData = PickleUtil.getDataFromPickle(CoreUtils.getPickleFileName(self.liveFPLAverageDataStore.getGameweek(), leagueId))
            if not cacheData:
                basicInfo = CoreUtils.getStaleClassicLeagueStandings(leagueId)
                ClassicLeagueDatastore.addLeague(leagueId, basicInfo)
                PickleUtil.saveToPickle(basicInfo, CoreUtils.getPickleFileName(self.liveFPLAverageDataStore.getGameweek(), leagueId))
            else:
                basicInfo = cacheData
                ClassicLeagueDatastore.addLeague(leagueId, basicInfo)
        else:
            basicInfo = cacheData['data']
        return basicInfo

    def calculateLiveStandingsForLeague(self, leagueId):
        if not leagueId:
            return {}
        staleStandings = self.getStaleClassicLeagueStandings(leagueId)
        if staleStandings is None:
            logger.info(' ! No data available for LeagueId#{}'.format(leagueId))
            return {}
        liveStandings = self.updateStaleClassicLeagueStandings(staleStandings)
        BasicAnalytics.runSuite(liveStandings)
        teams = liveStandings['members']
        for rank, team in enumerate(teams):
            self.updateDashboardDisplayTableFields(rank+1, team)
        logger.info(' * Finished serving request for dashboard live league')
        return liveStandings

    def updateStaleClassicLeagueStandings(self, data):
        for member in data['members']:
            self.getLiveUpdateForTeam(member)
        return data

    def getMultiplier(self, chipType, playingStatus, isCaptain):
        if chipType == ChipType.TripleCap:
            if isCaptain:
                return 3
            elif playingStatus == SquadStatus.Playing:
                return 1
            else:
                return 0
        elif chipType == ChipType.Benchboost:
            if isCaptain:
                return 2
            else:
                return 1
        else:
            if isCaptain:
                return 2
            elif playingStatus == SquadStatus.Playing:
                return 1
            else:
                return 0

    def getLiveUpdateForTeam(self, teamInfo):
        liveInfo = {}
        liveInfo['squad'] = teamInfo['squad']
        chipType = teamInfo['info']['activeChip']
        currentTotalWithProvisionalBonus = 0
        currentTotalWithoutProvisionalBonus = 0
        for playerInfo in liveInfo['squad']:
            liveData = ClassicLeagueLiveHandler.liveFPLDatastore.getPlayerLiveData(int(playerInfo['id']))
            playerInfo.update(liveData)
            currentTotalWithProvisionalBonus += self.getMultiplier(chipType, playerInfo['status'], playerInfo['isCaptain']) * liveData['totalPoints']
            currentTotalWithoutProvisionalBonus += self.getMultiplier(chipType, playerInfo['status'], playerInfo['isCaptain']) * (liveData['totalPoints'] - liveData['provisionalBonus'])
        liveInfo['currentGWTotalWithProvisionalBonus'] = currentTotalWithProvisionalBonus
        liveInfo['currentGWTotalWithoutProvisionalBonus'] = currentTotalWithoutProvisionalBonus
        teamInfo['live'] = liveInfo






