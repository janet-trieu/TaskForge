import React, { useState, useEffect } from "react";
import ConnectionsSearchbar from "../components/ConnectionsSearchbar";
import ConnectionCard from '../components/ConnectionCard';
import { makeRequest } from "../helpers";
import './Connections.css'

const Connections = ({ firebaseApp }) => {
  const [connections, setConnections] = useState([]);

  useEffect(async () => {
    const data = await makeRequest('/connections/get_connected_taskmasters', 'GET', null, firebaseApp.auth().currentUser.uid)
    if (data.error) alert(data.error);
    else {
      setConnections(data);
    }
  });

  return (
    <>
      <div id="connections-container">
        <div id="connections-header">
          <h3 id="connections-title">FirstName's Connections</h3>
          <ConnectionsSearchbar />
        </div>
        <div id="connections-card-container">
          {connections.map(uid => (
            <ConnectionCard key={uid} uid={uid} firebaseApp={firebaseApp} />
          ))}
        </div>
      </div>
    </>
  )
}

export default Connections;
