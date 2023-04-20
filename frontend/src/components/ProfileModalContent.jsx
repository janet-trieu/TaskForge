import React, { useState, forwardRef, useEffect } from "react";
import { makeRequest, fileToDataUrl } from "../helpers";
import defaultProfilePic from '../assets/default project icon.png'

const ProfileModalContent = forwardRef(({ details, setDetails, handleClose, firebaseApp }, ref) => {
  const [icon, setIcon] = useState(details.photo_url || defaultProfilePic);
  const [achievementVisible, setAchievementVisible] = useState(false);
  const [buttonText, setButtonText] = useState("Save Changes");
  const [reputuationVisible, setReputationVisible] = useState(false);

  useEffect(async () => {
    const achData = await makeRequest(`/achievements/get_hide_visibility?uid=${details.uid}`, 'GET', null, details.uid);
    const repData = await makeRequest(`/reputation/get_visibility?uid=${details.uid}`, 'GET', null, details.uid);
    setAchievementVisible(achData);
    setReputationVisible(repData);
  }, []);

  const handleSave = async (event) => {
    event.preventDefault();

    if (buttonText === "...") return;
    setButtonText("...");

    let newDetails = details;
    newDetails.display_name = event.target.name.value;
    newDetails.role = event.target.role.value;
    newDetails.email = event.target.email.value;
    newDetails.photo_url = icon;

    const uid = firebaseApp.auth().currentUser.uid;
    const body = {
      display_name: newDetails.display_name,
      role: newDetails.role,
      email: newDetails.email,
      photo_url: newDetails.photo_url
    }
    await makeRequest('/profile/update', 'PUT', body, uid)
    setDetails(newDetails);
    setButtonText("Save Changes");
    handleClose();
  }

  const uploadHandler = async (event) => {
    if (!event.target.files[0]) {
      setIcon(defaultProfilePic);
    } else {
      const file = event.target.files[0];
      const dataUrl = await fileToDataUrl(file);
      if (!dataUrl) setIcon(defaultProfilePic);
      else setIcon(dataUrl);
    }
  }

  const handleAchievementToggle = async (event) => {
    const data = await makeRequest('/achievements/toggle_visibility', 'POST', { action: event.target.checked }, details.uid);
    setAchievementVisible(data);
  }

  const handleReputationToggle = async (event) => {
    const data = await makeRequest('/reputation/toggle_visibility', 'POST', { visibility: event.target.checked }, details.uid);
    setReputationVisible(data);
  }

  return (
    <div id="profile-modal">
      <form id="profile-modal-form" onSubmit={handleSave}>
        <p style={{fontWeight: 'bold'}}>Icon</p>
        <div id='profile-update-icon-container'>
          <div className="profile-icon-container"><img className="profile-icon" src={icon}></img></div>
          <label htmlFor="profile-icon-upload">Change icon</label>
          <input type="file" id="profile-icon-upload" className="hide" onChange={uploadHandler} />
        </div>
        <br />
        <label htmlFor="name" style={{fontWeight: 'bold'}}>Display Name</label><br />
        <input type="text" id="name" defaultValue={details.display_name} /><br />
        <br />
        <label htmlFor="role" style={{fontWeight: 'bold'}}>Role</label><br />
        <input type="text" id="role" defaultValue={details.role} /><br />
        <br />
        <label htmlFor="email" style={{fontWeight: 'bold'}}>Email</label><br />
        <input type="text" id="email" defaultValue={details.email} /><br />
        <br />
        <label htmlFor="achievement-visbility" style={{fontWeight: 'bold'}}>Hide Achievements</label><br />
        <label className="switch">
          <input onChange={handleAchievementToggle} type="checkbox" id="toggle-achievement-visibility" checked={achievementVisible} />
          <span className="slider round"></span>
        </label><br />
        <br />
        <label htmlFor="reputation-visbility" style={{fontWeight: 'bold'}}>Show Reputation</label><br />
        <label className="switch">
          <input onChange={handleReputationToggle} type="checkbox" id="toggle-reputation-visibility" checked={reputuationVisible} />
          <span className="slider round"></span>
        </label><br />
        <br />
        <button type="submit">{buttonText}</button>
      </form>
    </div>
  );
});

export default ProfileModalContent;