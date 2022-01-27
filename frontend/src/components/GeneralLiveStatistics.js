import { LEVEL_ONE_STATISTICS_CL_HOME_MAP, LEVEL_TWO_STATISTICS_CL_HOME_MAP } from '../constants'
import React, { lazy } from 'react';
const QuadVerticalTiles = lazy(() => import('./QuadVerticalTiles'));

function formatDataForQuadVerticalTiles(data) {
    const levelOneTilesData = []
    const levelTwoTilesData = []
    const top10KHitsAvg = data.top10KHitsAvg;
    const overallHitsAvg = data.overallHitsAvg;
    Object.keys(data).forEach(key => {
        if (key.toUpperCase().indexOf('GAMEWEEK') !== -1) {
            return;
        }
        if (key in LEVEL_ONE_STATISTICS_CL_HOME_MAP) {
            if (key.toUpperCase().indexOf('HITSAVG') !== -1) {
                return;    
            }
            if (key.toUpperCase().indexOf('HITSINCLAVG') !== -1) {
                let upperData = null;
                if (key.toUpperCase().indexOf('TOP10K') !== -1) {
                    upperData = top10KHitsAvg
                }
                if (key.toUpperCase().indexOf('OVERALL') !== -1) {
                    upperData = overallHitsAvg
                }
                levelOneTilesData.push({
                    title : LEVEL_ONE_STATISTICS_CL_HOME_MAP[key],
                    upper : upperData,
                    lower : data[key]
                })    
            }
            else {
                levelOneTilesData.push({
                    title : LEVEL_ONE_STATISTICS_CL_HOME_MAP[key],
                    upper : null,
                    lower : data[key]
                })    
            }
        }
        if (key in LEVEL_TWO_STATISTICS_CL_HOME_MAP) {
            levelTwoTilesData.push({
                title : LEVEL_TWO_STATISTICS_CL_HOME_MAP[key],
                upper : String(data[key].totalPoints) + ' pts',
                lower : data[key].name
            })    
        }
    });
    return [levelOneTilesData, levelTwoTilesData]
}

function GeneralLiveStatistics({ data }) {
    const formattedData = formatDataForQuadVerticalTiles(data);
    // console.log('[STATS-DAT]', formattedData[0], formattedData[1], data);

    return (
        <React.Fragment>
            <QuadVerticalTiles data={formattedData[0]} theme={`is-active background-active`}/>
            <QuadVerticalTiles data={formattedData[1]} theme={`is-recovered background-recovery`}/>
        </React.Fragment>
    )
}

export default GeneralLiveStatistics;