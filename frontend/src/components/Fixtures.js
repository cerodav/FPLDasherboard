import React, { useMemo, useState, useEffect } from 'react';
import { Button, Modal } from 'react-bootstrap';
import classnames from 'classnames';
import Moment from 'moment';
import { FIXTURE_DETAILS_MODAL_ITEMS } from '../constants';
import { useTransition, animated } from 'react-spring';

function importAll(r) {
    var dataMap = {};
    for (const n of r.keys()) {
        const id = n.replace('./', '').replace('.png', '')
        dataMap[id] = r(n);
    }
    return dataMap
  }

function getLocalDate(dtString) {
    const dt = new Date(dtString);
    return Moment(dt.toString()).format("MMMM Do YYYY, h:mm a");
}

function getLogoId(teamId) {
    return 'badge_' + teamId + '_40'
}

function Fixtures({ data }) {
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
    var itemToShow = data[0];
    var defaultShowDetails = new Array(data.length).fill(false);
    const teamLogo = importAll(require.context('../images/teamLogo/', false, /\.(png)$/));
    const [show, setShow] = useState(false);
    const [selectedFixture, setSelectedFixture] = useState(null);
    const [showDetails, setShowDetails] = useState(defaultShowDetails);
    const handleClose = () => setShow(false);
    function handleShow(itemIndex) {         
        let currentShowState = [...showDetails];
        currentShowState[itemIndex] = (!currentShowState[itemIndex])
        setShowDetails(currentShowState);
    }
    // const transition = useTransition(
    //     showChildren ? children : [],
    //     item => item.text,
    //     {
    //       from: { opacity: 0, transform: 'scaleY(0)', maxHeight: '0px' },
    //       enter: { opacity: 1, transform: 'scaleY(1)', maxHeight: '1000px' },
    //       leave: { opacity: 0, transform: 'scaleY(0)', maxHeight: '0px' }
    //     }
    // );

    function renderModalTitle() {
        if (selectedFixture != null) {
            const selectedFixtureData = data[selectedFixture];
            return (
                <div className="board-item-title">
                    {selectedFixtureData.teamHome.name}
                    <img src={teamLogo[getLogoId(selectedFixtureData.teamHomeId)].default} />
                    <div className="score-box">{selectedFixtureData.teamHomeScore}</div>
                    <div className="score-box">{selectedFixtureData.teamAwayScore}</div>
                    <img src={teamLogo[getLogoId(selectedFixtureData.teamAwayId)].default} />
                    {selectedFixtureData.teamAway.name}
                </div>
            )
        }
        else {
            return (<div className="board-item-title"></div>);
        }
    }

    function isThereData(dataSection) {
        if (dataSection) {
            if (dataSection.home.length > 0 || dataSection.away.length > 0) {
                return true;
            }
        }
        return false;
    }

    function renderModalBody(index) {
        const selectedFixtureData = data[index];
        const fixtureDatapoints = Object.keys(selectedFixtureData);
        var datapointsToShow = [];
        Object.keys(FIXTURE_DETAILS_MODAL_ITEMS).map((item) => {
            if (isThereData(selectedFixtureData[item])) {
                datapointsToShow.push(item);
            }
        })
        return (
            <div className="board-item-body">
            {
                datapointsToShow.map((item, index) => (
                    <div key={index} className="board-item-body-section">
                        <div className="body-section-heading">
                            {FIXTURE_DETAILS_MODAL_ITEMS[item]}
                        </div>
                        <div className="body-section-body">
                            <div className="body-section-body-home">
                                {
                                    selectedFixtureData[item].home.map((event, index) => ((item != 'bps' || ((item == 'bps' && index < 5))) && (
                                        <><div key={event.webName} className="section-body-item">{event.webName}&nbsp;&nbsp;<div className="numberCircle">{event.value}</div></div><br /></>
                                    )))
                                }
                            </div>
                            <div className="body-section-body-away">
                                {
                                    selectedFixtureData[item].away.map((event, index) => ((item != 'bps' || ((item == 'bps' && index < 5)))  && (
                                        <><div key={event.webName} className="section-body-item">{event.webName}&nbsp;&nbsp;<div className="numberCircle">{event.value}</div></div><br /></>
                                    )))
                                }
                            </div>
                        </div>    
                    </div>
                ))
            }   
            </div>
        )
    }
  
    return (
        <React.Fragment>
            <div className="Board" style={{marginTop:'1.5rem'}}>
                <div className="FixturesColumn1">
                {
                    data.map((item, index) => ((index % 2 == 1) && (
                        <div key={index} className={classnames('board-item', 'fadeInUp', {expanded : showDetails[index]})} style={trail[index]} onClick={() => handleShow(index)}>
                            <div className="board-item-title">
                                {item.teamHome.name}
                                <img src={teamLogo[getLogoId(item.teamHomeId)].default} />
                                <div className="score-box">{item.teamHomeScore}</div>
                                <div className="score-box">{item.teamAwayScore}</div>
                                <img src={teamLogo[getLogoId(item.teamAwayId)].default} />
                                {item.teamAway.name}
                            </div>
                            <div className="board-item-footer">
                                {getLocalDate(item.kickoffTimeUTC)}
                            </div>
                            {(showDetails[index]) && (
                                <div className="board-item-additional-info fadeInUp" style={trail[0]}>
                                    {renderModalBody(index)}
                                </div>
                            )}
                        </div>
                    )))
                }
                </div>
                <div className="FixturesColumn1">
                {
                    data.map((item, index) => ((index % 2 == 0) && (
                        <div key={index} className={classnames('board-item', 'fadeInUp', {expanded : showDetails[index]})} style={trail[index]} onClick={() => handleShow(index)}>
                            <div className="board-item-title">
                                {item.teamHome.name}
                                <img src={teamLogo[getLogoId(item.teamHomeId)].default} />
                                <div className="score-box">{item.teamHomeScore}</div>
                                <div className="score-box">{item.teamAwayScore}</div>
                                <img src={teamLogo[getLogoId(item.teamAwayId)].default} />
                                {item.teamAway.name}
                            </div>
                            <div className="board-item-footer">
                                {getLocalDate(item.kickoffTimeUTC)}
                            </div>
                            {(showDetails[index]) && (
                                <div className="board-item-additional-info fadeInUp" style={trail[0]}>
                                    {renderModalBody(index)}
                                </div>
                            )}
                        </div>
                    )))
                }
                </div>
            </div>
        </React.Fragment>
    )
}

export default Fixtures;