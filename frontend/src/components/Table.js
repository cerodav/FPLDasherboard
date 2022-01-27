import TableHeaderCell from './HeaderCell';
import { FilterIcon, HubotIcon } from '@primer/octicons-react';
import classnames from 'classnames';
import produce from 'immer';
import {animated} from 'react-spring';
import React, { useCallback, lazy } from 'react';
import { useSessionStorage } from 'react-use';
import { CLASSIC_LEAGUE_LIVE_TABLE_COL_MAP } from '../constants'

const Row = lazy(() => import('./Row'));

function getPlayersPlayedRatio(playersPlayedString) {
    const ab = playersPlayedString.split('/')
    return parseFloat(ab[0])/parseFloat(ab[1])
}

function Table({data}) {
    const tabularData = data;
    const [sortData, setSortData] = useSessionStorage('sortData', {
        sortColumn: 'ranking',
        isAscending: true,
    });

    const handleSortClick = useCallback((columnName) => {
        if (sortData.sortColumn !== columnName) {
            setSortData(produce(sortData, (draftSortData) => {
                draftSortData.sortColumn = columnName;
            }));
        } else {
        setSortData(produce(sortData, (draftSortData) => {
                draftSortData.isAscending = !sortData.isAscending;
            }));
        }
    }, [sortData, setSortData]);

    const sortingFunction = ((teamA, teamB) => {
        const aData = teamA['dashboardTable'];
        const bData = teamB['dashboardTable'];
        if (sortData.sortColumn == 'playersPlayed') {
            return sortData.isAscending
            ? getPlayersPlayedRatio(aData[sortData.sortColumn]['lower']) - getPlayersPlayedRatio(bData[sortData.sortColumn]['lower'])
            : getPlayersPlayedRatio(bData[sortData.sortColumn]['lower']) - getPlayersPlayedRatio(bData[sortData.sortColumn]['lower']);
        }
        else {
            return sortData.isAscending
            ? aData[sortData.sortColumn]['lower'] - bData[sortData.sortColumn]['lower']
            : bData [sortData.sortColumn]['lower'] - aData[sortData.sortColumn]['lower'];  
        }
    });

    const tableColumnKeys = CLASSIC_LEAGUE_LIVE_TABLE_COL_MAP;
    const leagueName = tabularData.info.name;
    return (
        <React.Fragment>
            <div className="table-container" style={{marginTop:'1.5rem'}}>
                <div className="table fadeInUp" style={{ gridTemplateColumns: `repeat(${Object.keys(tableColumnKeys).length + 1}, auto)`,}}>
                    <div className="row heading">
                        <div className="cell heading">
                            <div>Team</div>
                            { (sortData.sortColumn === 'teamName') && (
                                <div className={classnames('sort-icon', {invert: sortData.isAscending,})}>
                                    <FilterIcon size={10} />
                                </div>
                            )}
                        </div>
                        { Object.keys(tableColumnKeys).map((columnName) => (
                            <TableHeaderCell key={columnName} handleSort={handleSortClick.bind(this, columnName)} sortData={sortData} setSortData={setSortData} columnName={columnName} />
                        ))}
                    </div>

                    { tabularData['members'].slice().sort((a, b) => sortingFunction(a, b)).map((entry, i) => {
                        return (
                            <Row key={i} data={entry}/>
                        );
                    })}
                </div>
            </div>
        </React.Fragment>
    );
}

const isEqual = (prevProps, currProps) => {
};

export default React.memo(Table, isEqual);
