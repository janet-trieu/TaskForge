import React from "react";
import './Searchbar.css';

const ProjectSearchbar = () => {
  const handleSearch = (event) => {
    event.preventDefault();
    console.log(event, 'hi');
  }
  return (
    <div id='searchbar-container'>
      <form onSubmit={handleSearch}>
        <input id='searchbar' placeholder="Search projects" />
        <button type='submit'>Search</button>
      </form>
      <div id="toggle-container">
        Show completed projects
        <label className="switch">
          <input type="checkbox" id="completed-projects" />
          <span className="slider round"></span>
        </label>
      </div>
    </div>
  )
}

export default ProjectSearchbar;
