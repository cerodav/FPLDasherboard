from fpldb.logger.logger import logger
from fpldb.database.model.core import *
from fpldb.api.officialFPL.officialFPLApi import OfficialFPLApi
from fpldb.database.session.sessionFactory import DefaultSessionFactory
from fpldb.driver.job.baseJob import BaseJob
from dashboardService.analytics.basicAnalytics import BasicAnalytics
from fpldb.utils.pickleUtil import PickleUtil
from fpldb.utils.coreUtils import CoreUtils

class HistoryCollectionPickleJob(BaseJob):

    fplApi = OfficialFPLApi()
    session = DefaultSessionFactory().getSession()

    def __init__(self):
        self.key = 'HistoryCollectionPickleJob'

    def getLeagueIdListFromDB(self, priorityLevel = None):
        if priorityLevel is not None:
            leagues = self.session.query(League).filter(League.priority == priorityLevel).all()
        else:
            leagues = self.session.query(League).order_by(League.priority).all()
        return [x.leagueId for x in leagues]

    def run(self):
        logger.info('Running HistoryCollectionPickleJob ...')
        leagueIds = self.getLeagueIdListFromDB(priorityLevel=0)
        history = {}
        for leagueId in leagueIds:
            logger.info('Collecting historical league id # {} data'.format(leagueId))
            leagueData = self.fplApi.getClassicLeagueStandings(leagueId)
            teamsInLeague = [{'teamId':x['entry'], 'playerName':x['player_name'], 'teamName':x['entry_name']} for x in leagueData['standings']['results']]
            for team in teamsInLeague:
                teamId = team['teamId']
                historicalData = self.fplApi.getHistory(teamId)
                history[teamId] = historicalData
            stats = BasicAnalytics.runHistoricalAnalysisSuite(history, teamsInLeague)
            PickleUtil.saveToPickle(stats, CoreUtils.getStatsPickleFileName(CoreUtils.getGameweek(), leagueId))
            logger.info('Completed generating pickle for league id # {}'.format(leagueId))

if __name__ == '__main__':
    l = HistoryCollectionPickleJob()
    l.run()


