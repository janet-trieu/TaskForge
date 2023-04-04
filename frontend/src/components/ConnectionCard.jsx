import React, { useState, useEffect } from "react";
import { makeRequest } from "../helpers";
import './ConnectionCard.css';
import userIcon from '../assets/default user icon.png';

const ConnectionCard = ({ firebaseApp, photo_url, displayName, role }) => {
  if (!photo_url) {
    photo_url = userIcon
  }

  return (
      <div className="connection-card">
        <img src={photo_url}></img>
        <div className="connection-card-info">
          <div style={{fontWeight: 'bold'}}>{displayName}</div>
          <div style={{color: 'gray'}}>{role}</div>
        </div>
      </div>
    )
}

export default ConnectionCard;
