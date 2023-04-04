import React, { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import logoName from '../assets/logo_with_text.png';
import settingsIcon from '../assets/settings.svg';
import logoutIcon from '../assets/logout.png';
import homeIcon from '../assets/home.png';
import projectsIcon from '../assets/projects.png';
import tasksIcon from '../assets/tasks.png';
import profileIcon from '../assets/profile.png';
import connectionsIcon from '../assets/connections.png';

const Sidebar = ({ firebaseApp }) => {
  const navigate = useNavigate();
  const location = useLocation();

  const [homeHighlight, setHomeHighlight] = useState('');
  const [projectsHighlight, setProjectsHighlight] = useState('');
  const [tasksHighlight, setTasksHighlight] = useState('');
  const [profileHighlight, setProfileHighlight] = useState('');
  const [connectionsHighlight, setConnectionsHighlight] = useState('');
  const [settingsHighlight, setSettingsHighlight] = useState('');

  useEffect(() => {
    const path = location.pathname.split('/')[1];

    setHomeHighlight('');
    setProjectsHighlight('');
    setTasksHighlight('');
    setProfileHighlight('');
    setConnectionsHighlight('');
    setSettingsHighlight('');

    switch(path) {
      case "projects":
        setProjectsHighlight("highlighted");
        break;
      case "tasks":
        setTasksHighlight("highlighted");
        break;
      case "profile":
        setProfileHighlight("highlighted");
        break;
      case "connections":
        setConnectionsHighlight("highlighted");
        break;
      case "settings":
        setSettingsHighlight("highlighted");
        break;
      default:
        setHomeHighlight("highlighted");
    }

  }, [location])

  return (
    <>
      <div id='sidebar'>
        <img id='logo-name' src={logoName} style={{width: '70%'}} />
        <div id='sidebar-middle'>
          <div className={`sidebar-button ${homeHighlight}`} onClick={() => navigate('/')}><img src={homeIcon} />Home</div>
          <div className={`sidebar-button ${projectsHighlight}`} onClick={() => navigate('/projects')}><img src={projectsIcon} />Projects</div>
          <div className={`sidebar-button ${tasksHighlight}`} onClick={() => navigate('/tasks')}><img src={tasksIcon} />Assigned Tasks</div>
          <div className={`sidebar-button ${profileHighlight}`} onClick={() => navigate('/profile')}><img src={profileIcon} />Profile</div>
          <div className={`sidebar-button ${connectionsHighlight}`} onClick={() => navigate('/connections')}><img src={connectionsIcon} />Connections</div>
        </div>
        <div id='sidebar-bottom'>
          <div className={`sidebar-button ${settingsHighlight}`} onClick={() => navigate('/settings')}><img src={settingsIcon} />Settings</div>
          <div className="sidebar-button" onClick={() => {firebaseApp.auth().signOut(); navigate('/');}}>
            <img src={logoutIcon} />Logout
          </div>
        </div>
      </div>
    </>
  )
};

export default Sidebar;
