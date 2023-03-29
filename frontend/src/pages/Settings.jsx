import React from "react";
import SettingsContainer from '../components/SettingsContainer.jsx';

import banIcon from '../assets/settings ban user.png';
import adminIcon from '../assets/settings admin user.png';
import passwordIcon from '../assets/settings reset password.png'

const adminButtons = [
  { id: 1, icon: adminIcon, action: 'Admin User', warning: 'This will give the user admin permissions.', type: 'uid search' },
  { id: 2, icon: banIcon, action: 'Ban User', warning: 'This will remove all existing details permanently.', type: 'uid search'},
]

const accountButtons = [
  { id: 1, icon: passwordIcon, action:'Reset Password', warning: 'This will send a reset password link to your email.', type: 'confirm'}
]

const Settings = () => {
  return (
    <>
      <SettingsContainer title="Admin" description="Manage and configure user accounts." buttons={adminButtons} />
      <SettingsContainer title="Account" description="Manage and configure your account." buttons={accountButtons} />
    </>
  )
}

export default Settings;
