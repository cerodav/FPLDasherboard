import React, { lazy } from 'react';

function MiniStatTable({ title, data }) {
    return (
        <React.Fragment>
            <div className="stat-table">
                <div className="stat-table-title">
                    {title}
                </div>    
                <div className="stat-table-body">
                    {
                        data.map((item, index) => (
                            <div className="stat-table-row" key={index}>
                                <div className="stat-table-team">
                                    <span className="team-name">{item.teamName}</span>
                                    <br></br>
                                    <span className="manager-name">{item.playerName}</span>
                                </div>
                                <div className="stat-table-value">
                                    {item.value}
                                </div>    
                            </div>    
                        ))
                    }
                </div>    
            </div>
        </React.Fragment>
    )
}

export default MiniStatTable;