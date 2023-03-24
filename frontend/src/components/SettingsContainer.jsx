import React from "react";
import './SettingsContainer.css'
import banIcon from '../assets/settings ban user.png';
import adminIcon from '../assets/settings admin user.png';

const SettingsContainer = () => {
  return (
    <>
      <div className="settings-container">
        <h3>Admin</h3>
        <p style={{ color: "gray" }}>Manage and configure user accounts.</p>
        <div className="divider"></div>
        <div className="buttons">
          <button><img src={adminIcon} />Admin User</button>
          <button><img src={banIcon} />Ban User</button>
        </div>
      </div>
    </>
  )
}

export default SettingsContainer;
