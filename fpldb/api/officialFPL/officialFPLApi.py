import requests
import json
from fpldb.logger.logger import logger

class OfficialFPLApi:

    _baseUrl = 'https://fantasy.premierleague.com/api/'
    _staticFPLBootstrapData = None

    @staticmethod
    def getCompleteUrl(slug):
        return OfficialFPLApi._baseUrl + slug

    @staticmethod
    def getTeamDetails(teamId):
        logger.info('Collecting basic team info for {}'.format(teamId))

        slug = 'entry/{}/'
        formattedSlug = slug.format(teamId)
        completedUrl = OfficialFPLApi.getCompleteUrl(formattedSlug)
        logger.info('Request for basic team info : {}'.format(completedUrl))

        r = requests.get(completedUrl)
        responseData = r.json()
        # logger.info('Collected response for classic league standings : {}'.format(responseData))
        return responseData

    @staticmethod
    def getLiveData(eventNumber):
        logger.info('Collecting live data info')

        slug = 'event/{}/live'
        formattedSlug = slug.format(eventNumber)
        completedUrl = OfficialFPLApi.getCompleteUrl(formattedSlug)
        logger.info('Request for basic team info : {}'.format(completedUrl))

        r = requests.get(completedUrl)
        responseData = r.json()
        # logger.info('Collected response for live data : {}'.format(responseData))
        return responseData

    @staticmethod
    def getStaticPlayerData():
        staticPlayerData = {}
        for player in OfficialFPLApi.getStaticDataBootstrap()['elements']:
            staticPlayerData[player['id']] = player
        return staticPlayerData

    @staticmethod
    def getLatestEventData():
        latestEventData = {}
        selectedEvent = None
        interestedFields = ['name', 'average_entry_score', 'highest_score', 'most_selected', 'most_transferred_in', 'top_element', 'top_element_info',
                            'most_captained', 'most_vice_captained']
        renamedFields = ['name', 'avgScore', 'highestScore', 'mostSelectedId', 'mostTransferredInId', 'highestScoringPlayerId', 'highestScoringPlayerInfo',
                         'mostCaptainedId', 'mostViceCaptainedId']
        deltaAvgScore = 0
        deltaHighestScore = 0
        deltaHighestScoringPlayerScore = 0
        for event in OfficialFPLApi.getStaticDataBootstrap()['events']:
            if event['finished']:
                if selectedEvent is None:
                    selectedEvent = event
                else:
                    deltaAvgScore = event['average_entry_score'] - selectedEvent['average_entry_score']
                    deltaHighestScore = event['highest_score'] - selectedEvent['highest_score']
                    deltaHighestScoringPlayerScore = event['top_element_info']['points'] - selectedEvent['top_element_info']['points']
                    selectedEvent = event
                continue

            if not event['finished']:
                break

        for field, renamedField in zip(interestedFields, renamedFields):
            latestEventData[renamedField] = selectedEvent[field]

        latestEventData['deltaAvgScore'] = deltaAvgScore
        latestEventData['deltaHighestScore'] = deltaHighestScore
        latestEventData['deltaHighestScoringPlayerScore'] = deltaHighestScoringPlayerScore

        return latestEventData

    @staticmethod
    def getFixtures(gwNum):
        logger.info('Collecting fixture information')

        slug = 'fixtures/?event={}'
        formattedSlug = slug.format(gwNum)
        completedUrl = OfficialFPLApi.getCompleteUrl(formattedSlug)
        logger.info('Request for event status : {}'.format(completedUrl))

        r = requests.get(completedUrl)
        responseData = r.json()
        return responseData

    @staticmethod
    def getEventStatus():
        logger.info('Collecting event status')

        slug = 'event-status/'
        formattedSlug = slug
        completedUrl = OfficialFPLApi.getCompleteUrl(formattedSlug)
        logger.info('Request for event status : {}'.format(completedUrl))

        r = requests.get(completedUrl)
        responseData = r.json()
        return responseData

    @staticmethod
    def getHistory(teamId):
        logger.info('Collecting history data')

        slug = 'entry/{}/history/'
        formattedSlug = slug.format(teamId)
        completedUrl = OfficialFPLApi.getCompleteUrl(formattedSlug)
        logger.info('Request for event status : {}'.format(completedUrl))

        r = requests.get(completedUrl)
        responseData = r.json()
        return responseData

    @staticmethod
    def getStaticTeamData():
        staticTeamData = {}
        for team in OfficialFPLApi.getStaticDataBootstrap()['teams']:
            staticTeamData[team['id']] = team
        return staticTeamData

    @staticmethod
    def getStaticDataBootstrap():
        if OfficialFPLApi._staticFPLBootstrapData is not None:
            return OfficialFPLApi._staticFPLBootstrapData

        logger.info('Collecting bootstrap static data')

        slug = 'bootstrap-static/'
        formattedSlug = slug
        completedUrl = OfficialFPLApi.getCompleteUrl(formattedSlug)
        logger.info('Request for bootstrap static data : {}'.format(completedUrl))

        r = requests.get(completedUrl)
        responseData = r.json()
        OfficialFPLApi._staticFPLBootstrapData = responseData
        return OfficialFPLApi._staticFPLBootstrapData

    @staticmethod
    def getPlayerData(playerId):
        logger.info('Collecting player data for {}'.format(playerId))

        slug = 'element-summary/{}/'
        formattedSlug = slug.format(playerId)
        completedUrl = OfficialFPLApi.getCompleteUrl(formattedSlug)
        logger.info('Request for player info : {}'.format(completedUrl))

        r = requests.get(completedUrl)
        responseData = r.json()
        logger.info('Collected response for player info : {}'.format(responseData))
        return responseData

    @staticmethod
    def getGWPlayerPick(teamId, gw=1):
        logger.info('Collecting player picks for {}, {}'.format(teamId, gw))

        slug = 'entry/{}/event/{}/picks/'
        formattedSlug = slug.format(teamId, gw)
        completedUrl = OfficialFPLApi.getCompleteUrl(formattedSlug)
        logger.info('Request for player picks : {}'.format(completedUrl))

        r = requests.get(completedUrl)
        responseData = r.json()
        # logger.info('Collected response for classic league standings : {}'.format(responseData))
        return responseData

    @staticmethod
    def getClassicLeagueStandings(leagueId):
        if leagueId is None or leagueId == '':
            return None

        logger.info('Collecting classic league standings for {}'.format(leagueId))

        slug = 'leagues-classic/{}/standings/'
        formattedSlug = slug.format(leagueId)
        completedUrl = OfficialFPLApi.getCompleteUrl(formattedSlug)
        logger.info('Request for classic league standings : {}'.format(completedUrl))

        r = requests.get(completedUrl)
        responseData = r.json()
        return responseData

if __name__ == '__main__':
    OfficialFPLApi.getClassicLeagueStandings(854530)


