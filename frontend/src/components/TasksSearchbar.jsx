import React from "react";
import './Searchbar.css';
import { makeRequest } from "../helpers";

const TasksSearchbar = ({ setTasks, setIsLoading, uid, showCompleted, setShowCompleted }) => {
  const handleSearch = async (event) => {
    event.preventDefault();
    setIsLoading('Loading...');

    const body = {
      query_tid: event.target.id.value,
      query_title: event.target.title.value,
      query_description: event.target.description.value,
      query_deadline: event.target.deadline.value
    }
    const data = await makeRequest('/tasklist/search', 'GET', body, uid);
    if (data.error) alert(data.error);
    else {
      setTasks(data);
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
        <input type="text" id='id' placeholder="Task ID" />
        <input type="text" id='title' placeholder="Task title" />
        <input type="text" id='description' placeholder="Task description" />
        <input type="text" id='deadline' placeholder="Deadline as DD/MM/YYYY" />
        <button type='submit'>Search</button>
      </form>
      <div id="toggle-container">
        Show completed tasks
        <label className="switch">
          <input onChange={handleToggle} type="checkbox" id="completed-projects" />
          <span className="slider round"></span>
        </label>
      </div>
    </div>
  )
}

export default TasksSearchbar;
