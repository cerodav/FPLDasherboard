import { CalendarIcon, StarIcon, FlameIcon, MirrorIcon, LogoGistIcon, VersionsIcon, RssIcon, ZapIcon } from '@primer/octicons-react';
// export const API_ROOT_URL = 'http://192.168.0.96:8086/api/live'
export const API_LIVE_ROOT_URL = 'http://35.164.86.119:8086/api/live'
export const API_NEWS_UDPATES_ROOT_URL = 'http://35.164.86.119:8086/api/news-updates'
// export const API_LIVE_ROOT_URL = 'http://localhost:8086/api/live'
// export const API_NEWS_UDPATES_ROOT_URL = 'http://localhost:8086/api/news-updates'
export const DEFAULT_REDIRECT = '/classicleague/1143965'
export const ALLOW_DARK_MODE_TOGGLE = false
export const PAGE_PREFIXES = {
  ClassicLeagueHomePage: '/classicleague/'
}
export const FPL_BACKEND_CALL = {
  leagueStatistics: `${API_LIVE_ROOT_URL}/leaguestatistics/`,
  compareStatistics: `${API_LIVE_ROOT_URL}/compstatistics/`,
  latestStatistics: `${API_LIVE_ROOT_URL}/lateststatistics`,
  liveClassicLeagueStandings: `${API_LIVE_ROOT_URL}/classicleague/`,
  gameweekDetails: `${API_LIVE_ROOT_URL}/gameweekdetails/`,
  newsGrab: `${API_NEWS_UDPATES_ROOT_URL}/news`,
  updatesGrab: `${API_NEWS_UDPATES_ROOT_URL}/live-updates`,
}
export const LEAGUE_STATISTIC_DEFINITIONS = {
  ranking : {
    displayName: 'Rank',
    color: '#ff073a',
    format: 'string',
    options: {key: 'rank'},
    hideDelta: false,
  },
  manager : {
    displayName: 'Manager',
    color: '#ff073a',
    format: 'string',
    options: {key: 'playerName'},
    hideDelta: false,
  },
  gwPoints : {
    displayName: 'Gameweek Points',
    color: '#ff073a',
    format: 'string',
    options: {key: 'gwPoints'},
    hideDelta: true,
  },
  totalPoints : {
    displayName: 'Total Points',
    color: '#ff073a',
    format: 'string',
    options: {key: 'totalPoints'},
    hideDelta: true,
  },
  hits : {
    displayName: 'Hits Taken',
    color: '#ff073a',
    format: 'string',
    options: {key: 'hits'},
    hideDelta: true,
  },
  chip : {
    displayName: 'Chip Played',
    color: '#ff073a',
    format: 'string',
    options: {key: 'chip'},
    hideDelta: true,
  },
  captaincy : {
    displayName: 'Captain',
    color: '#ff073a',
    format: 'string',
    options: {key: 'captaincy'},
    hideDelta: true,
  },
  vicecaptaincy : {
    displayName: 'Vice Captain',
    color: '#ff073a',
    format: 'string',
    options: {key: 'vicecaptaincy'},
    hideDelta: true,
  },
  playersPlayed : {
    displayName: 'Players Played',
    color: '#ff073a',
    format: 'string',
    options: {key: 'playersPlayed'},
    hideDelta: true,
  }, 
};
export const STATISTIC_DEFINITIONS = {
  current: {
    displayName: 'Current Gameweek',
    color: '#ff073a',
    format: 'string',
    options: {key: 'Current'},
    hideDelta: true,
  },
  mostCaptained: {
    displayName: 'Most\nCaptained',
    color: '#ff073a',
    format: 'string',
    options: {key: 'Current'},
  },
  mostTransferredIn: {
    displayName: 'Most\nBrought In',
    color: '#ff073a',
    format: 'string',
    options: {key: 'Current'},
  },
  topPerformer: {
    displayName: 'Best\nPlayer',
    color: '#ff073a',
    format: 'string',
    options: {key: 'Current'},
  },
  average: {
    displayName: 'Average\nGW Points',
    color: '#ff073a',
    format: 'int',
    options: {key: 'Current'},
  },
  highest: {
    displayName: 'Highest\nGW Points',
    color: '#ff073a',
    format: 'int',
    options: {key: 'Current'},
  },
  topPerformerPoints: {
    displayName: 'Points',
    color: '#ff073a',
    format: 'int',
    options: {key: 'Current'},
  },
  confirmed: {
    displayName: 'confirmed',
    color: '#ff073a',
    format: 'int',
    options: {key: 'confirmed'},
  },
  };

const definitions = Object.keys(STATISTIC_DEFINITIONS).reduce(
  (acc, statistic) => {
    const {options, ...config} = STATISTIC_DEFINITIONS[statistic];
    acc.options[statistic] = options;
    acc.configs[statistic] = config;
    return acc;
  },
  {options: {}, configs: {}}
);

const leagueDefinitions = Object.keys(LEAGUE_STATISTIC_DEFINITIONS).reduce(
  (acc, statistic) => {
    const {options, ...config} = LEAGUE_STATISTIC_DEFINITIONS[statistic];
    acc.options[statistic] = options;
    acc.configs[statistic] = config;
    return acc;
  },
  {options: {}, configs: {}}
);

export const D3_TRANSITION_DURATION = 300;

