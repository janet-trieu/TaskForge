import React, { useState, useEffect } from "react";
import { makeRequest } from "../helpers.js";
import SettingsContainer from '../components/SettingsContainer.jsx';
import banIcon from '../assets/settings ban user.png';
import adminIcon from '../assets/settings admin user.png';
import unbanIcon from '../assets/settings unban user.png';
import removeIcon from '../assets/settings remove user.png';
import restoreIcon from '../assets/settings restore user.png';
import passwordIcon from '../assets/settings reset password.png'

const adminButtons = [
  { id: 1, icon: adminIcon, action: 'Admin User', warning: 'This will give the user admin permissions.', type: 'uid search' },
  { id: 2, icon: banIcon, action: 'Ban User', warning: 'This will ban the user from TaskForge.', type: 'uid search'},
  { id: 3, icon: unbanIcon, action: 'Unban User', warning: 'This will unban the user from TaskForge.', type: 'uid search'},
  { id: 4, icon: removeIcon, action: 'Remove User', warning: 'This will remove the user from TaskForge.', type: 'uid search'}
  // { id: 5, icon: restoreIcon, action: 'Restore User', warning: 'This will restore the user from TaskForge.', type: 'uid search'},
]

const accountButtons = [
  { id: 1, icon: passwordIcon, action:'Reset Password', warning: 'This will send a reset password link to your email.', type: 'confirm'}
]

const Settings = ({ firebaseApp }) => {
  const [isLoading, setIsLoading] = useState("Loading...");
  const [admin, setAdmin] = useState();

  useEffect(async () => {
    const data = await makeRequest("/admin/is_admin", "GET", null, firebaseApp.auth().currentUser.uid);
    if (data.error) alert(data.error);
    else {
      console.log(data)
      setAdmin(data);
      setIsLoading(false);
    }
  }, [])

  return (
    <>
      {isLoading || (
        <div>
          {admin && <SettingsContainer firebaseApp={firebaseApp} title="Admin" description="Manage and configure user accounts." buttons={adminButtons} />}
          <br />
          <SettingsContainer firebaseApp={firebaseApp} title="Account" description="Manage and configure your account." buttons={accountButtons} />
        </div>
      )}
    </>
  )
}

export default Settings;
