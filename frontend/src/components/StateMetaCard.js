// import Tooltip from './Tooltip';

import {InfoIcon, CircleIcon} from '@primer/octicons-v2-react';
import React from 'react';

function StateMetaCard({
  title,
  statistic,
  total,
  formula,
  date,
  description,
  className,
  playingPlayerList = null,
  benchPlayerList = null,
  differentialPlayerList = null,
}) {
  return (
    <div className={`meta-item ${className}`} style={{paddingBottom: '1rem'}}>
      <div className="meta-item-top">
        <h3>{title}</h3>
        {/* <Tooltip {...{data: formula}}>
          {!playingPlayerList && (<InfoIcon size={16} />)}
        </Tooltip> */}
      </div>
      <h1>{statistic}</h1>
      <h5>{date}</h5>
      {total && <h5>{`India has ${total} CPM`}</h5>}
      {description && (<p>{description}</p>)}
      {playingPlayerList && (<div className={`pills`} style={{justifyContent:'flex-start', marginBottom: '0.25rem'}}>{playingPlayerList.slice(0,6).map((player, idx) => (
        <button-playing type={`button`}>{player.name}&nbsp;&nbsp;({player.liveScore})</button-playing>
      ))}</div>)}
      {playingPlayerList && (<div className={`pills`} style={{justifyContent:'flex-start', marginBottom: '0.25rem'}}>{playingPlayerList.slice(6, 11).map((player, idx) => (
        <button-playing type={`button`}>{player.name}&nbsp;&nbsp;({player.liveScore})</button-playing>
      ))}</div>)}
      {playingPlayerList && (<div className={`pills`} style={{justifyContent:'flex-start', marginBottom: '0.25rem'}}>{playingPlayerList.slice(11, playingPlayerList.length).map((player, idx) => (
        <button-playing type={`button`}>{player.name}&nbsp;&nbsp;({player.liveScore})</button-playing>
      ))}</div>)}
      {benchPlayerList && (<div className={`pills`} style={{justifyContent:'flex-start', marginBottom: '0.25rem'}}>{benchPlayerList.map((player, idx) => (
        <button-bench type={`button`}>{player.name}&nbsp;&nbsp;({player.liveScore})</button-bench>
      ))}</div>)}
      {differentialPlayerList && (<h1></h1>)}
      {differentialPlayerList && (<h5></h5>)}
      {differentialPlayerList && (<div className="meta-item-top">
        <h3>{`Differentials`}</h3>
      </div>)}
      {differentialPlayerList && (<h1></h1>)}
      {differentialPlayerList && (<h5></h5>)}
      {differentialPlayerList && (<div className={`pills`} style={{justifyContent:'flex-start', marginBottom: '0.25rem'}}>{differentialPlayerList.slice(0,6).map((player, idx) => (
        <button-playing type={`button`}>{player.name}&nbsp;&nbsp;({player.liveScore})</button-playing>
      ))}</div>)}
      {differentialPlayerList && (<div className={`pills`} style={{justifyContent:'flex-start', marginBottom: '0.25rem'}}>{differentialPlayerList.slice(6, 11).map((player, idx) => (
        <button-playing type={`button`}>{player.name}&nbsp;&nbsp;({player.liveScore})</button-playing>
      ))}</div>)}
      {differentialPlayerList && (<div className={`pills`} style={{justifyContent:'flex-start', marginBottom: '0.25rem'}}>{differentialPlayerList.slice(11, playingPlayerList.length).map((player, idx) => (
        <button-playing type={`button`}>{player.name}&nbsp;&nbsp;({player.liveScore})</button-playing>
      ))}</div>)}
    </div>
  );
}

export default StateMetaCard;
