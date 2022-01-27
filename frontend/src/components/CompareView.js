import { ArrowUpIcon, ArrowDownIcon } from '@primer/octicons-react';
import { GAMEWEEK_DETAILS_LABEL_MAP } from '../constants'
import React, { useState, lazy, Suspense, useEffect } from 'react';
import { useTrail, animated, config } from 'react-spring';
import classnames from 'classnames';
import { CalendarIcon } from '@primer/octicons-react';
import createClass from 'create-react-class';
import {useLocalStorage, useSessionStorage} from 'react-use';

const Dropdown = lazy(() => import('./Dropdown'));
const TeamPlot = lazy(() => import('./TeamPlot'));
const LineChart = lazy(() => import('./LineChart'));

function generateDataForDropDown(data) {
    var ddData = []
    data.members.forEach(element => {
        ddData.push({
            key : element.info.id,
            value : element.info.userName,
            label : element.info.name
        })
    });
    return ddData;
}

function getRandomInt(max) {
    return Math.floor(Math.random() * max);
}

function getTeamFromUsername(data, uName) {
    for (let team of data.members) {
        if (team.info.userName == uName) {
            return team
        }
    }
}

function generatePlotParameters() {
    var ddData = []
    var interestedColumns = [
        {
            'label':'Total Points',
            'value':'total_points'
        },
        {
            'label':'Bank',
            'value':'bank'
        },
        {
            'label':'Transfers',
            'value':'event_transfers'
        },
        {
            'label':'Transfer Cost',
            'value':'event_transfers_cost'
        },
        {
            'label':'Overall Rank',
            'value':'overall_rank'
        },
        {
            'label':'GW Points',
            'value':'points'
        },
        {
            'label':'GW Points on Bench',
            'value':'points_on_bench'
        },
        {
            'label':'Squad Value',
            'value':'value'
        }];
        
    interestedColumns.forEach(element => {
        ddData.push({
            key : element.value,
            value : element.value,
            label : element.label
        })
    });
    return ddData;
}

function generatePlayerLocationMap(squad) {
    var locationMap = {};
    locationMap['Goalkeeper'] = [];
    locationMap['Defender'] = [];
    locationMap['Midfielder'] = [];
    locationMap['Attacker'] = [];
    locationMap['Bench'] = [];
    squad.forEach((p) => {
        if (p.status == "Playing") {
            locationMap[p.position].push(p);
        }
        else {
            locationMap['Bench'].push(p);
        }
        
    });
    return locationMap;
}

function getAllStats(name, compareStatistics, data) {
    var res = {};
    res['compare'] = compareStatistics[name];
    res['live'] = getTeamFromUsername(data, name);
    return res;
}

var IconChoice = createClass({
    render: function() {
        return <this.props.component.slug size={14}/>
    }
});