export const STATISTIC_CONFIGS = definitions.configs;
export const STATISTIC_OPTIONS = definitions.options;

export const LEAGUE_STATISTIC_CONFIGS = leagueDefinitions.configs;
export const LEAGUE_STATISTIC_OPTIONS = leagueDefinitions.options;

export const TABLE_STATISTICS_EXPANDED = Object.keys(LEAGUE_STATISTIC_DEFINITIONS);


export const LEVEL_ONE_STATISTICS_CL_HOME_MAP = {
  'overallAvg' : 'Overall Average',
  'overallHitsInclAvg' : 'With Hits',
  'top10KAvg' : 'T10K Average',
  'top10KHitsInclAvg' : 'With Hits',
}

export const LEAGUE_STATISTICS_MAP = {
  'mogwCounts' : 'Manager of Week', 
  'highestGWPoints' : 'Highest GW Points', 
  'highestNetValue' : 'Highest Net Value', 
  'highestWildcardPoints' : 'Highest Wildcard Points', 
  'highestFreehitPoints' : 'Highest Freehit Points',
  'highestBboostPoints' : 'Highest Bench Boost Points',
  'highest3xcPoints' : 'Highest Triple Captain Points',
  'highestBank' : 'Highest Bank Balance', 
  'highestEventTransfers' : 'Highest Transfer Count', 
  'highestEventTransfersCost' : 'Highest Transfer Hits', 
  'highestPointsOnBench' : 'Highest Bench Points', 
  'lowestGWPoints' : 'Lowest GW Points', 
  'lowestBank' : 'Lowest Bank Balance', 
  'lowestEventTransfers' : 'Lowest Transfer Count', 
  'highestEventTransfers' : 'Highest Transfer Count', 
  'lowestEventTransfersCost' : 'Lowest Transfer Hits', 
  'lowestPointsOnBench' : 'Lowest Bench Points', 
  'lowestNetValue' : 'Lowest Net Value', 
}

export const FIXTURE_DETAILS_MODAL_ITEMS = {
  'goalsScored' : 'Goals',
  'assists' : 'Assists',
  'saves' : 'Saves',
  'ownGoals' : 'Own Goals',
  'penaltiesMissed' : 'Penalties Missed',
  'penaltiesSaved' : 'Penalties Saved',
  'yellowCards' : 'Yellow Cards',
  'redCards' : 'Red Cards',
  'bonus' : 'Bonus',
  'bps' : 'Bonus Point System',
}

export const GAMEWEEK_DETAILS_LABEL_MAP = {
  'gameweek' : {
    label: 'Gameweek ',
    icon: StarIcon
  },
  'fixtures' : {
    label: 'Fixtures',
    icon: CalendarIcon
  },
  'justiceLeague' : {
    label: 'Justice League',
    icon: FlameIcon
  },
  'compareView' : {
    label: 'Compare',
    icon: MirrorIcon
  },
}

export const PAGE_SCREENS = {
  'news' : {
    label: 'News',
    icon: RssIcon
  },
  'fixtures' : {
    label: 'Fixtures',
    icon: CalendarIcon
  },
  'league' : {
    label: 'League',
    icon: FlameIcon
  },
  'compareView' : {
    label: 'Compare',
    icon: MirrorIcon
  },
  'statistics' : {
    label: 'Statistics',
    icon: ZapIcon
  },
}

export const LEVEL_TWO_STATISTICS_CL_HOME_MAP = {
  'bestAttacker' : 'Best ATT',
  'bestMidfielder' : 'Best MID',
  'bestDefender' : 'Best DEF',
  'bestGoalkeeper' : 'Best GK',
}

export const CLASSIC_LEAGUE_LIVE_TABLE_COL_MAP = {
  'ranking' : 'Rank',
  'manager' : 'Manager',
  'totalPoints' : 'Total',
  'gwPoints' : 'GW Points',
  'hits' : 'Hits',
  'chip' : 'Chip',
  'captaincy' : 'Captain',
  'vicecaptaincy' : 'Vice Captain',
  'playersPlayed' : 'Players Played'
}

export const LEVEL_ONE_STATISTICS_CL_HOME_LIST = Object.keys(LEVEL_ONE_STATISTICS_CL_HOME_MAP);

export const LEVEL_TWO_STATISTICS_CL_HOME_LIST = Object.keys(LEVEL_TWO_STATISTICS_CL_HOME_MAP);

export const LEVELONE_FPL_STATISTICS = [
  'mostCaptained',
  'mostTransferredIn',
  'topPerformer',
];

export const LEVELTWO_FPL_STATISTICS = [
  'average',
  'highest',
  'topPerformerPoints',
];

export const STATISTICS_THEME_MAP = {
  'current' : 'recovered',
  'mostCaptained' : 'active',
  'mostTransferredIn' : 'recovered',
  'topPerformer' : 'confirmed',
  'average' : 'confirmed',
  'highest' : 'recovered',
  'topPerformerPoints' : 'active',
}

export const STATISTICS_DATA_KEY_MAP = {
  'mostCaptained' : 'mostCaptained',
  'mostTransferredIn' : 'mostTransferredIn',
  'topPerformer' : 'highestScoringPlayer',
  'average' : 'avgScore',
  'highest' : 'highestScore',
  'topPerformerPoints' : 'highestScoringPlayerScore',
}

export const SPRING_CONFIG_NUMBERS = {clamp: true, precision: 1};