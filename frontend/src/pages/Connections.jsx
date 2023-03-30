import React from "react";
import ConnectionsSearchbar from "../components/ConnectionsSearchbar";
import ConnectionCard from '../components/ConnectionCard';
import './Connections.css'

const Connections = () => {
  return (
    <>
      <div id="connections-container">
        <div id="connections-header">
          <h3 id="connections-title">FirstName's Connections</h3>
          <ConnectionsSearchbar />
        </div>
        <div id="connections-card-container">
          <ConnectionCard />
          <ConnectionCard />
          <ConnectionCard />
          <ConnectionCard />
          <ConnectionCard />
          <ConnectionCard />
          <ConnectionCard />
          <ConnectionCard />
          <ConnectionCard />
          <ConnectionCard />
          <ConnectionCard />
          <ConnectionCard />
          <ConnectionCard />
          <ConnectionCard />
        </div>
      </div>
    </>
  )
}

export default Connections;
