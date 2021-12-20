import sys
import time
from fpldb.logger.logger import logger
from fpldb.utils.configFileUtil import ConfigFileUtil
from fpldb.driver.criterion.membershipUpdateCriterion import MembershipUpdateCriterion
from fpldb.driver.criterion.bootstrapDataUpdateCriterion import BootstrapDataUpdateCriterion
from fpldb.driver.job.fplBootstrapDataUpdateJob import *
from fpldb.driver.job.leagueMembershipCacheJob import *

class Driver:

    jobs = {
        'FPLBootstrapDataUpdateJob': FPLBootstrapDataUpdateJob,
        'LeagueMembershipCacheJob': LeagueMembershipCacheJob,
    }

    criteria = {
        'MembershipUpdateEvent' : MembershipUpdateCriterion,
        'BootstrapDataUpdateEvent' : BootstrapDataUpdateCriterion,
    }

    def __init__(self, force=False):
        self.force = False
        logger.info('Driver setting up ...')
        if force:
            self.force = force
            logger.info("Criteria won't be evaluated ...")
            logger.info("Force flag set to True ...")
        self.routine = ConfigFileUtil().getConfig('driverRoutine', None)

        if self.routine is None:
            logger.info('No routine available, exiting')
            sys.exit(0)

    def wait(self, secs=60):
        time.sleep(secs)

    def run(self):
        for idx in self.routine:
            job = self.routine[idx]
            jobName = job['jobName']
            criteriaName = job['criteria']
            jobClass = self.jobs.get(jobName, None)
            criterionClass = self.criteria.get(criteriaName, None)
            if jobClass is None:
                logger.error(' ! Error when trying to find Job Class. Skipping ...')
                continue
            jobInstance = jobClass()
            criterionInstance = criterionClass(key=jobName)
            if self.force or criterionInstance.isValid():
                jobInstance.start()

if __name__ == '__main__':
    d = Driver(force=False)
    d.run()

