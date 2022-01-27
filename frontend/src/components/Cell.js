import { SPRING_CONFIG_NUMBERS, LEAGUE_STATISTIC_CONFIGS } from '../constants.js';
import { getTableStatistic } from '../utils/commonFunctions';
import classnames from 'classnames';
import React from 'react';
import { animated } from 'react-spring';

function getDeltaText(hideDelta, upperData) {
  if (hideDelta) {
    return ''
  }
  else {
    if (isNaN(upperData)) {
      return upperData;
    }
    else {
      if (upperData > 0) {
        return "↑" + upperData;
      }
      else {
        if (upperData == 0) {
          return "-";
        }
        else {
          return "↓" + upperData*-1;
        }
      }
    }
  }
}

function getDeltaClassName(hideDelta, upperData) {
  if (isNaN(upperData)) {
    return 'is-deceased';
  }
  let deltaClassName = 'is-recovered'
  if (!hideDelta && upperData < 0) {
    deltaClassName = 'is-confirmed'
  }
  if (!hideDelta && upperData == 0) {
    deltaClassName = 'is-deceased'
  }
  return deltaClassName
}

const Cell = ({data, columnName}) => {

  const hideDelta = data.upper.length == 0 || data.upper == null;
  const deltaClassName = getDeltaClassName(hideDelta, data.upper);
  const deltaText = getDeltaText(hideDelta, data.upper);
  
  return (
    <div className="cell statistic">
      {(!hideDelta) && (
        <animated.div className={classnames('delta', `${deltaClassName}`)}>
          {deltaText}
        </animated.div>
      )}

      <animated.div className={classnames('total', getClassForColumn(columnName, data.lower))} >
        {data.lower}
      </animated.div>
    </div>
  );
};

function getClassForColumn(columnName, lowerData)  {
  if (columnName == 'hits') {
    return (lowerData >= 0 ? `is-confirmed` : `is-recovered`);
  }
  if (columnName == 'chip') {
    return (lowerData != '-' ? `is-recovered` : `is-deceased`);
  }
  return `is-deceased`;
};

const isCellEqual = (prevProps, currProps) => {
  // if (!equal(prevProps.data?.total, currProps.data?.total)) {
  //   return false;
  // }
  // if (!equal(prevProps.data?.delta, currProps.data?.delta)) {
  //   return false;
  // }
  // if (!equal(prevProps.isPerMillion, currProps.isPerMillion)) {
  //   return false;
  // }
  // return true;
};

export default React.memo(Cell, isCellEqual);
