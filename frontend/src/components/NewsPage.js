import React, { useMemo, useState } from 'react';
import { Button, Modal } from 'react-bootstrap';
import classnames from 'classnames';
import Moment from 'moment';
import { FIXTURE_DETAILS_MODAL_ITEMS } from '../constants'
import { XCircleFillIcon } from '@primer/octicons-react';

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

function NewsPage({ data }) {
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
    // const teamLogo = importAll(require.context('../images/teamLogo/', false, /\.(png)$/));
    const [show, setShow] = useState(false);
    const [selectedFixture, setSelectedFixture] = useState(null);
    const handleClose = () => setShow(false);
    function handleShow(itemIndex) { 
        setSelectedFixture(itemIndex);
        setShow(true); 
    }

    function renderModalTitle() {
        // console.log('[X MTITLE]', selectedFixture)
        if (selectedFixture != null) {
            const selectedFixtureData = data[selectedFixture];
            return (
                <div className="board-item-title">
                    {selectedFixtureData.teamHome.name}
                    
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

    function renderModalBody() {
        // console.log('[X MBODY]', selectedFixture)
        if (selectedFixture != null) {
            const selectedFixtureData = data[selectedFixture];
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
                                        selectedFixtureData[item].home.map((event) => (
                                            <div key={event.webName} className="section-body-item">{event.webName}&nbsp;&nbsp;{'(' + event.value + ')'}</div>
                                        ))
                                    }
                                </div>
                                <div className="body-section-body-away">
                                    {
                                        selectedFixtureData[item].away.map((event) => (
                                            <div key={event.webName} className="section-body-item">{event.webName}&nbsp;&nbsp;{'(' + event.value + ')'}</div>
                                        ))
                                    }
                                </div>
                            </div>    
                        </div>
                    ))
                }   
                </div>
            )
        }
        else {
            return (<div className="board-item-body"></div>);
        }
    }
    console.log('[DA]', data);
    return (
        <React.Fragment>
            <div className="NewsPage" style={{marginTop:'1.5rem'}}>
                <div className="NewsPageColumn1" style={{marginTop:'1.5rem'}}>
                {
                    data.map((item, index) => ((index % 2 == 1) && (
                        <div key={index} className={classnames('newspage-item', 'fadeInUp')} style={trail[index]}>
                            <div className="newspage-item-title">
                                {item.title}
                            </div>
                            <div className="newspage-item-body">
                                {item.content.map(str => <p>{str}</p>)}
                            </div>
                            <div className="newspage-item-footer">
                                {getLocalDate(item.timestamp)}
                            </div>
                        </div>
                    )))
                }
                </div>
                <div className="NewsPageColumn2" style={{marginTop:'1.5rem'}}>
                {
                    data.map((item, index) => ((index % 2 == 0) && (
                        <div key={index} className={classnames('newspage-item', 'fadeInUp')} style={trail[index]}>
                            <div className="newspage-item-title">
                                {item.title}
                            </div>
                            <div className="newspage-item-body">
                                {item.content.map(str => <p>{str}</p>)}
                            </div>
                            <div className="newspage-item-footer">
                                {getLocalDate(item.timestamp)}
                            </div>
                        </div>
                    )))
                }
                </div>
                
                <Modal show={show} onHide={handleClose} style={{overlay: {zIndex: 1000}}}>
                    <Modal.Header>
                        <Modal.Title>
                            {/* <Button variant="secondary" onClick={handleClose}>
                                Close
                            </Button> */}
                            <div onClick={handleClose} style={{textAlign:'end'}}>
                                <XCircleFillIcon size={14} />
                            </div>
                            {renderModalTitle()}
                        </Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        {renderModalBody()}
                    </Modal.Body>
                    <Modal.Footer>
                    </Modal.Footer>
                </Modal>
            </div>
        </React.Fragment>
    )
}

export default NewsPage;