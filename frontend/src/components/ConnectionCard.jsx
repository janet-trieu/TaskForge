import React, { useState, useEffect } from "react";
import { makeRequest } from "../helpers";
import './ConnectionCard.css';
import userIcon from '../assets/default user icon.png';

const ConnectionCard = ({ firebaseApp, uid }) => {
  const [isLoading, setIsLoading] = useState('Loading...');
  const [connectionDetails, setConnectionDetails] = useState(null);

  useEffect(async () => {

    const data = await makeRequest('/connections/details', 'GET', {uid: uid}, firebaseApp.auth().currentUser.uid);
    if (data.error) alert(data.error);
    else {
      setConnectionDetails(data);
      setIsLoading(false);
    }
  }, []);

  return (
    isLoading || (
      <div className="connection-card">
        <img src={userIcon}></img>
        <div className="connection-card-info">
          <div style={{fontWeight: 'bold'}}>{connectionDetails.display_name}</div>
          <div style={{color: 'gray'}}>{connectionDetails.role}</div>
        </div>
      </div>
    )
  )
}

export default ConnectionCard;
