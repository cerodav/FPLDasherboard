from sqlalchemy import Column, String, Integer, Date, Boolean, ForeignKey, Float, PrimaryKeyConstraint
from sqlalchemy.types import Enum as SQLAlchemyEnumType
from enum import Enum
from fpldb.utils.typesUtil import ActivityStatus
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class League(Base):
    __tablename__ = 'League'
    leagueId = Column(String, primary_key=True)
    name = Column(String)
    type = Column(String)
    createdTime = Column(Date)
    modifiedTime = Column(Date)
    members = relationship('LeagueMembership')
    priority = Column(Integer)

class ChipType(Enum):
    Benchboost = 1
    TripleCap = 2
    Freehit = 3
    Wildcard = 4

    @staticmethod
    def getChipType(name):
        if name is None:
            return None

        if name in ChipType.__members__:
            return ChipType.__members__[name]
        else:
            return None

class Team(Base):
    __tablename__ = 'Team'
    teamId = Column(String, primary_key=True)
    name = Column(String)
    userName = Column(String)
    wc1Played = Column(Boolean)
    wc2Played = Column(Boolean)
    tcPlayed = Column(Boolean)
    bbPlayed = Column(Boolean)
    fhPlayed = Column(Boolean)
    createdTime = Column(Date)
    modifiedTime = Column(Date)
    overallRank = Column(Integer)
    overallPoints = Column(Integer)
    bankValue = Column(Float)
    squadValue = Column(Float)
    gameweek = Column(Integer)
    gameweekPoints = Column(Integer)
    totalTransfers = Column(Integer)
    gameweekTransfers = Column(Integer)
    gameweekTransferCost = Column(Integer)
    activeChip = Column(SQLAlchemyEnumType(ChipType))
    squad = relationship("TeamMembership")


'''
add column gameweekTransfers int(10) null,
add column gameweekTransferCost int(10) null,
add column activeChip varchar(128) null;
'''
'''
alter table fpldb_devdb.Team
add column overallRank int(10) null,
add column overallPoints int(10) null,
add column bankValue float(10,1) null,
add column squadValue float(10,1) null,
add column gameweek int(10) null,
add column totalTransfers int(10) null;
'''
class LeagueMembership(Base):
    __tablename__ = 'LeagueMembership'
    __table_args__ = (
        PrimaryKeyConstraint('leagueId', 'teamId'),
    )
    leagueId = Column(String, ForeignKey('League.leagueId'))
    teamId = Column(String, ForeignKey('Team.teamId'))
    gameweek = Column(Integer)
    gameweekPoints = Column(Integer)
    totalPoints = Column(Integer)
    createdTime = Column(Date)
    modifiedTime = Column(Date)
    leagueRank = Column(Integer)
    lastRank = Column(Integer)
    rankSort = Column(Integer)
    team = relationship("Team")

'''
add column leagueRank int(10) null,
add column lastRank int(10) null,
add column rankSort int(10) null;
'''

'''
alter table fpldb_devdb.LeagueMembership
add column gameweek int(10) null,
add column gameweekPoints int(10) null,
add column totalPoints int(10) null,
add column transfers int(10) null,
add column transferCost int(10) null,
add column activeChip varchar(128) null;
'''

class SquadStatus(Enum):
    Bench = 1
    Playing = 2

class TeamMembership(Base):
    __tablename__ = 'TeamMembership'
    __table_args__ = (
        PrimaryKeyConstraint('teamId', 'playerId'),
    )
    teamId = Column(String, ForeignKey('Team.teamId'))
    playerId = Column(String, ForeignKey('Player.playerId'))
    gameweek = Column(Integer)
    playingStatus = Column(SQLAlchemyEnumType(SquadStatus))
    captain = Column(Boolean)
    vicecaptain = Column(Boolean)
    createdTime = Column(Date)
    modifiedTime = Column(Date)
    player = relationship('Player')

'''
alter table fpldb_devdb.TeamMembership
add column playingStatus varchar(10) null,
add column captain bit null,
add column vicecaptain bit null;
'''

class Player(Base):
    __tablename__ = 'Player'
    playerId = Column(String, primary_key=True)
    firstName = Column(String)
    lastName = Column(String)
    webName = Column(String)
    teamName = Column(String)
    code = Column(Integer)
    cost = Column(Float)
    photo = Column(String)
    totalPoints = Column(Integer)
    minutes = Column(Integer)
    goals = Column(Integer)
    assists = Column(Integer)
    cleanSheets = Column(Integer)
    goalsConceded = Column(Integer)
    ownGoals = Column(Integer)
    penaltiesSaved = Column(Integer)
    penaltiesMissed = Column(Integer)
    yellowCards = Column(Integer)
    redCards = Column(Integer)
    saves = Column(Integer)
    bonusPoints = Column(Integer)
    bonus = Column(Integer)
    influence = Column(Float)
    creativity = Column(Float)
    threat = Column(Float)
    influenceRank = Column(Integer)
    creativityRank = Column(Integer)
    threatRank = Column(Integer)
    ictIndex = Column(Float)
    ictRank = Column(Integer)
    chanceOfPlaying = Column(Integer)
    createdTime = Column(Date)
    modifiedTime = Column(Date)

class ActivityLog(Base):
    __tablename__ = 'ActivityLog'
    logId = Column(Integer, primary_key=True)
    activityId = Column(String)
    gameweek = Column(Integer)
    completionTime = Column(Date)
    status = Column(SQLAlchemyEnumType(ActivityStatus))

if __name__ == '__main__':

    from fpldb.database.session.sessionFactory import DefaultSessionFactory
    d = DefaultSessionFactory()
    s = d.getSession()
    r = s.query(League).all()
    for row in r :
        print(row.name)



