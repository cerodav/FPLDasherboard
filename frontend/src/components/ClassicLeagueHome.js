import classnames from 'classnames';
import React, { lazy, Suspense, useRef, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { useLocalStorage, useSessionStorage, useWindowSize } from 'react-use';
import { PAGE_PREFIXES, FPL_BACKEND_CALL, GAMEWEEK_DETAILS_LABEL_MAP, PAGE_SCREENS } from '../constants';
import { getLocationPathPostPrefix } from '../utils/commonFunctions'
import useIsVisible from '../hooks/useIsVisible';
import useStickySWR from '../hooks/useStickySWR';
import { fetcher } from '../utils/commonFunctions';
import createClass from 'create-react-class';

const Table = lazy(() => import('./Table'));
const GameweekDetails = lazy(() => import('./GameweekDetails'));
const GeneralLiveStatistics = lazy(() => import('./GeneralLiveStatistics'));
const Fixtures = lazy(() => import('./Fixtures'));
const NewsPage = lazy(() => import('./NewsPage'));
const CompareView = lazy(() => import('./CompareView'));
const LeagueStatistics = lazy(() => import('./LeagueStatistics'));

var IconChoice = createClass({
    render: function() {
        return <this.props.component.slug size={14}/>
    }
});

function ClassicLeagueHome() {
    // const location = useLocation();
    // const locationPrefix = PAGE_PREFIXES.ClassicLeagueHomePage
    // const leagueId = getLocationPathPostPrefix(location.pathname, locationPrefix)
    const leagueId = 1143965;

    const {data:latestGeneralStatistics} = useStickySWR( FPL_BACKEND_CALL.latestStatistics, fetcher,
        {
            revalidateOnMount: true,
            refreshInterval: 100000000000,
        }
    );

    const {data:newsGrabData} = useStickySWR( FPL_BACKEND_CALL.newsGrab, fetcher,
        {
            revalidateOnMount: true,
            refreshInterval: 100000000000,
        }
    );

    const {data:liveUpdatesGrabData} = useStickySWR( FPL_BACKEND_CALL.updatesGrab, fetcher,
        {
            revalidateOnMount: true,
            refreshInterval: 10000000,
        }
    );

    const {data:liveClassicLeagueStandings} = useStickySWR( `${FPL_BACKEND_CALL.liveClassicLeagueStandings}` + leagueId, fetcher,
        {
            revalidateOnMount: true,
            refreshInterval: 100000000000,
        }
    );

    const {data:leagueStatistics} = useStickySWR( `${FPL_BACKEND_CALL.leagueStatistics}` + leagueId, fetcher,
        {
            revalidateOnMount: true,
            refreshInterval: 100000000000,
        }
    );

    const {data:compareStatistics} = useStickySWR( `${FPL_BACKEND_CALL.compareStatistics}` + leagueId, fetcher,
        {
            revalidateOnMount: true,
            refreshInterval: 100000000000,
        }
    );

    const {data:gameweekDetails} = useStickySWR( `${FPL_BACKEND_CALL.gameweekDetails}`, fetcher,
        {
            revalidateOnMount: true,
            refreshInterval: 100000000000,
        }
    );

    const homeRightElement = useRef();

    const validDataTypes = Object.keys(GAMEWEEK_DETAILS_LABEL_MAP);
    const pageScreens = Object.keys(PAGE_SCREENS);
    const gameweekNumber = gameweekDetails ? gameweekDetails.gameweek.gameweekNumber : null;
    const [lastActivatedScreen, setViewScreen] = useSessionStorage(
        'activeScreen',
        pageScreens[0]
    );
    // console.log('[D]', leagueStatistics)
    return (
        <React.Fragment>

            <div className="Home">
                <div className={classnames('home-left expanded')}>
                    {
                        <div className="pills" style={{justifyContent:'flex-start'}}>
                            {pageScreens.map((option) => (
                                <button
                                    key={option}
                                    type="button"
                                    className={classnames({ selected: lastActivatedScreen === option })}
                                    onClick={() => setViewScreen(option)}
                                >
                                    <IconChoice component={{slug:PAGE_SCREENS[option].icon}} />&nbsp;&nbsp;{PAGE_SCREENS[option].label}
                                </button>
                            ))}
                        </div>
                    }
                    {
                        (!gameweekDetails) && (
                            <div className="header" style={{marginTop: '1.5rem'}}>
                                <Suspense fallback={<div />}>
                                <div className="Banner">
                                    <span className='snippet'>Loading...</span><br />
                                    <span className='snippet'>Fetching Gameweek data</span>
                                </div>
                                </Suspense>
                            </div>
                        )
                    }
                    {
                        ((lastActivatedScreen == 'news') && newsGrabData) && (
                            <Suspense fallback={<div />}>
                                <NewsPage data={newsGrabData}/>
                            </Suspense>
                        )
                    }
                    {
                        ((lastActivatedScreen == 'gameweek') && latestGeneralStatistics) && (
                            <Suspense fallback={<div />}>
                                <GeneralLiveStatistics data={latestGeneralStatistics}/>
                            </Suspense>
                        )
                    }
                    {
                        ((lastActivatedScreen == 'fixtures') && gameweekDetails) && (
                            <Suspense fallback={<div />}>
                                <Fixtures data={gameweekDetails.fixtures}/>
                            </Suspense>
                        )
                    }
                    {
                        ((lastActivatedScreen == 'compareView') && liveClassicLeagueStandings) && (
                            <Suspense fallback={<div />}>
                                <CompareView data={liveClassicLeagueStandings} compareStatistics={compareStatistics}/>
                            </Suspense>
                        )
                    }
                    {
                        ((lastActivatedScreen == 'statistics') && leagueStatistics) && (
                            <Suspense fallback={<div />}>
                                <LeagueStatistics data={leagueStatistics}/>
                            </Suspense>
                        )
                    }
                    {
                        (!liveClassicLeagueStandings && leagueId) && (
                            <div className="header" style={{marginTop: '1.5rem'}}>
                                <Suspense fallback={<div />}>
                                <div className="Banner">
                                    <span className='snippet'>Loading...</span><br />
                                    <span className='snippet'>Fetching data for League#{leagueId}</span>
                                </div>
                                </Suspense>
                            </div>
                        )
                    }
                    {
                        (lastActivatedScreen == 'league' && liveClassicLeagueStandings) && (
                            <Suspense fallback={<div />}>
                                <Table data={liveClassicLeagueStandings}/>
                            </Suspense>
                        )
                    }
                </div>
                <div className={classnames('home-right expanded')} ref={homeRightElement}>
                </div>
            </div>
        </React.Fragment>
        );
    }

    export default ClassicLeagueHome;
