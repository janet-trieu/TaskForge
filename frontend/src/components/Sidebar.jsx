import React from "react";
import logoName from '../assets/logo_with_text.png';
import settingsIcon from '../assets/settings.svg';
import logoutIcon from '../assets/logout.png';
import homeIcon from '../assets/home.png';
import projectsIcon from '../assets/projects.png';
import tasksIcon from '../assets/tasks.png';
import profileIcon from '../assets/profile.png';
import connectionsIcon from '../assets/connections.png';

const Sidebar = ({ firebaseApp }) => {
  return (
    <>
      <div id='sidebar'>
        <img id='logo-name' src={logoName} style={{width: '70%'}} />
        <div id='sidebar-middle'>
          <div className="sidebar-button"><img src={homeIcon} />Home</div>
          <div className="sidebar-button"><img src={projectsIcon} />Projects</div>
          <div className="sidebar-button"><img src={tasksIcon} />Tasks</div>
          <div className="sidebar-button"><img src={profileIcon} />Profile</div>
          <div className="sidebar-button"><img src={connectionsIcon} />Connections</div>
        </div>
        <div id='sidebar-bottom'>
          <div className="sidebar-button">
            <img src={settingsIcon} /> Settings
          </div>
          <div className="sidebar-button" onClick={() => {firebaseApp.auth().signOut();}}>
            <img src={logoutIcon} /> Logout
          </div>
        </div>
      </div>
    </>
  )
};

export default Sidebar;
