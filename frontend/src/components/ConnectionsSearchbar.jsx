import React from "react";
import './Searchbar.css';
import { makeRequest } from "../helpers";

const ConnectionsSearchbar = (props) => {
  const handleSearch = async (event) => {
    event.preventDefault();
    const query = event.target.searchbar.value;

    if (query === "") {props.setConnections(null); return;};

    const newConnections = props.connections.filter((connection) => {
      if (connection.display_name.toLowerCase().includes(query.toLowerCase())) {
        return true
      }
      return false
    });
    props.setConnections(newConnections);
  }
  return (
      <form onSubmit={handleSearch}>
        <input id='searchbar' placeholder="Search connections" />
        &nbsp;&nbsp;
        <button type='submit'>Search</button>
      </form>
  )
}

export default ConnectionsSearchbar;
