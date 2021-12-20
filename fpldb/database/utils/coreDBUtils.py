from fpldb.logger.logger import logger
from fpldb.database.model.core import *
from fpldb.api.officialFPL.officialFPLApi import OfficialFPLApi
from fpldb.database.session.sessionFactory import DefaultSessionFactory

class CoreDBUtils:

    session = DefaultSessionFactory().getSession()
    fplApi = OfficialFPLApi()

    @staticmethod
    def getLeagueMembershipDetails(leagueId):
        leagueMembership = CoreDBUtils.session.query(LeagueMembership).filter(LeagueMembership.leagueId == leagueId).all()
        if leagueMembership is None or len(leagueMembership) == 0:
            return None
        return leagueMembership

    @staticmethod
    def getLeagueDetails(leagueId):
        t = CoreDBUtils.session.query(League).filter(League.leagueId == leagueId).one_or_none()
        return t

    @staticmethod
    def getTeamDetails(teamId, gw=None):
        t = CoreDBUtils.session.query(Team).filter(Team.teamId == teamId)
        if gw:
            t = t.filter(Team.gameweek == gw)
        t = t.one_or_none()
        return t

    @staticmethod
    def getTeamMembershipDetails(teamId, gw = None):
        if gw is None:
            teamMembership = CoreDBUtils.session.query(TeamMembership).filter(
                TeamMembership.teamId == teamId).all()
        else:
            teamMembership = CoreDBUtils.session.query(TeamMembership).filter(
                TeamMembership.teamId == teamId, TeamMembership.gameweek == gw).all()
        if teamMembership is None or len(teamMembership) == 0:
            return None
        return teamMembership

    @staticmethod
    def getPlayer(playerId):
        return CoreDBUtils.session.query(Player).filter(Player.playerId == playerId).one_or_none()

    @staticmethod
    def wipeOutTeamMetadata(teamId, commit=False):
        t = CoreDBUtils.session.query(Team).filter(Team.teamId == teamId).delete()
        if commit:
            CoreDBUtils.session.commit()

    @staticmethod
    def wipeOutLeagueMembershipData(leagueId, commit=False):
        CoreDBUtils.session.query(LeagueMembership).filter(LeagueMembership.leagueId == leagueId).delete()
        if commit:
            CoreDBUtils.session.commit()

    @staticmethod
    def wipeOutTeamMembershipData(teamId, commit=False):
        t = CoreDBUtils.session.query(TeamMembership).filter(TeamMembership.teamId == teamId).delete()
        if commit:
            CoreDBUtils.session.commit()

