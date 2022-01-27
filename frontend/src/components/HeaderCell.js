import { LEAGUE_STATISTIC_DEFINITIONS } from '../constants';
import { toTitleCase } from '../utils/commonFunctions';
import { FilterIcon, InfoIcon } from '@primer/octicons-react';
import { useLongPress } from 'react-use';
import classnames from 'classnames';
import equal from 'fast-deep-equal';
import produce from 'immer';
import React from 'react';
import { CLASSIC_LEAGUE_LIVE_TABLE_COL_MAP } from '../constants';

function TableHeaderCell({handleSort, sortData, setSortData, columnName}) {
  console.log('[SORT]', sortData, columnName);
  const tableColumnKeys = CLASSIC_LEAGUE_LIVE_TABLE_COL_MAP;

  return (
    <div className="cell heading" onClick={handleSort.bind(this, columnName)}>
      {(sortData.sortColumn == columnName) && (
        <div className={classnames('sort-icon', {invert: sortData.isAscending})}>
          <FilterIcon size={10} />
        </div>
      )}
      <div>{tableColumnKeys[columnName]}</div>
    </div>
  );
}

const isTableHeaderCellEqual = (prevProps, currProps) => {
  if (!equal(prevProps.sortData, currProps.sortData)) {
    return false;
  } else {
    return true;
  }
};

export default React.memo(TableHeaderCell, isTableHeaderCellEqual);
