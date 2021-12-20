from fpldb.logger.logger import logger
from fpldb.database.model.core import *
from fpldb.api.officialFPL.officialFPLApi import OfficialFPLApi
from fpldb.database.session.sessionFactory import DefaultSessionFactory
from fpldb.driver.job.baseJob import BaseJob

class FPLBootstrapDataUpdateJob(BaseJob):

    fplApi = OfficialFPLApi()
    session = DefaultSessionFactory().getSession()

    def __init__(self):
        self.criteria = None
        self.key = 'FPLBootstrapDataUpdateJob'

    def getBootstrapData(self):
        staticData = self.fplApi.getStaticPlayerData()
        return staticData

    def getPlayer(self, playerDetail):
        p = Player()
        p.playerId = playerDetail['id']
        p.totalPoints = playerDetail['total_points']
        p.bonus = playerDetail['bps']
        p.code = playerDetail['code']
        p.cost = playerDetail['now_cost']
        p.assists = playerDetail['assists']
        p.bonusPoints = playerDetail['bonus']
        p.chanceOfPlaying = playerDetail['chance_of_playing_next_round']
        p.cleanSheets = playerDetail['clean_sheets']
        p.creativity = playerDetail['creativity']
        p.creativityRank = playerDetail['creativity_rank']
        p.influence = playerDetail['influence']
        p.influenceRank = playerDetail['influence_rank']
        p.threat = playerDetail['threat']
        p.threatRank = playerDetail['threat_rank']
        p.ictIndex = playerDetail['ict_index']
        p.ictRank = playerDetail['ict_index_rank']
        p.firstName = playerDetail['first_name']
        p.lastName = playerDetail['second_name']
        p.webName = playerDetail['web_name']
        p.goals = playerDetail['goals_scored']
        p.goalsConceded = playerDetail['goals_conceded']
        p.ownGoals = playerDetail['own_goals']
        p.yellowCards = playerDetail['yellow_cards']
        p.redCards = playerDetail['red_cards']
        p.penaltiesMissed = playerDetail['penalties_missed']
        p.penaltiesSaved = playerDetail['penalties_saved']
        p.minutes = playerDetail['minutes']
        p.photo = playerDetail['photo']
        p.saves = playerDetail['saves']
        return  p

    def run(self):
        self.session.query(Player).delete()
        data = self.getBootstrapData()
        for idx in data:
            playerDetail = data[idx]
            p = self.getPlayer(playerDetail)
            self.session.add(p)
        self.session.commit()

if __name__ == '__main__':
    f = FPLBootstrapDataUpdateJob()
    f.run()