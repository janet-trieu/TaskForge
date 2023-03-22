import React from "react";
import ConnectionsSearchbar from "../components/ConnectionsSearchbar";
import ConnectionCard from '../components/ConnectionCard';  

const Connections = () => {
  return (
    <>
      <ConnectionsSearchbar />
      <div id='connections-container'>
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
    </>
  )
}

export default Connections;
