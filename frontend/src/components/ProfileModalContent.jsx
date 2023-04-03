import React, {forwardRef} from "react";
import { makeRequest } from "../helpers";

const ProfileModalContent = forwardRef(({ details, setDetails, setOpen, firebaseApp }, ref) => {
  const handleSave = async (event) => {
    event.preventDefault();
    let newDetails = details;
    newDetails.display_name = event.target.name.value;
    newDetails.role = event.target.role.value;

    const uid = firebaseApp.auth().currentUser.uid;
    const body = {
      display_name: newDetails.display_name,
      role: newDetails.role,
      email: null,
      photo_url: null
    }
    await makeRequest('/profile/update', 'PUT', body, uid)

    setDetails(newDetails);
    setOpen(false);
  } 
  return (
    <div id="profile-modal">
      <form id="profile-modal-form" onSubmit={handleSave}>
        <label htmlFor="name" style={{fontWeight: 'bold'}}>Display Name</label><br />
        <input type="text" id="name" defaultValue={details.display_name} /><br />
        <br />
        <label htmlFor="role" style={{fontWeight: 'bold'}}>Role</label><br />
        <input type="text" id="role" defaultValue={details.role} /><br />
        <br />
        <button type="submit">Save Changes</button>
      </form>
    </div>
  );
});

export default ProfileModalContent;