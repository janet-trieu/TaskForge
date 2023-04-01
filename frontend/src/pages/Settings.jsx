import React from "react";
import SettingsContainer from '../components/SettingsContainer.jsx';
//import SettingsModalConfirm from "../components/SettingsModalConfirm.jsx";

import banIcon from '../assets/settings ban user.png';
import adminIcon from '../assets/settings admin user.png';

const adminButtons = [
  { id: 1, icon: adminIcon, action: 'Admin', warning: 'This will give the user admin permissions.' },
  { id: 2, icon: banIcon, action: 'Ban', warning: 'This will remove all existing details permanently.'},
]

const Settings = () => {
  return (
    <>
      <SettingsContainer title="Admin" description="Manage and configure user accounts." buttons={adminButtons} />
    </>
  )
}

export default Settings;