function CompareView({ data, compareStatistics }) {

    const [plotParameters, setPlotParameters] = useState(generatePlotParameters());
    const [selectedPlotParameter, setSelectedPlotParameter] = useState(plotParameters[0].value);
    const [dropdownData, setDropdownData] = useState(generateDataForDropDown(data));
    var [selectedTeamAValue, setSelectedTeamAValue ] = useState(dropdownData[0].value);
    var [selectedTeamBValue, setSelectedTeamBValue] = useState(dropdownData[1].value);
    var [teamALocMap, setTeamALocMap ] = useState(generatePlayerLocationMap(data.members[0].live.squad));
    var [teamBLocMap, setTeamBLocMap] = useState(generatePlayerLocationMap(data.members[1].live.squad));
    var [teamACompStat, setTeamACompStat ] = useState(getAllStats(selectedTeamAValue, compareStatistics, data));
    var [teamBCompStat, setTeamBCompStat] = useState(getAllStats(selectedTeamBValue, compareStatistics, data));
    var [lineChartOptions, setLineChartOptions] = useState(generateLineChartOptions(getIndexTs(teamBCompStat, selectedPlotParameter), 
                                                            getValueTs(teamACompStat, selectedPlotParameter), 
                                                            getValueTs(teamBCompStat, selectedPlotParameter)));
    
    function teamAChangeHandler(event) {
        setSelectedTeamAValue(event.target.value);
        setTeamALocMap(generatePlayerLocationMap(getTeamFromUsername(data, event.target.value).live.squad));
        setTeamACompStat(getAllStats(event.target.value, compareStatistics, data));
    }
    
    function teamBChangeHandler(event) {
        setSelectedTeamBValue(event.target.value);
        setTeamBLocMap(generatePlayerLocationMap(getTeamFromUsername(data, event.target.value).live.squad));
        setTeamBCompStat(getAllStats(event.target.value, compareStatistics, data));
    }

    function selectedPlotParameterChangeHandler(event) {
        setSelectedPlotParameter(event.target.value);
    }

    function getIndexTs(data, param) {
        var ddData = [];
        data['compare'][param]['index'].forEach(element => {
            ddData.push(`GW${element}`)
        });
        return ddData;
    }

    function getValueTs(data, param) {
        var ddData = [];
        data['compare'][param]['value'].forEach(element => {
            ddData.push(element)
        });
        return ddData;
    }

    function generateLineChartOptions(index, data1, data2) {
        var options = {
            chart: {
              backgroundColor: "#6c757d30"
            },
            title: {
              text: 'Line chart',
              style: {
                display: 'none'
              }
            },
            legend: {
              align: 'right',
              verticalAlign: 'top',
              symbolWidth: 5,
              symbolHeight: 8
            },
            xAxis: {
              tickColor: '#FFF',
              categories: index,
              labels: {
                formatter: function () {
                  return `${this.value}`
                },
                style: {
                  color: '#DFDFDF'
                }
              }
            },
            yAxis: {
              tickColor: '#FFF',
              gridLineColor: "#6c757d30",
              title: {
                style: {
                  display: 'none'
                }
              },
              labels: {
                formatter: function () {
                  return `${this.value}`
                },
                style: {
                  color: '#DFDFDF'
                }
              }
            },
            plotOptions: {
              series: {
                marker: {
                  symbol: 'circle'
                }
              }
            },
            tooltip: {
              shared: true
            },
            series: [{
              type: 'line',
              name: '',
              color: '#007bff',
              data: data1
            }, {
              type: 'line',
              name: '',
              color: '#28a745',
              data: data2
            }]
        };
        return options;
    }

    useEffect(() => {
        var options = generateLineChartOptions(getIndexTs(teamBCompStat, selectedPlotParameter), 
        getValueTs(teamACompStat, selectedPlotParameter), 
        getValueTs(teamBCompStat, selectedPlotParameter));
        console.log('Chart update ini');
        setLineChartOptions(options);
        console.log('Chart update done');
    }, [selectedPlotParameter, selectedTeamAValue, selectedTeamBValue]);

    return (
        <React.Fragment>
            <div className="compare-view-content" style={{marginTop:'1.5rem'}}>
                <div className="compare-view-body is-blue">
                    <div className="compare-view-bar is-blue">
                        <div className="compare-view-square">
                            <div className="compare-view-square-title">GW Points</div>
                            <div className="compare-view-square-body">{teamACompStat['live']['live']['currentGWTotalWithProvisionalBonus']}</div>
                        </div>
                        <div className="compare-view-square">
                            <div className="compare-view-square-title">Ovr Points</div>
                            <div className="compare-view-square-body">{teamACompStat['live']['live']['currentTotalWithProvisionalBonus']}</div>
                        </div>
                        <div className="compare-view-square">
                            <div className="compare-view-square-title">Ovr Rank</div>
                            <div className="compare-view-square-body">{teamACompStat['live']['info']['overallRank'].toLocaleString()}</div>
                        </div>
                    </div>
                    <div className="compare-view-dropdown">
                        <Dropdown data={dropdownData} selectedItem={selectedTeamAValue} handleChange={(x) => teamAChangeHandler(x)} />
                    </div>       
                    <TeamPlot data={teamALocMap}/>
                    
                </div>    
                <div className="compare-view-body is-green">
                    <div className="compare-view-bar is-green">
                        <div className="compare-view-square">
                            <div className="compare-view-square-title">GW Points</div>
                            <div className="compare-view-square-body">{teamBCompStat['live']['live']['currentGWTotalWithProvisionalBonus']}</div>
                        </div>
                        <div className="compare-view-square">
                            <div className="compare-view-square-title">Ovr Points</div>
                            <div className="compare-view-square-body">{teamBCompStat['live']['live']['currentTotalWithProvisionalBonus']}</div>
                        </div>
                        <div className="compare-view-square">
                            <div className="compare-view-square-title">Ovr Rank</div>
                            <div className="compare-view-square-body">{teamBCompStat['live']['info']['overallRank'].toLocaleString()}</div>
                        </div>
                    </div>
                    <div className="compare-view-dropdown">
                        <Dropdown data={dropdownData} selectedItem={selectedTeamBValue} handleChange={(x) => teamBChangeHandler(x)} />
                    </div>
                    <TeamPlot data={teamBLocMap}/>
                    
                </div>
                <div className="compare-view-section is-blue">
                    <div className="compare-view-title">
                        Transfers
                    </div>
                    <div className="compare-view-body-transfers">
                        {
                            teamACompStat['compare']['transfers'][0]['transfers'].map((event, index) => (
                                <div className="compare-view-body-transfer-item">
                                    <p><IconChoice component={{slug:ArrowUpIcon}} />&nbsp;&nbsp;{event[0]}</p>
                                    <p><IconChoice component={{slug:ArrowDownIcon}} />&nbsp;&nbsp;{event[1]}</p>
                                </div>
                            ))
                        }
                    </div>
                </div>
                <div className="compare-view-section is-green">
                    <div className="compare-view-title">
                        Transfers
                    </div>
                    <div className="compare-view-body-transfers">
                        {
                            teamBCompStat['compare']['transfers'][0]['transfers'].map((event, index) => (
                                <div className="compare-view-body-transfer-item">
                                    <p><IconChoice component={{slug:ArrowUpIcon}} />&nbsp;&nbsp;{event[0]}</p>
                                    <p><IconChoice component={{slug:ArrowDownIcon}} />&nbsp;&nbsp;{event[1]}</p>
                                </div>
                            ))
                        }
                    </div>
                </div>
                
                <div className="compare-view-section is-blue">
                    <div className="compare-view-bar is-blue">
                        <div className="compare-view-square">
                            <div className="compare-view-square-title">Best Ovr Rank</div>
                            <div className="compare-view-square-body">{teamACompStat['compare']['stats']['bestOverallRank'].toLocaleString()}</div>
                        </div>
                        <div className="compare-view-square">
                            <div className="compare-view-square-title">Highest Squad Value</div>
                            <div className="compare-view-square-body">{teamACompStat['compare']['stats']['highestValue']/10}</div>
                        </div>
                        <div className="compare-view-square">
                            <div className="compare-view-square-title">Max Points on Bench</div>
                            <div className="compare-view-square-body">{teamACompStat['compare']['stats']['maxPointsOnBench']}</div>
                        </div>
                    </div>
                    <div className="compare-view-bar is-blue">
                        <div className="compare-view-square">
                            <div className="compare-view-square-title">Net Transfers</div>
                            <div className="compare-view-square-body">{teamACompStat['compare']['stats']['netTransfers']}</div>
                        </div>
                        <div className="compare-view-square">
                            <div className="compare-view-square-title">Net Transfer Cost</div>
                            <div className="compare-view-square-body">{-teamACompStat['compare']['stats']['netTransfersCost']}</div>
                        </div>
                        <div className="compare-view-square">
                            <div className="compare-view-square-title">Net Points on Bench</div>
                            <div className="compare-view-square-body">{teamACompStat['compare']['stats']['netPointsOnBench']}</div>
                        </div>
                    </div>
                </div>

                <div className="compare-view-section is-green">
                    <div className="compare-view-bar is-green">
                    <div className="compare-view-square">
                            <div className="compare-view-square-title">Best Ovr Rank</div>
                            <div className="compare-view-square-body">{teamBCompStat['compare']['stats']['bestOverallRank'].toLocaleString()}</div>
                        </div>
                        <div className="compare-view-square">
                            <div className="compare-view-square-title">Highest Squad Value</div>
                            <div className="compare-view-square-body">{teamBCompStat['compare']['stats']['highestValue']/10}</div>
                        </div>
                        <div className="compare-view-square">
                            <div className="compare-view-square-title">Max Points on Bench</div>
                            <div className="compare-view-square-body">{teamBCompStat['compare']['stats']['maxPointsOnBench']}</div>
                        </div>
                    </div>
                    <div className="compare-view-bar is-green">
                    <div className="compare-view-square">
                            <div className="compare-view-square-title">Net Transfers</div>
                            <div className="compare-view-square-body">{teamBCompStat['compare']['stats']['netTransfers']}</div>
                        </div>
                        <div className="compare-view-square">
                            <div className="compare-view-square-title">Net Transfer Cost</div>
                            <div className="compare-view-square-body">{-teamBCompStat['compare']['stats']['netTransfersCost']}</div>
                        </div>
                        <div className="compare-view-square">
                            <div className="compare-view-square-title">Net Points on Bench</div>
                            <div className="compare-view-square-body">{teamBCompStat['compare']['stats']['netPointsOnBench']}</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div className="compare-view-body is-blue" style={{marginTop:'1em', backgroundColor:'#6c757d30'}}>
                <div className="compare-view-dropdown" style={{marginBottom:'1em'}}>
                    <Dropdown data={plotParameters} selectedItem={selectedPlotParameter} handleChange={(x) => selectedPlotParameterChangeHandler(x)} />
                </div>
                <LineChart options={lineChartOptions}/>
            </div>
        </React.Fragment>
    )
}

export default CompareView;