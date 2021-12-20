from collections import defaultdict
from datetime import datetime

import pandas as pd

from fpldb.dashboardService.dataCollectors.liveFPLAverageDataStore import LiveFPLAverageDataStore
from fpldb.api.officialFPL.officialFPLApi import OfficialFPLApi
from fpldb.database.utils.coreDBUtils import CoreDBUtils
from fpldb.logger.logger import logger
from fpldb.database.session.sessionFactory import DefaultSessionFactory
from fpldb.database.model.core import *
from fpldb.utils.formattingUtil import FormattingUtil


class CoreUtils:

    staticTeamData = OfficialFPLApi.getStaticTeamData()
    session = DefaultSessionFactory().getSession()
    gameweek = None

    @staticmethod
    def getGameweek():
        if CoreUtils.gameweek is not None:
            return CoreUtils.gameweek

        eventStatus = OfficialFPLApi.getEventStatus()
        gwNum = eventStatus['status'][0]['event']
        CoreUtils.gameweek = gwNum
        return CoreUtils.gameweek

    async def get(self):
        logger.info('[INCOMING] Request at {}'.format(self.request.path))
        parentPath = self.pathInfo[0].upper()
        try :
            if parentPath == 'CLASSICLEAGUE':
                response = self.calculateLiveStandingsForLeague()
            elif parentPath == 'LATESTSTATISTICS':
                response = self.getLatestEventData()
            self.send_response(response)
        except Exception as e:
            logger.exception('[EXCEPTION] While trying to respond to query {}'.format(self.request.path))

    @staticmethod
    def getPlayerInfo(playerId):
        playerMetadata = OfficialFPLApi.getStaticPlayerData()[playerId]
        returnObj = {
            'id': playerId,
            'secondName' : playerMetadata['second_name'],
            'firstName': playerMetadata['first_name'],
            'webName': playerMetadata['web_name'],
            'teamCode' : playerMetadata['team'],
            'teamName' : CoreUtils.staticTeamData[playerMetadata['team']]['name'],
        }
        return returnObj

    @staticmethod
    def getTeamInfo(teamId, gwId = None, forceOnboard = False):
        if gwId is None:
            gwId = CoreUtils.getGameweek()

        teamRawData = CoreDBUtils.getTeamDetails(teamId, gw=gwId), CoreDBUtils.getTeamMembershipDetails(teamId, gwId)
        if forceOnboard or not all(teamRawData):
            logger.info('No data or incomplete data for teamId#{} in DB'.format(teamId))
            logger.info('Onboarding data for teamId#{}'.format(teamId))
            CoreDBUtils.wipeOutTeamMembershipData(teamId, commit=True)
            CoreDBUtils.wipeOutTeamMetadata(teamId, commit=True)
            teamRawData = CoreUtils.onboardTeam(teamId, gwId)
        return teamRawData

    @staticmethod
    def wipeOutTeam(teamId):
        CoreDBUtils.wipeOutTeamMembershipData(teamId)
        CoreDBUtils.wipeOutTeamMetadata(teamId)
        logger.info('[WIPEOUT] Deleting data for team id # {}'.format(teamId))

    @staticmethod
    def onboardTeam(teamId, gwId = None, commit=False):

        data = {}
        bench = []
        playing = []
        captain = None
        viceCaptain = None

        teamMetaData = OfficialFPLApi.getTeamDetails(teamId)
        teamRawData = OfficialFPLApi.getGWPlayerPick(teamId, gwId)

        for player in teamRawData['picks']:
            processedPlayer = CoreUtils.getPlayerInfo(player['element'])
            processedPlayer['multiplier'] = player['multiplier']
            if player['multiplier'] == 0:
                bench.append(processedPlayer)
            else:
                playing.append(processedPlayer)
            if player['multiplier'] >= 2:
                captain = processedPlayer['id']
            if player['is_vice_captain']:
                viceCaptain = processedPlayer['id']

        data['squad'] = {'playing': playing, 'bench': bench, 'captain': captain, 'viceCaptain': viceCaptain}

        interestedEventFields = ['points', 'total_points', 'event_transfers', 'event_transfers_cost', 'points_on_bench']
        renamedEventFields = ['points', 'totalPoints', 'eventTransfers', 'eventTransfersCost',
                              'pointsOnBench']

        chipMap = {
            '3XC':ChipType.TripleCap,
            'BBOOST':ChipType.Benchboost,
            'WILDCARD':ChipType.Wildcard,
            'FREEHIT':ChipType.Freehit
        }

        data['eventData'] = {}
        for field, renamedField in zip(interestedEventFields, renamedEventFields):
            data['eventData'][renamedField] = teamRawData['entry_history'][field]
        data['eventData']['activeChip'] = teamRawData['active_chip']
        data['eventData']['automaticSubs'] = teamRawData['automatic_subs']

        t = Team()
        t.teamId = teamMetaData['id']
        t.name = teamMetaData['name']
        t.userName = '{} {}'.format(teamMetaData['player_first_name'], teamMetaData['player_last_name'])
        t.overallRank = teamMetaData['summary_overall_rank']
        t.overallPoints = teamMetaData['summary_overall_points']
        t.gameweek = teamMetaData['current_event']
        t.bankValue = teamMetaData['last_deadline_bank']/10
        t.squadValue = teamMetaData['last_deadline_value']/10
        t.totalTransfers = teamMetaData['last_deadline_total_transfers']
        t.gameweekPoints = data['eventData']['points']
        t.gameweekTransfers = data['eventData']['eventTransfers']
        t.gameweekTransferCost = data['eventData']['eventTransfersCost']
        t.activeChip = chipMap.get(data['eventData']['activeChip'].upper(), None) if data['eventData']['activeChip'] else None
        CoreUtils.session.add(t)

        squad = []
        for p in data['squad']['playing']:
            tm = TeamMembership()
            tm.teamId = teamId
            tm.playerId = p['id']
            tm.gameweek = gwId
            tm.playingStatus = SquadStatus.Playing
            tm.captain = False
            tm.vicecaptain = False
            if p['id'] == data['squad']['viceCaptain']:
                tm.vicecaptain = True
            if p['id'] == data['squad']['captain']:
                tm.captain = True
            CoreUtils.session.add(tm)
            squad.append(tm)

        for p in data['squad']['bench']:
            tm = TeamMembership()
            tm.teamId = teamId
            tm.playerId = p['id']
            tm.gameweek = CoreUtils.getGameweek()
            tm.playingStatus = SquadStatus.Bench
            tm.captain = False
            tm.vicecaptain = False
            if p['id'] == data['squad']['viceCaptain']:
                tm.vicecaptain = True
            if p['id'] == data['squad']['captain']:
                tm.captain = True
            CoreUtils.session.add(tm)
            squad.append(tm)

        if commit:
            CoreUtils.session.commit()
        return t, squad

    def getLatestEventData(self):
        rawData = self.OfficialFPLApi.getLatestEventData()
        response = {}
        for key in rawData:
            if key.endswith('Id'):
                reformattedKey = key.replace('Id', '')
                playerDetail = self.getPlayerInfo(rawData[key])
                response[reformattedKey] = {}
                response[reformattedKey]['upper'] = playerDetail['firstName']
                response[reformattedKey]['lower'] = playerDetail['name']
                continue
            if key == 'avgScore':
                response['avgScore'] = {}
                response['avgScore']['upper'] = str(rawData['deltaAvgScore'])
                response['avgScore']['lower'] = str(rawData['avgScore'])
                continue
            if key == 'highestScore':
                response['highestScore'] = {}
                response['highestScore']['upper'] = str(rawData['deltaHighestScore'])
                response['highestScore']['lower'] = str(rawData['highestScore'])
                continue
            if key == 'highestScoringPlayerInfo':
                response['highestScoringPlayerScore'] = {}
                response['highestScoringPlayerScore']['upper'] = str(rawData['deltaHighestScoringPlayerScore'])
                response['highestScoringPlayerScore']['lower'] = str(rawData['highestScoringPlayerInfo']['points'])
                continue
            if key in ['deltaAvgScore', 'deltaHighestScore', 'deltaHighestScoringPlayerScore']:
                continue
            response[key] = {}
            response[key]['upper'] = None
            response[key]['lower'] = rawData[key]

        avgData = self._liveFPLAverageDataStore.getAvgData()

        response['top10KAvg'] = avgData['top10KAvg']
        response['top10KHitsAvg'] = avgData['top10KHitsAvg']
        response['top10KHitsInclAvg'] = avgData['top10KHitsInclAvg']

        response['overallAvg'] = avgData['overallAvg']
        response['overallHitsAvg'] = avgData['overallHitsAvg']
        response['overallHitsInclAvg'] = avgData['overallHitsInclAvg']

        response['gameweekNumber'] = avgData['gameweekNumber']

        # logger.info('# Response - ', response)
        return response

    def getCodeForChipUser(self, chipName):
        chipMap = {
            'WILDCARD':'WC',
            '3XC':'TC',
            'BBOOST':'BB',
            'FREEHIT':'FH'
        }
        if chipName is not None:
            if chipName.upper() in chipMap:
                return chipMap[chipName.upper()]
            else:
                return None
        else:
            return '-'

    def getDashboardDisplayTableFields(self, item):
        # Formatted for dashboard
        captainName = None
        vicecaptainName = None
        for entry in item['squad']['captain']:
            if entry['multiplier'] >= 2:
                captainName = entry['name']
            else:
                vicecaptainName = entry['name']

        item['captaincy'] = {}
        item['captaincy']['upper'] = ''
        item['captaincy']['lower'] = captainName

        item['vicecaptaincy'] = {}
        item['vicecaptaincy']['upper'] = ''
        item['vicecaptaincy']['lower'] = vicecaptainName

        item['ranking'] = {}
        item['ranking']['upper'] = item['lastRank'] - item['liveRank']
        item['ranking']['lower'] = item['liveRank']

        item['hits'] = {}
        item['hits']['upper'] = ''
        item['hits']['lower'] = item['eventData']['eventTransfersCost'] * (-1)

        item['chip'] = {}
        item['chip']['upper'] = ''
        item['chip']['lower'] = self.getCodeForChipUser(item['eventData']['activeChip'])

        playedCount = 0
        for player in item['squad']['playing']:
            if 'minsPlayed' in player:
                playedCount += 1
        item['playersPlayed'] = {}
        item['playersPlayed']['upper'] = ''
        item['playersPlayed']['lower'] = str(playedCount) + '/11'

        item['gwPoints'] = {}
        item['gwPoints']['upper'] = ''
        # item['gwPoints']['lower'] = item['eventData']['points']
        item['gwPoints']['lower'] = item['livePlayingTeamScore']

        # team['livePlayingTeamScore'] = playingTeamLiveScore
        # team['liveTotalTeamScore'] = team['total'] - team['eventTotal'] + playingTeamLiveScore

        item['totalPoints'] = {}
        item['totalPoints']['upper'] = ''
        # item['totalPoints']['lower'] = item['eventData']['totalPoints']
        item['totalPoints']['lower'] = item['liveTotalTeamScore']

        pName = item['playerName'].split()
        item['manager'] = {}
        item['manager']['upper'] = ' '.join(pName[1:])
        item['manager']['lower'] = pName[0]

    @staticmethod
    def getPickleFileName(gw, leagueId):
        return 'GW{}_LID#{}'.format(gw, leagueId)

    @staticmethod
    def getStatsPickleFileName(gw, leagueId):
        return 'GW{}_LID#{}_STATS'.format(gw, leagueId)

    def getStaleClassicLeagueStandings(leagueId):
        leagueDetails = None
        leagueMembershipDetails = None
        try:
            leagueDetails = CoreDBUtils.getLeagueDetails(leagueId)
            leagueMembershipDetails = CoreDBUtils.getLeagueMembershipDetails(leagueId)
        except Exception as e:
            logger.exception(' ! Error on collecting league {} data from fplDB'.format(leagueId))
            raise Exception(' ! Failure in collecting league {} details'.format(leagueId))

        if leagueDetails is None and leagueMembershipDetails is None:
            return None

        league = {}
        info = {
            'name' : leagueDetails.name
        }
        league['info'] = info
        league['members'] = []
        for member in leagueMembershipDetails:
            team = {}
            info = {}
            info['gwPoints'] = member.gameweekPoints
            info['lastRank'] = member.lastRank
            info['currentRank'] = member.leagueRank
            info['rankSort'] = member.rankSort
            info['id'] = member.teamId
            info['totalPoints'] = member.totalPoints
            info['activeChip'] = member.team.activeChip
            info['bankValue'] = member.team.bankValue
            info['squadValue'] = member.team.squadValue
            info['bbPlayed'] = member.team.bbPlayed
            info['fhPlayed'] = member.team.fhPlayed
            info['tcPlayed'] = member.team.tcPlayed
            info['gwTransferCost'] = member.team.gameweekTransferCost
            info['gwTransfers'] = member.team.gameweekTransfers
            info['name'] = member.team.name
            info['overallRank'] = member.team.overallRank
            info['totalTransfers'] = member.team.totalTransfers
            info['userName'] = member.team.userName
            info['wc1Played'] = member.team.wc1Played
            info['wc2Played'] = member.team.wc2Played
            team['info'] = info
            squad = []
            for player in member.team.squad:
                det = {}
                det['isCaptain'] = player.captain
                det['isVCaptain'] = player.vicecaptain
                det['id'] = player.playerId
                det['status'] = player.playingStatus
                data = CoreDBUtils.getPlayer(player.playerId)
                det['name'] = data.webName
                det['code'] = data.code
                det['photo'] = data.photo
                det['chanceOfPlaying'] = data.chanceOfPlaying
                squad.append(det)
            team['squad'] = squad
            league['members'].append(team)
        return league

    @staticmethod
    def getGWTeamInfo(self, teamId, gwId):
        data = {}
        playing = []
        bench = []
        captain = []
        captainName = None
        vicecaptainName = None

        teamRawData = CoreDBUtils.OfficialFPLApi.getGWPlayerPick(teamId, gwId)

        for player in teamRawData['picks']:
            processedPlayer = self.getPlayerInfo(player['element'])
            processedPlayer['multiplier'] = player['multiplier']
            if player['is_vice_captain'] or player['multiplier'] >= 2:
                if player['is_vice_captain']:
                    vicecaptainName = processedPlayer['name']
                if player['multiplier'] >= 2:
                    captainName = processedPlayer['name']
                captain.append(processedPlayer)
                continue
            if player['multiplier'] == 0:
                bench.append(processedPlayer)
                continue
            playing.append(processedPlayer)

        data['squad'] = {'playing': playing, 'bench': bench, 'captain': captain}

        interestedEventFields = ['points', 'total_points', 'event_transfers', 'event_transfers_cost', 'points_on_bench']
        renamedEventFields = ['points', 'totalPoints', 'eventTransfers', 'eventTransfersCost',
                              'pointsOnBench']
        data['eventData'] = {}
        for field, renamedField in zip(interestedEventFields, renamedEventFields):
            data['eventData'][renamedField] = teamRawData['entry_history'][field]
        data['eventData']['activeChip'] = teamRawData['active_chip']
        data['eventData']['automaticSubs'] = teamRawData['automatic_subs']

        return data

    @staticmethod
    def onboardLeague(leagueId):

        currentGW = CoreUtils.getGameweek()

        # Limiting to only grabbing data for classic leagues
        basicInfo = OfficialFPLApi.getClassicLeagueStandings(leagueId=leagueId)
        if basicInfo['league']['league_type'] not in ['x', 's']:
            return

        # Add/Update entry at League table
        newLeague = False
        l = CoreDBUtils.getLeagueDetails(leagueId)
        if not l:
            l = League()
            newLeague = True
            l.leagueId = leagueId
            l.type = basicInfo['league']['league_type']
        l.name = basicInfo['league']['name']
        l.createdTime = FormattingUtil.getDatetimeFromDatetimeString(basicInfo['league']['created']).date()
        if newLeague:
            CoreUtils.session.add(l)

        interestedFields = ['player_name', 'rank', 'last_rank', 'rank_sort', 'total', 'entry',
                            'entry_name']
        renamedFields = ['playerName', 'rank', 'lastRank', 'rankSort', 'total', 'id',
                         'teamName']
        CoreDBUtils.wipeOutLeagueMembershipData(leagueId)
        for entry in basicInfo['standings']['results']:
            item = {}
            for field, renamedField in zip(interestedFields, renamedFields):
                item[renamedField] = entry[field]

            teamInfo = CoreUtils.getTeamInfo(item['id'], gwId=currentGW, forceOnboard=True)
            teamMetadata, teamPlayers = teamInfo

            lm = LeagueMembership()
            lm.leagueId = leagueId
            lm.teamId = item['id']
            lm.gameweek = currentGW
            lm.gameweekPoints = teamMetadata.gameweekPoints
            lm.totalPoints = item['total']
            lm.leagueRank = item['rank']
            lm.lastRank = item['lastRank']
            lm.rankSort = item['rankSort']
            CoreUtils.session.add(lm)

        CoreUtils.session.commit()

    def getLastBonusPointUpdateDate(self, eventStatus):
        bonusDate = datetime(2020,1,1)
        for item in eventStatus['status']:
            if item['bonus_added']:
                bonusDate = max(bonusDate, pd.to_datetime(item['date']))
        return bonusDate

    def updateDifferentialsData(self, data):

        playerMap = defaultdict(lambda : 0)
        teamCount = 0
        for team in data['standings']:
            teamCount += 1
            playingSquad = team['squad']['playing']
            for player in playingSquad:
                playerMap[player['id']] += 1

        for team in data['standings']:
            playingSquad = team['squad']['playing']
            team['squad']['differential'] = []
            for player in playingSquad:
                if (playerMap[player['id']]/teamCount)*100 < 20:
                    team['squad']['differential'].append(player)

        return data

    def calculateLiveStandingsForLeague(self):

        if 1 not in self.pathInfo:
            return None

        eventStatus = self.OfficialFPLApi.getEventStatus()
        currentStandings = self.getClassicLeagueStandings()
        currentGW = currentStandings['gameweekNumber']
        # response = currentStandings
        # if eventStatus['leagues'].upper() != 'UPDATED':
        bonusDate = self.getLastBonusPointUpdateDate(eventStatus)
        liveActionPlayerData = self.generateInformationFromLiveData(currentGW)
        response = self.getUpdatedLeagueStandings(currentStandings, liveActionPlayerData, bonusDate)
        response = self.updateDifferentialsData(response)
        for item in response['standings']:
            self.getDashboardDisplayTableFields(item)
        # else:
        #     for idx, team in enumerate(response['standings']):
        #         team['liveRank'] = idx
        logger.info(' * Finished serving request for dashboard live league')
        return response

    def filterOutUnplayedPlayers(self, liveDataMap):

        playedElements = {}
        for idx, element in enumerate(liveDataMap):
            elementId = element['id']
            if element['stats']['minutes'] == 0:
                continue

            elementInfo = {}
            elementInfo['id'] = elementId
            elementInfo['points'] = element['stats']['total_points']
            elementInfo['bonusPoints'] = element['stats']['bps']
            elementInfo['fixtures'] = []
            elementInfo['minsPlayed'] = element['stats']['minutes']
            for event in element['explain']:
                elementInfo['fixtures'].append(event['fixture'])
            playedElements[elementId] = elementInfo

        return playedElements

    def generateInformationFromLiveData(self, currentGW):

        liveData = self.OfficialFPLApi.getLiveData(currentGW)
        if 'elements' in liveData:
            liveData = liveData['elements']
        else:
            liveData = None
        liveData = self.filterOutUnplayedPlayers(liveData)
        liveData = self.accountForBonusPoints(liveData)
        return liveData

    def isBonusIncludedInTotal(self, fixtureId, fixtures, bonusDate):
        for fixture in fixtures:
            if fixture['id'] == fixtureId:
                if pd.to_datetime(fixture['kickoff_time']).date() <= bonusDate.date():
                    return True
        return False

    def updatePointBasedOnLiveScores(self, team, liveActionData, bonusDate, gwNum, fixtures, addBonus):
        teamPicks = team['squad']
        playingTeamLiveScore = 0
        benchTeamLiveScore = 0
        for mode in teamPicks:
            for player in teamPicks[mode]:
                multiplier = player['multiplier'] if mode != 'bench' else 1
                player['liveScore'] = 0
                if player['id'] in liveActionData:
                    player['minsPlayed'] = liveActionData[player['id']]['minsPlayed']
                    bonusIncludedInTotal = self.isBonusIncludedInTotal(liveActionData[player['id']]['fixtures'][0],
                                                                       fixtures, bonusDate)
                    player['liveScore'] += multiplier * liveActionData[player['id']]['points']
                    if addBonus and not bonusIncludedInTotal:
                        player['liveScore'] += multiplier * liveActionData[player['id']]['bonus']
                if mode.upper() == 'PLAYING':
                    playingTeamLiveScore += player['liveScore']
                if mode.upper() == 'BENCH':
                    benchTeamLiveScore += player['liveScore']

        team['livePlayingTeamScore'] = playingTeamLiveScore
        team['liveTotalTeamScore'] = team['total'] - team['eventTotal'] + playingTeamLiveScore
        team['liveBenchTeamScore'] = benchTeamLiveScore
        return team

    def basedOnLivePlayingTeamScore(self, elem):
        return elem['liveTotalTeamScore']

    def getUpdatedLeagueStandings(self, currentStandings, liveActionMap, bonusDate, addBonus=True):
        fixtures = self.OfficialFPLApi.getFixtures(currentStandings['gameweekNumber'])
        for team in currentStandings['standings']:
            team = self.updatePointBasedOnLiveScores(team, liveActionMap, bonusDate, currentStandings['gameweekNumber'], fixtures, addBonus)
        currentStandings['standings'] = sorted(currentStandings['standings'], key=self.basedOnLivePlayingTeamScore,
                                               reverse=True)
        for idx, team in enumerate(currentStandings['standings']):
            team['liveRank'] = idx + 1
        return currentStandings

    def accountForBonusPoints(self, liveData):

        innerDefaultDict = defaultdict(lambda : [])
        # bpsMapPerFixture = defaultdict(lambda : innerDefaultDict)
        bpsMapPerFixture = {}

        for elementId in liveData:
            element = liveData[elementId]
            element['bonus'] = 0
            for f in element['fixtures']:
                if f in bpsMapPerFixture:
                    if element['bonusPoints'] in bpsMapPerFixture[f]:
                        bpsMapPerFixture[f][element['bonusPoints']].append(element)
                    else:
                        bpsMapPerFixture[f][element['bonusPoints']] = []
                        bpsMapPerFixture[f][element['bonusPoints']].append(element)
                else:
                    bpsMapPerFixture[f] = {}
                    bpsMapPerFixture[f][element['bonusPoints']] = []
                    bpsMapPerFixture[f][element['bonusPoints']].append(element)
                # bpsMapPerFixture[f][element['bonusPoints']].append(element)

        for fixtureId in bpsMapPerFixture:
            maxBps = max(bpsMapPerFixture[fixtureId].keys())
            if len(bpsMapPerFixture[fixtureId][maxBps]) == 2:
                for element in bpsMapPerFixture[fixtureId][maxBps]:
                    liveData[element['id']]['bonus'] += 3
                nextMaxBps = max([x for x in bpsMapPerFixture[fixtureId].keys() if x not in [maxBps]])
                for element in bpsMapPerFixture[fixtureId][nextMaxBps]:
                    liveData[element['id']]['bonus'] += 1
            else:
                liveData[bpsMapPerFixture[fixtureId][maxBps][0]['id']]['bonus'] += 3
                nextMaxBps = max([x for x in bpsMapPerFixture[fixtureId].keys() if x not in [maxBps]])
                if len(bpsMapPerFixture[fixtureId][nextMaxBps]) == 2:
                    for element in bpsMapPerFixture[fixtureId][nextMaxBps]:
                        liveData[element['id']]['bonus'] += 2
                else:
                    liveData[bpsMapPerFixture[fixtureId][nextMaxBps][0]['id']]['bonus'] += 2
                    nextNextMaxBps = max([x for x in bpsMapPerFixture[fixtureId].keys() if x not in [maxBps, nextMaxBps]])
                    if len(bpsMapPerFixture[fixtureId][nextNextMaxBps]) == 2:
                        for element in bpsMapPerFixture[fixtureId][nextNextMaxBps]:
                            liveData[element['id']]['bonus'] += 1
                    else:
                        liveData[bpsMapPerFixture[fixtureId][nextNextMaxBps][0]['id']]['bonus'] += 1

        return liveData




