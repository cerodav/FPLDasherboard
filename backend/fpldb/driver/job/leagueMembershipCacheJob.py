from fpldb.logger.logger import logger
from fpldb.database.model.core import *
from fpldb.api.officialFPL.officialFPLApi import OfficialFPLApi
from fpldb.database.session.sessionFactory import DefaultSessionFactory
from fpldb.driver.job.baseJob import BaseJob
from fpldb.utils.coreUtils import CoreUtils

class LeagueMembershipCacheJob(BaseJob):

    fplApi = OfficialFPLApi()
    session = DefaultSessionFactory().getSession()

    def __init__(self):
        self.key = 'LeagueMembershipCacheJob'

    def getLeagueIdListFromDB(self, priorityLevel = None):
        if priorityLevel is not None:
            leagues = self.session.query(League).filter(League.priority == priorityLevel).all()
        else:
            leagues = self.session.query(League).order_by(League.priority).all()
        return [x.leagueId for x in leagues]

    def run(self):
        logger.info('Running LeagueMembershipCacheJob ...')
        # leagueIds = self.getLeagueIdListFromDB(priorityLevel=0)
        leagueIds = ['1143965']
        for leagueId in leagueIds:
            logger.info('Onboarding/updating league id # {}'.format(leagueId))
            CoreUtils.onboardLeague(leagueId)
            logger.info('Completed onboarding/updating league id # {}'.format(leagueId))

if __name__ == '__main__':
    l = LeagueMembershipCacheJob()
    l.run()


