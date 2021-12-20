import pandas as pd
from datetime import datetime, timedelta
from fpldb.utils.configFileUtil import ConfigFileUtil
from fpldb.api.officialFPL.officialFPLApi import OfficialFPLApi
from fpldb.database.model.core import *
from fpldb.database.session.sessionFactory import DefaultSessionFactory
from fpldb.driver.criterion.criterion import Criterion
from fpldb.utils.coreUtils import CoreUtils
from fpldb.logger.logger import logger

class BootstrapDataUpdateCriterion(Criterion):

    ''' Update only once during GW per job '''

    cfUtil = ConfigFileUtil()
    fplApi = OfficialFPLApi()
    session = DefaultSessionFactory().getSession()

    def __init__(self, key=''):
        self.key = key

    @staticmethod
    def getGWStartDate(data):
        gwStartDate = min([pd.to_datetime(x['kickoff_time']) for x in data])
        return gwStartDate

    def isJobAlreadyComplete(self, gwNum):
        log = self.session.query(ActivityLog).filter(ActivityLog.activityId == self.key, ActivityLog.status.in_(
            [ActivityStatus.Completed, ActivityStatus.Started, ActivityStatus.Processing])).order_by(
            ActivityLog.completionTime.desc()).first()
        if log:
            completionDate = log.completionTime
            todayDate = datetime.now()
            if completionDate == todayDate:
                return True
        return False

    def isWithinMinsBeforeKickOffCacheUpdateTimeThreshold(self, gwNum):
        fixtureDetails = self.fplApi.getFixtures(gwNum=gwNum)
        startDatetime = BootstrapDataUpdateCriterion.getGWStartDate(fixtureDetails)
        startDatetime = startDatetime.replace(tzinfo=None)
        currentTime = datetime.utcnow()
        timeRange = self.cfUtil.getConfig('minsBeforeKickOffCacheUpdateTime', default=30)
        timeRange = timedelta(minutes=timeRange)
        if (currentTime - startDatetime) <= timeRange :
            return True
        return False

    def isValid(self):
        gwNum = CoreUtils.getGameweek()
        if self.isJobAlreadyComplete(gwNum):
            return False
        # if not self.isWithinMinsBeforeKickOffCacheUpdateTimeThreshold(gwNum):
        #     return False
        return True

if __name__ == '__main__':
    key = ''
    c = BootstrapDataUpdateCriterion(key=key)
    logger.info('[C] Key : {}, isValid : {}'.format(key, c.isValid()))