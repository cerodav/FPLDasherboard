create table League (
    leagueId        varchar(128) not null,
    name            varchar(255) not null,
    type            varchar(128) not null,
    createdTime     datetime default CURRENT_TIMESTAMP,
    modifiedTime    datetime default CURRENT_TIMESTAMP,
    priority        int null default 0,
    primary key (leagueId)
);

create table Team (
    teamId          varchar(128) not null,
    name            varchar(255) not null,
    userName        varchar(255) not null,
    wc1Played       bit null,
    wc2Played       bit null,
    tcPlayed        bit null,
    bbPlayed        bit null,
    fhPlayed        bit null,
    createdTime     datetime default CURRENT_TIMESTAMP,
    modifiedTime    datetime default CURRENT_TIMESTAMP,
    primary key (teamId)
);

create table LeagueMembership (
    leagueId        varchar(128) not null,
    teamId          varchar(128) not null,
    createdTime     datetime default CURRENT_TIMESTAMP,
    modifiedTime    datetime default CURRENT_TIMESTAMP,
    leagueRank      int(10) null,
    lastRank        int(10) null,
    rankSort        int(10) null;
    foreign key (leagueId) REFERENCES League(leagueId),
    foreign key (teamId) REFERENCES Team(teamId)
);

alter table fpldb_devdb.Team
add column overallRank int(10) null,
add column overallPoints int(10) null,
add column bankValue float(10,1) null,
add column squadValue float(10,1) null,
add column gameweek int(10) null,
add column totalTransfers int(10) null;

alter table fpldb_devdb.Team
add column gameweekTransfers int(10) null,
add column gameweekTransferCost int(10) null,
add column activeChip varchar(128) null;

alter table fpldb_devdb.LeagueMembership
add column gameweek int(10) null,
add column gameweekPoints int(10) null,
add column totalPoints int(10) null,
add column activeChip varchar(128) null;

alter table fpldb_devdb.TeamMembership
add column playingStatus varchar(10) null,
add column captain bit null,
add column vicecaptain bit null;

create table TeamMembership (
    teamId          varchar(128) not null,
    playerId        varchar(128) not null,
    gameweek        int(10) not null,
    createdTime     datetime default CURRENT_TIMESTAMP,
    modifiedTime    datetime default CURRENT_TIMESTAMP,
    foreign key (teamId) REFERENCES Team(teamId)
);

create table Player (
    playerId          varchar(128) not null,
    firstName		  varchar(128) not null,
    lastName 		  varchar(128) not null,
    webName           varchar(128) not null,
    teamName          varchar(128) not null,
    code 			  int(10) null,
    cost			  float(10) null,
    photo			  varchar(128) null,
    totalPoints		  int(10) null,
    minutes			  int(10) null,
    goals             int(10) null,
    assists           int(10) null,
    cleanSheets       int(10) null,
    goalsConceded     int(10) null,
    ownGoals      	  int(10) null,
    penaltiesSaved    int(10) null,
    penaltiesMissed   int(10) null,
    yellowCards       int(10) null,
    redCards          int(10) null,
    saves             int(10) null,
    bonusPoints       int(10) null,
    bonus			  int(10) null,
    influence		  float(10) null,
    creativity		  float(10) null,
    threat		  	  float(10) null,
    influenceRank	  int(10) null,
    creativityRank	  int(10) null,
    threatRank		  int(10) null,
    ictIndex		  float(10) null,
    ictRank		  	  int(10) null,
    chanceOfPlaying	  int(10) null,
    createdTime     datetime default CURRENT_TIMESTAMP,
    modifiedTime    datetime default CURRENT_TIMESTAMP
);

create table ActivityLog (
    logId             int not null auto_increment,
    activityId        varchar(512) not null,
    status            varchar(64) null,
    gameweek          int not null,
    completionTime    datetime default CURRENT_TIMESTAMP,
    primary key (logId)
);