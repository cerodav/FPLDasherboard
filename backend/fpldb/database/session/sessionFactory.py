from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fpldb.utils.configFileUtil import ConfigFileUtil

class DefaultSessionFactory :

    def __init__(self):
        self.cFileUtil = ConfigFileUtil()
        connectionString = self.getConnectionString()
        self.engine = self.genEngine(connectionString)
        sessionFactory = sessionmaker(bind=self.engine)
        self.session = sessionFactory()
        self.dbType = None

    def genEngine(self, connStr):
        if self.dbType == 'postgres':
            return create_engine(connStr)
        else:
            return create_engine(connStr, connect_args={'charset': 'utf8'})

    def getSession(self):
        return self.session

    def getEngine(self):
        return self.engine

    def getConnectionString(self):
        dbDetails = self.cFileUtil.getConfig('dbDetails', default=None)
        if dbDetails is not None:
            dbType = dbDetails.get('dbType', None)
            userName = dbDetails.get('dbUserName', None)
            password = dbDetails.get('dbPassword', None)
            endpoint = dbDetails.get('dbEndpoint', None)
            port = dbDetails.get('dbPort', None)
            dbName = dbDetails.get('dbName', None)
            connStr = dbDetails.get('connStr', None)

        if dbDetails is None or (None in [dbType, userName, password, endpoint, port, dbName] and connStr is None):
            raise Exception('Error while formulating the connection string for DB connection')

        self.dbType = dbType
        if connStr:

            return connStr
        else:
            connectionStringTemplate = '{}://{}:{}@{}:{}/{}'
            return connectionStringTemplate.format(dbType, userName, password, endpoint, port, dbName)

if __name__ == '__main__':
    d = DefaultSessionFactory()
    s = d.getSession()
    s.execute("SELECT current_database();")
    r = s.execute('Select * from League')
    for row in r :
        print(row.name)







