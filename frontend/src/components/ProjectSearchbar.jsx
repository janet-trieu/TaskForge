import React from "react";
import './Searchbar.css';
import { makeRequest } from "../helpers";

const ProjectSearchbar = ({ setProjects, setIsLoading, uid, showCompleted, setShowCompleted }) => {
  const handleSearch = async (event) => {
    event.preventDefault();
    setIsLoading('Loading...');
    const data = await makeRequest('/projects/search', 'GET', {query: event.target.searchbar.value}, uid);
    if (data.error) alert(data.error);
    else {
      setProjects(data);
      setIsLoading(false);
    }
  }

  const handleToggle = () => {
    const temp = showCompleted;
    setShowCompleted(!temp);
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
          <input onChange={handleToggle} type="checkbox" id="completed-projects" />
          <span className="slider round"></span>
        </label>
      </div>
    </div>
  )
}

export default ProjectSearchbar;
