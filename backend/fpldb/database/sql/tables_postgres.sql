create table League (
    "leagueId"        varchar(128) not null,
    "name"            varchar(255) not null,
    "type"            varchar(128) not null,
    "createdTime"     timestamp default CURRENT_TIMESTAMP,
    "modifiedTime"    timestamp default CURRENT_TIMESTAMP,
    "priority"        int null default 0,
    primary key ("leagueId")
);

create table Team (
    "teamId"          varchar(128) not null,
    "name"            varchar(255) not null,
    "userName"        varchar(255) not null,
    "wc1Played"       boolean null,
    "wc2Played"       boolean null,
    "tcPlayed"        boolean null,
    "bbPlayed"        boolean null,
    "fhPlayed"        boolean null,
    "createdTime"     timestamp default CURRENT_TIMESTAMP,
    "modifiedTime"    timestamp default CURRENT_TIMESTAMP,
    primary key ("teamId")
);

create table LeagueMembership (
    "leagueId"        varchar(128) not null,
    "teamId"          varchar(128) not null,
    "createdTime"     timestamp default CURRENT_TIMESTAMP,
    "modifiedTime"    timestamp default CURRENT_TIMESTAMP,
    "leagueRank"      int null,
    "lastRank"        int null,
    "rankSort"        int null,
    foreign key ("leagueId") REFERENCES League("leagueId"),
    foreign key ("teamId") REFERENCES Team("teamId")
);

alter table Team
add column "overallRank" int null,
add column "overallPoints" int null,
add column "bankValue" numeric(10,1) null,
add column "squadValue" numeric(10,1) null,
add column "gameweek" int null,
add column "totalTransfers" int null,
add column "gameweekPoints" int null,
add column "gameweekTransfers" int null,
add column "gameweekTransferCost" int null,
add column "activeChip" varchar(128) null;

alter table LeagueMembership
add column "gameweek" int null,
add column "gameweekPoints" int null,
add column "totalPoints" int null,
add column "activeChip" varchar(128) null;

create table TeamMembership (
    "teamId"          varchar(128) not null,
    "playerId"        varchar(128) not null,
    "gameweek"        int not null,
    "createdTime"     timestamp default CURRENT_TIMESTAMP,
    "modifiedTime"    timestamp default CURRENT_TIMESTAMP,
    foreign key ("teamId") REFERENCES Team("teamId")
);

alter table TeamMembership
add column "playingStatus" varchar(10) null,
add column "captain" boolean null,
add column "vicecaptain" boolean null;

create table Player (
    "playerId"            varchar(128) not null,
    "firstName"		      varchar(128) not null,
    "lastName" 		      varchar(128) not null,
    "webName"             varchar(128) not null,
    "teamName"            varchar(128) not null,
    "code" 			      int null,
    "cost"			      numeric(10, 1) null,
    "photo"			      varchar(128) null,
    "totalPoints"		  int null,
    "minutes"			  int null,
    "goals"               int null,
    "assists"             int null,
    "cleanSheets"         int null,
    "goalsConceded"       int null,
    "ownGoals"      	  int null,
    "penaltiesSaved"      int null,
    "penaltiesMissed"     int null,
    "yellowCards"         int null,
    "redCards"            int null,
    "saves"               int null,
    "bonusPoints"         int null,
    "bonus"			      int null,
    "influence"		      numeric(10, 1) null,
    "creativity"		  numeric(10, 1) null,
    "threat"		  	  numeric(10, 1) null,
    "influenceRank"	      int null,
    "creativityRank"	  int null,
    "threatRank"		  int null,
    "ictIndex"		      numeric(10, 1) null,
    "ictRank"		  	  int null,
    "chanceOfPlaying"	  int null,
    "createdTime"         timestamp default CURRENT_TIMESTAMP,
    "modifiedTime"        timestamp default CURRENT_TIMESTAMP
);

create table ActivityLog (
    "logId"             serial not null,
    "activityId"        varchar(512) not null,
    "status"            varchar(64) null,
    "gameweek"          int not null,
    "completionTime"    timestamp default CURRENT_TIMESTAMP,
    primary key ("logId")
);
