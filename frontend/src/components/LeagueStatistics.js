import React, { lazy, useMemo } from 'react';
import { LEAGUE_STATISTICS_MAP } from '../constants'
import classnames from 'classnames';
const MiniStatTable = lazy(() => import('./MiniStatTable'));
// const Timeseries = lazy(() => import('./Timeseries'));

function LeagueStatistics({ data }) {
    const validStats = Object.keys(LEAGUE_STATISTICS_MAP);
    console.log('[STATS]', data);
    return (
        <React.Fragment>
            <div className={classnames('stats-table-container', 'fadeInUp')} style={{marginTop: '1.5rem', animationDelay: `${50}ms`}}>
            {
                validStats.map((statType, index) => ((data[statType].length != 0) && (
                    <MiniStatTable title={LEAGUE_STATISTICS_MAP[statType]} data={data[statType]} key={statType}/>
                )))
            }
            </div>
        </React.Fragment>
    )
}

export default LeagueStatistics;