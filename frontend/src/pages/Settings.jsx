import React from "react";
import SettingsContainer from '../components/SettingsContainer.jsx';

import banIcon from '../assets/settings ban user.png';
import adminIcon from '../assets/settings admin user.png';

const adminButtons = [
  { id: 1, icon: adminIcon, label: 'Admin User' },
  { id: 2, icon: banIcon, label: 'Ban User' },
]

const Settings = () => {
  return (
    <>
      <SettingsContainer title="Admin" description="Manage and configure user accounts." buttons={adminButtons} />
    </>
  )
}

export default Settings;
