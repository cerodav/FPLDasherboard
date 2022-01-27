import Cell from './Cell';
import StateMetaCard from './StateMetaCard';
import { CLASSIC_LEAGUE_LIVE_TABLE_COL_MAP } from '../constants';
import classnames from 'classnames';
import React, { useState, useCallback, useRef } from 'react';
import { useSessionStorage } from 'react-use';

function Row({ data }) {
  const [showTeamDetails, setShowTeamDetails] = useState(false);
  const [sortData, setSortData] = useSessionStorage('districtSortData', {
    sortColumn: 'confirmed',
    isAscending: false,
    delta: false,
  });

  const rowElement = useRef();

  const handleRowClick = useCallback(() => {
    console.log('[ROW] Clicked', data);
    if (data.squad) {
      setShowTeamDetails(!showTeamDetails);
    }
  }, [showTeamDetails, data]);

  const tableColumns = CLASSIC_LEAGUE_LIVE_TABLE_COL_MAP;
  const rowData = data.dashboardTable
  return (
    <React.Fragment>
      {/* <div className={classnames('row')} onClick={handleRowClick} ref={rowElement}> */}
      <div className={classnames('row')} ref={rowElement}>
        {/* <div className="cell">
          <div className="state-name fadeInUp">
            {rowData.teamName.lower}
          </div>
        </div> */}
        <Cell key={'teamName'} data={rowData.teamName} columnName={'teamName'} />

        {Object.keys(tableColumns).map((columnName) => (
          <Cell key={columnName} data={rowData[columnName]} columnName={columnName} />
        ))}
      </div>

      {/* {(showTeamDetails) && (
        <React.Fragment>
          <div className="state-meta">
            <StateMetaCard className="recovery" title={`Squad`} playingPlayerList={data.live.squad} benchPlayerList={data.live.squad}
              differentialPlayerList={data.live.differentials} description={null} />
          </div>
        </React.Fragment>
      )} */}
    </React.Fragment>
  );
}

const isEqual = (prevProps, currProps) => {
};

export default React.memo(Row, isEqual);
