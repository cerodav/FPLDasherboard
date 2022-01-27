import numpy as np
from sklearn.cluster import AgglomerativeClustering
from collections import defaultdict
from fpldb.database.model.core import SquadStatus
from fpldb.logger.logger import logger
import copy

class BasicAnalytics():

    @staticmethod
    def runSuite(liveStandings):
        BasicAnalytics.updateDifferentialsData(liveStandings)
        BasicAnalytics.updateLiveStandings(liveStandings)

    @staticmethod
    def getStartingPoints(teamInfo):
        return teamInfo['totalPoints'] - teamInfo['gwPoints']

    @staticmethod
    def updateLiveStandings(data):
        teams = data['members']
        for team in teams:
            startingPoint = BasicAnalytics.getStartingPoints(team['info'])
            currentPointsWithPBonus = team['live']['currentGWTotalWithProvisionalBonus']
            currentPointsWithoutPBonus = team['live']['currentGWTotalWithoutProvisionalBonus']
            currentTotalWithProvisionalBonus = startingPoint + currentPointsWithPBonus
            currentTotalWithoutProvisionalBonus = startingPoint + currentPointsWithoutPBonus
            team['live']['currentTotalWithProvisionalBonus'] = currentTotalWithProvisionalBonus
            team['live']['currentTotalWithoutProvisionalBonus'] = currentTotalWithoutProvisionalBonus
        data['members'] = sorted(data['members'], key= lambda x: x['live']['currentTotalWithProvisionalBonus'], reverse= True)

    @staticmethod
    def updateDifferentialsData(data):
        teams = data['members']
        teamScores = np.array([BasicAnalytics.getStartingPoints(x['info']) for x in teams]).reshape(-1, 1)
        cluster = AgglomerativeClustering(n_clusters=7, affinity='euclidean', linkage='single')
        clusterIds = cluster.fit_predict(teamScores)

        #tagging team with cluster
        clusters = {}
        for clusterId, team in zip(clusterIds, teams):
            if clusterId in clusters:
                clusters[clusterId].append(team)
            else:
                clusters[clusterId] = [team]

        for clusterId in clusters:
            clusterMembers = clusters[clusterId]
            numberOfMembers = len(clusterMembers)
            playerMap = defaultdict(lambda: 0)
            for member in clusterMembers:
                squad = member['squad']
                member['live']['differentials'] = []
                for player in squad:
                    playerMap[player['id']] += 1
            if numberOfMembers == 1:
                continue
            for member in clusterMembers:
                squad = member['squad']
                for player in squad:
                    if (playerMap[player['id']]/numberOfMembers)*100 < 30:
                        member['live']['differentials'].append(player)

        return data

    @staticmethod
    def getBestInEachPositionLive(data, input):
        buckets = {}
        for playerId in input:
            player = input[playerId]
            if player['position'] not in buckets:
                buckets[player['position']] = []
            buckets[player['position']].append(player)
        for item in buckets:
            data[item] = copy.deepcopy(max(buckets[item], key=lambda x: x['totalPoints']))
        return data

    @staticmethod
    def runHistoricalAnalysisSuite(historicalData, teamInfo):
        teamInfoMap = {x['teamId']: x for x in teamInfo}
        gwScene, chipScene = BasicAnalytics.formatDataForHistoricalAnalysis(historicalData)
        statistics = BasicAnalytics.getHistoryStats(historicalData)
        statisticsPartTwo = BasicAnalytics.getBestManagerOfGWCounts(gwScene)
        statisticsPartThree = BasicAnalytics.getBestChipUsages(chipScene)
        timeseries = BasicAnalytics.getTeamTimeseries(gwScene, teamInfoMap)
        response = {}
        for stat in statistics:
            if stat == 'totalPointsTimeseries':
                formattedStat = stat
                response[formattedStat] = statistics[stat]
            else:
                for variant in statistics[stat]:
                    statType = 'highest' if variant == 'max' else 'lowest'
                    formattedStat = statType + stat.capitalize()
                    response[formattedStat] = statistics[stat][variant]
        response['mogwCounts'] = statisticsPartTwo
        for chipType in statisticsPartThree:
            formattedStat = 'highest{}Points'.format(chipType.capitalize())
            response[formattedStat] = statisticsPartThree[chipType]
        response['mogwCounts'] = statisticsPartTwo
        for stat in response:
            if stat != 'totalPointsTimeseries':
                for item in response[stat]:
                    teamId = item['teamId']
                    item.update(teamInfoMap[teamId])
            else:
                response[stat] = [{
                    'teamId' : x,
                    'playerName' : teamInfoMap[x]['playerName'],
                    'teamName': teamInfoMap[x]['teamName'],
                    'data' : response[stat][x]
                } for x in response[stat]]
        response['totalPointsTimeseries'] = timeseries
        return response

    @staticmethod
    def getRunningStats(teamSpecificTimeseries):
        for teamId in teamSpecificTimeseries:
            stats = {}
            stats['highestValue'] = max(teamSpecificTimeseries[teamId]['value']['value'])
            stats['netTransfers'] = sum(teamSpecificTimeseries[teamId]['event_transfers']['value'])
            stats['netTransfersCost'] = sum(teamSpecificTimeseries[teamId]['event_transfers_cost']['value'])
            stats['netPointsOnBench'] = sum(teamSpecificTimeseries[teamId]['points_on_bench']['value'])
            stats['maxPointsOnBench'] = max(teamSpecificTimeseries[teamId]['points_on_bench']['value'])
            stats['bestOverallRank'] = min(teamSpecificTimeseries[teamId]['overall_rank']['value'])
            teamSpecificTimeseries[teamId]['stats'] = stats
        return teamSpecificTimeseries

    @staticmethod
    def runCompareAnalysisSuite(historicalData, teamInfo):
        teamSpecificTimeseries = BasicAnalytics.generateTimeSerieses(historicalData)
        teamSpecificTimeseries = BasicAnalytics.getRunningStats(teamSpecificTimeseries)
        return teamSpecificTimeseries

    @staticmethod
    def getBestChipUsages(data):
        result = {x:[] for x in data}
        for chipType in data:
            processedList = sorted(data[chipType], key=lambda x : x['data']['points'], reverse=True)[:3]
            result[chipType] = [{'teamId':x['teamId'], 'value':x['data']['points']} for x in processedList]
        return result

    @staticmethod
    def getBestManagerOfGWCounts(data):
        gwWinners = {}
        for gwNum in data:
            if len(data[gwNum]) != 0:
                gwWinners[gwNum] = max(data[gwNum], key=lambda x : x['data']['points'])
        winnersList = list(gwWinners.values())
        winnerCounts = defaultdict(lambda : 0)
        for w in winnersList:
            winnerCounts[w['teamId']] += 1
        return sorted([{'teamId':x, 'value':winnerCounts[x]} for x in winnerCounts], key=lambda x : x['value'], reverse=True)[:3]

    @staticmethod
    def getBestGWScores(historicalData):
        bestGWScores = []
        results = {}
        for teamId in historicalData:
            currentTeamData = historicalData[teamId]['current']
            localBestGWScores = [x['points'] for x in currentTeamData]
            bestGWScores.extend([{'teamId':teamId, 'value':x} for x in localBestGWScores])
        results['max'] = sorted(bestGWScores, key=lambda x: x['value'], reverse=True)[:3]
        results['min'] = sorted(bestGWScores, key=lambda x: x['value'], reverse=False)[:3]
        return results

    @staticmethod
    def getCummulativeStats(historicalData):
        concernedAttributes = ['event_transfers', 'event_transfers_cost', 'points_on_bench']
        bestScores = {x:[] for x in concernedAttributes}
        results = {}
        for teamId in historicalData:
            currentTeamData = historicalData[teamId]['current']
            localBestScores = {x: 0 for x in concernedAttributes}
            for event in currentTeamData:
                for stat in localBestScores:
                    localBestScores[stat] += event[stat]
            for stat in bestScores:
                bestScores[stat].append({
                    'teamId':teamId,
                    'value':localBestScores[stat]
                })
        for stat in bestScores:
            results[stat] = {
                'min':None,
                'max':None
            }
            results[stat]['max'] = sorted(bestScores[stat], key=lambda x: x['value'], reverse=True)[:3]
            results[stat]['min'] = sorted(bestScores[stat], key=lambda x: x['value'], reverse=False)[:3]

        return results

    @staticmethod
    def getCurrentBestStats(historicalData):
        concernedAttributes = ['bank', 'value']
        bestScores = {x: [] for x in concernedAttributes}
        results = {}
        for teamId in historicalData:
            currentTeamData = historicalData[teamId]['current'][-1]
            for attrib in concernedAttributes:
                bestScores[attrib].append({
                    'teamId': teamId,
                    'value': currentTeamData[attrib]/10
                })

        for attrib in concernedAttributes:
            results[attrib] = {
                'min': None,
                'max': None,
            }
            results[attrib]['min'] = sorted(bestScores[attrib], key=lambda x: x['value'], reverse=False)[:3]
            results[attrib]['max'] = sorted(bestScores[attrib], key=lambda x: x['value'], reverse=True)[:3]
        return results

    @staticmethod
    def getTeamTimeseries(gwScene, teamInfoMap):
        results = {}
        for gwId in gwScene:
            results[gwId] = [{
                                 'teamId': x['teamId'],
                                 'totalPoints': x['data']['total_points'],
                                 'teamName': teamInfoMap[x['teamId']]['teamName'],
                                 'playerName': teamInfoMap[x['teamId']]['playerName']
            } for x in gwScene[gwId]]
        return results

    @staticmethod
    def getHistoryStats(historicalData):
        bestGWScores = BasicAnalytics.getBestGWScores(historicalData)
        bestStats = BasicAnalytics.getCummulativeStats(historicalData)
        currentBests = BasicAnalytics.getCurrentBestStats(historicalData)
        result = {
            'gwPoints' : bestGWScores,
            # 'totalPointsTimeseries' : timeseries,
        }
        result.update(bestStats)
        result.update(currentBests)
        renameMap = {
            'event_transfers' : 'eventTransfers',
            'event_transfers_cost': 'eventTransfersCost',
            'points_on_bench': 'pointsOnBench',
            'value': 'netValue'
        }
        for item in renameMap:
            temp = result[item]
            del result[item]
            result[renameMap[item]] = temp
        return result

    @staticmethod
    def generateTimeSerieses(data, columns=['points', 'total_points', 'overall_rank', 'bank', 'value', 'event_transfers', 'event_transfers_cost', 'points_on_bench'], index='event'):
        tMap = {}
        for teamId in data:
            tMap[teamId] = {}
            for col in columns + ['past_season_total_points', 'past_season_rank', 'chips', 'transfers']:
                tMap[teamId][col] = {
                    'index': [],
                    'value': []
                }
            for entry in data[teamId]['current']:
                for col in columns:
                    tMap[teamId][col]['index'].append(entry[index])
                    tMap[teamId][col]['value'].append(entry[col])
            for entry in data[teamId]['past']:
                for col in ['past_season_total_points', 'past_season_rank']:
                    tMap[teamId][col]['index'].append(entry['season_name'])
                    tMap[teamId][col]['value'].append(entry[col.replace('past_season_', '')])
            for entry in data[teamId]['chips']:
                tMap[teamId]['chips']['index'].append(entry['event'])
                tMap[teamId]['chips']['value'].append(entry['name'])
            transferBuckets = {}
            for entry in data[teamId]['transfers']:
                if entry['event'] not in transferBuckets:
                    transferBuckets[entry['event']] = []
                transferBuckets[entry['event']].append((entry['element_in'], entry['element_out']))
            tMap[teamId]['transfers'] = transferBuckets
        return tMap

    @staticmethod
    def formatDataForHistoricalAnalysis(data):
        gwScene = {x:[] for x in range(1,39)}
        chipScene = {x: [] for x in ['wildcard', 'freehit', 'bboost', 'wildcard', '3xc']}
        for teamId in data:
            currentData = data[teamId]['current']
            chipData = data[teamId]['chips']
            chipDataMap = {x['event']:x['name'] for x in chipData}
            for item in currentData:
                gwScene[item['event']].append({
                    'teamId' : teamId,
                    'data' : item
                })
                if item['event'] in list(chipDataMap.keys()):
                    chipType = chipDataMap[item['event']]
                    chipScene[chipType].append({
                        'teamId': teamId,
                        'data': item
                    })
        return gwScene, chipScene




