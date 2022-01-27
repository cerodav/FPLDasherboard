from fpldb.logger.logger import logger
from fpldb.utils.typesUtil import ActivityStatus
from fpldb.database.model.core import *
from fpldb.api.officialFPL.officialFPLApi import OfficialFPLApi
from fpldb.utils.coreUtils import CoreUtils
from fpldb.database.session.sessionFactory import DefaultSessionFactory
from datetime import datetime

class BaseJob:

    session = DefaultSessionFactory().getSession()
    fplApi = OfficialFPLApi()

    def start(self):
        exceptionOccured = False
        try:
            logger.info(' + Starting job : {}'.format(self.key))
            self.recordActivity(ActivityStatus.Started)
            self.run()
        except Exception as e:
            logger.exception(' ! Failure while running job : {}'.format(self.key))
            self.recordActivity(ActivityStatus.Failed)
            exceptionOccured = True
        if not exceptionOccured:
            logger.info(' + Completed running job : {}'.format(self.key))
            self.recordActivity(ActivityStatus.Completed)

    def recordActivity(self, activityStatus, gw=None):
        if not getattr(self, 'key', None) or self.key is None:
            return

        if gw is None:
            gw = CoreUtils.getGameweek()

        a = ActivityLog()
        a.gameweek = gw
        a.activityId = self.key
        a.completionTime = datetime.now()
        a.status = activityStatus.name
        self.session.add(a)
        self.session.commit()
