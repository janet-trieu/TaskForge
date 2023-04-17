import React, { useState, forwardRef } from "react";
import { makeRequest, fileToDataUrl } from "../helpers";
import defaultProfilePic from '../assets/default project icon.png'

const ProfileModalContent = forwardRef(({ details, setDetails, handleClose, firebaseApp }, ref) => {
  const [icon, setIcon] = useState(details.photo_url || defaultProfilePic);

  const handleSave = async (event) => {
    event.preventDefault();
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
        <button type="submit">Save Changes</button>
      </form>
    </div>
  );
});

export default ProfileModalContent;