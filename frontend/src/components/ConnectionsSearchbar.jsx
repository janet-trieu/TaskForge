import React from "react";
import './Searchbar.css';

const ConnectionsSearchbar = () => {
  const handleSearch = (event) => {
    event.preventDefault();
    console.log(event, 'hi');
  }
  return (
      <form onSubmit={handleSearch}>
        <input id='searchbar' placeholder="Search connections" />
        <button type='submit'>Search</button>
      </form>
  )
}

export default ConnectionsSearchbar;
