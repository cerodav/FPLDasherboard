from fpldb.dashboardService.dataCollectors.datastore import Datastore

class ClassicLeagueDatastore:

    @staticmethod
    def addLeague(leagueId, data):
        key = 'leagueId#{}'.format(leagueId)
        Datastore.add(key, data)

    @staticmethod
    def getLeague(leagueId):
        key = 'leagueId#{}'.format(leagueId)
        return Datastore.get(key)

    @staticmethod
    def addTeam(teamId, data):
        key = 'teamId#{}'.format(teamId)
        Datastore.add(key, data)

    @staticmethod
    def getTeam(teamId):
        key = 'teamId#{}'.format(teamId)
        return Datastore.get(key)

    @staticmethod
    def clearAll():
        Datastore.cleanUp()
