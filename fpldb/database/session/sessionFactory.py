from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fpldb.utils.configFileUtil import ConfigFileUtil

class DefaultSessionFactory :

    def __init__(self):
        self.cFileUtil = ConfigFileUtil()
        connectionString = self.getConnectionString()
        self.engine = create_engine(connectionString, connect_args={'charset':'utf8'})
        sessionFactory = sessionmaker(bind=self.engine)
        self.session = sessionFactory()

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

        if dbDetails is None or None in [dbType, userName, password, endpoint, port, dbName]:
            raise Exception('Error while formulating the connection string for DB connection')

        connectionStringTemplate = '{}://{}:{}@{}:{}/{}'

        return connectionStringTemplate.format(dbType, userName, password, endpoint, port, dbName)

if __name__ == '__main__':
    d = DefaultSessionFactory()
    s = d.getSession()
    r = s.execute('Select * from League')
    for row in r :
        print(row.name)







