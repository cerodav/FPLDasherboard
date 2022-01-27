import React, { useState, lazy, Suspense, useMemo } from 'react';
import Background from '../images/teamPlot/TeamPlotWhite.png';
import classnames from 'classnames';

function TeamPlot({ data }) {
    const trail = useMemo(() => {
        const styles = [];
        for(var i = 0; i < 15; i = i + 1) {
            styles.push({
                animationDelay: `${i * 50}ms`,
              });
        }
        return styles;
    }, []);
    const [nAtt, setNAtt] = useState(data.Attacker.length);
    const [nMidd, setNMidd] = useState(data.Attacker.length + data.Midfielder.length);
    const [nDef, setNDef] = useState(data.Attacker.length + data.Midfielder.length + data.Defender.length);
    const [nGK, setNGK] = useState(data.Defender.length + data.Attacker.length + data.Midfielder.length + data.Goalkeeper.length);

    return (
        <React.Fragment>
            <div className="team-plot-container" style={{backgroundImage: `url(${Background})`, backgroundPosition: 'center', backgroundSize: 'contain', backgroundRepeat: 'no-repeat'}}>
                <div className="team-plot-att" style={{ gridTemplateColumns: `repeat(${data.Attacker.length}, auto)`,}}>
                {
                    data.Attacker.map((player, index) => (
                        <div key={player.name} className={classnames('player', 'fadeInUp')} style={trail[index]}>
                            <div className="player-name">{player.name}</div>
                            <div className="player-score">{player.totalPoints}</div>
                        </div>
                    ))
                }
                </div>
                <div className="team-plot-mid" style={{ gridTemplateColumns: `repeat(${data.Midfielder.length}, auto)`,}}>
                {
                    data.Midfielder.map((player, index) => (
                        <div key={player.name} className={classnames('player', 'fadeInUp')} style={trail[index + nAtt]}>
                            <div className="player-name">{player.name}</div>
                            <div className="player-score">{player.totalPoints}</div>
                        </div>
                    ))
                }                    
                </div>
                <div className="team-plot-def" style={{ gridTemplateColumns: `repeat(${data.Defender.length}, auto)`,}}>
                {
                    data.Defender.map((player, index) => (
                        <div key={player.name} className={classnames('player', 'fadeInUp')} style={trail[index + nMidd]}>
                            <div className="player-name">{player.name}</div>
                            <div className="player-score">{player.totalPoints}</div>
                        </div>
                    ))
                }    
                </div>
                <div className="team-plot-gk" style={{ gridTemplateColumns: `repeat(${data.Goalkeeper.length}, auto)`,}}>
                {
                    data.Goalkeeper.map((player, index) => (
                        <div key={player.name} className={classnames('player', 'fadeInUp')} style={trail[index + nDef]}>
                            <div className="player-name">{player.name}</div>
                            <div className="player-score">{player.totalPoints}</div>
                        </div>
                    ))
                }    
                </div>
            </div>    
            <div className="team-plot-bch" style={{ gridTemplateColumns: `repeat(${data.Bench.length}, auto)`,}}>
                {
                    data.Bench.map((player, index) => (
                        <div key={player.name} className={classnames('player', 'fadeInUp')} style={trail[index + 11]}>
                            <div className="player-name">{player.name}</div>
                            <div className="player-score">{player.totalPoints}</div>
                        </div>
                    ))
                }  
            </div>
        </React.Fragment>
    )
}

export default TeamPlot;