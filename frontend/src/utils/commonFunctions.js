import { LEAGUE_STATISTIC_CONFIGS, LEAGUE_STATISTIC_DEFINITIONS, LEAGUE_STATISTIC_OPTIONS } from '../constants';
  
export const getLocationPathPostPrefix = (fullPath, prefixPath) => {
    if (fullPath == undefined || prefixPath == undefined || fullPath.length == 0 || prefixPath.length == 0) {
        return null
    }
    else {
        return fullPath.substring(fullPath.indexOf(prefixPath) + prefixPath.length)
    }
};
  
export const fplFormatNumber = (value, isDelta) => {
    if (!isDelta) {
        return value
    }
    else {
        return parseInt(value) > 0 ? '+' + value : '-' + value;
    }
};
 
export const capitalize = (s) => {
    if (typeof s !== 'string') return '';
    return s.charAt(0).toUpperCase() + s.slice(1);
};
  
export const toTitleCase = (str) => {
    return str.replace(/\w\S*/g, function (txt) {
    return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
};
  
export const getFPLStatistic = (data, key, isUpper=false) => {
    var selectionIdx = 0;
    if (isUpper) {
        return data[key]['upper']
    }
    return data[key]['lower']
}
  
export const fetcher = (url) => {
    return fetch(url).then((response) => {
        return response.json();
    });
};

export const getTableStatistic = (data, statistic, isPerMillion, lastUpdatedTT) => {
    const total = 0;
    const delta = 0;
    return {total, delta};
};
  