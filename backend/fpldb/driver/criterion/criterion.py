import pandas as pd
from datetime import datetime, timedelta
from fpldb.utils.configFileUtil import ConfigFileUtil
from fpldb.api.officialFPL.officialFPLApi import OfficialFPLApi
from fpldb.database.model.core import *
from fpldb.database.session.sessionFactory import DefaultSessionFactory

class Criterion:

    def isValid(self):
        return True

if __name__ == '__main__':
    t = Criterion()
    t.isValid()