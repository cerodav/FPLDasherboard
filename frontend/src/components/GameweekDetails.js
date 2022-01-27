import { GAMEWEEK_DETAILS_LABEL_MAP } from '../constants'
import React, { useState, lazy, Suspense } from 'react';
import { useTrail, animated, config } from 'react-spring';
import classnames from 'classnames';
import { CalendarIcon } from '@primer/octicons-react';
import createClass from 'create-react-class';
import {useLocalStorage, useSessionStorage} from 'react-use';

const GeneralLiveStatistics = lazy(() => import('./GeneralLiveStatistics'));
const Fixtures = lazy(() => import('./Fixtures'));

function isAnyVisible(buttonStatusMap) {
    for (const key of Object.keys(buttonStatusMap)) {
        if (buttonStatusMap[key].isInfoVisible) {
            return true;
        }
    }
    return false;
}

function closeAllVisible(buttonStatusMap, exceptDataType) {
    for (const key of Object.keys(buttonStatusMap)) {
        if (buttonStatusMap[key].isInfoVisible && key != exceptDataType) {
            buttonStatusMap[key].setIsInfoVisible.bind(this, !buttonStatusMap[key].isInfoVisible);
        }
    }
}

var IconChoice = createClass({
    render: function() {
        return <this.props.component.slug size={14}/>
    }
});

function GameweekDetails({ data, stats }) {
    const validDataTypes = Object.keys(GAMEWEEK_DETAILS_LABEL_MAP);
    var buttonStatusMap = {};
    // var lastActivatedScreen = validDataTypes[0];
    const collectedDataTypes = Object.keys(data);
    const gameweekNumber = data.gameweek.gameweekNumber;

    // For use of Fixtures
    const fixturesVisibilityControl = useState(false);
    buttonStatusMap['fixtures'] = {
        isInfoVisible : fixturesVisibilityControl[0],
        setIsInfoVisible : fixturesVisibilityControl[1],
    }

    // For use of Gameweek
    const gwVisibilityControl = useState(true);
    buttonStatusMap['gameweek'] = {
        isInfoVisible : gwVisibilityControl[0],
        setIsInfoVisible : gwVisibilityControl[1],
    }

    // function setViewScreen(screenName) {
    //     lastActivatedScreen = screenName;
    //     console.log('[CLICK]', lastActivatedScreen);
    // }

    const [lastActivatedScreen, setViewScreen] = useSessionStorage(
        'gwDetailsActiveScreen',
        validDataTypes[0]
    );

    return (
        <React.Fragment>
            <div className="pills" style={{justifyContent:'flex-start', marginBottom:'1.5rem'}}>
                {validDataTypes.map((option) => (
                    <button
                        key={option}
                        type="button"
                        className={classnames({ selected: lastActivatedScreen === option })}
                        onClick={() => setViewScreen(option)}
                    >
                        <IconChoice component={{slug:GAMEWEEK_DETAILS_LABEL_MAP[option].icon}} />&nbsp;&nbsp;{option == 'gameweek' ? GAMEWEEK_DETAILS_LABEL_MAP[option].label + gameweekNumber : GAMEWEEK_DETAILS_LABEL_MAP[option].label}
                    </button>
                ))}
            </div>
            {
                ((lastActivatedScreen == 'gameweek') && stats) && (
                    <Suspense fallback={<div />}>
                        <GeneralLiveStatistics data={stats}/>
                    </Suspense>
                )
            }
            {
                ((lastActivatedScreen == 'fixtures') && data.fixtures) && (
                    <Suspense fallback={<div />}>
                        <Fixtures data={data.fixtures}/>
                    </Suspense>
                )
            }
        </React.Fragment>
    )
}

export default GameweekDetails;