import React from "react";
import './ConnectionCard.css';
import userIcon from '../assets/default user icon.png';

const ConnectionCard = () => {
  return (
    <>
      <div className="connection-card">
        <img src={userIcon}></img>
        <div className="connection-card-info">
          <div style={{fontWeight: 'bold'}}>FullName</div>
          <div>Role</div>
          <div style={{color: 'gray'}}># mutual connections</div>
        </div>
      </div>
    </>
  )
}

export default ConnectionCard;
