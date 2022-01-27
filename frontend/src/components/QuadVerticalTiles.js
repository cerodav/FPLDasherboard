import classnames from 'classnames';
import React, {useMemo} from 'react';
import {animated} from 'react-spring';

function PureLevelItem({data}) {

  return (
    <React.Fragment>
      <h5>{data.title}</h5>
      <animated.h4>
        {data.upper ? (`${data.upper}`) : ('\u00A0')}
      </animated.h4>
      <animated.h1>
        {data.lower ? (`${data.lower}`) : ('\u00A0')}
      </animated.h1>
    </React.Fragment>
  );
}

const LevelItem = React.memo(PureLevelItem);

function QuadVerticalTiles({data, theme}) {
  const trail = useMemo(() => {
    const styles = [];
    data.map((_, index) => {
      styles.push({
        animationDelay: `${index * 50}ms`,
      });
      return null;
    });
    return styles;
  }, []);
  
  return (
    <div className="Level">
      {data.map((item, index) => (
        <animated.div key={index} className={classnames('level-item', `${theme}`, 'fadeInUp')} style={trail[index], {marginTop:'1.5rem'}}>
          <LevelItem
            data={item}
          />
        </animated.div>
      ))}
    </div>
  );
}

const isEqual = (prevProps, currProps) => {
  // console.log('[IS-EQ-LEVELS]', prevProps, currProps)
};

export default React.memo(QuadVerticalTiles, isEqual);
