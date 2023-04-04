import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import { makeRequest } from "../helpers";
import starIcon from "../assets/star.png";
import defaultProfilePic from '../assets/default project icon.png'
import taskIcon from '../assets/tasks.png';
import { Modal } from "@mui/material";
import ProfileModalContent from "../components/ProfileModalContent";

const Profile = ({ firebaseApp }) => {
  const location = useLocation();
  const [isLoading, setIsLoading] = useState("Loading...");
  const [details, setDetails] = useState();
  const [open, setOpen] = useState(false);
  const handleOpen = () => {setOpen(true)};
  const handleClose = () => {setOpen(false)};

  const getInformation = async () => {
    if (location.pathname === '/profile') {
      const uid = await firebaseApp.auth().currentUser.uid;
      const data = await makeRequest('/profile/details', 'GET', null, uid);
      if (data.error) alert(data.error);
      else {
        setDetails(data);
        setIsLoading(false);
      }
    } else {
      const uid = await firebaseApp.auth().currentUser.uid;
      const requested_uid = location.pathname.split('/')[2];
      const data = await makeRequest(`/profile/${uid}`, 'GET', {uid: requested_uid}, uid);
      if (data.error) alert(data.error);
      else {
        setDetails(data);
        setIsLoading(false);
      }
    }
  }
  useEffect(getInformation, []);

  return (
    isLoading || (
      <div id='profile-page'>
        <div id='profile-header'>
          <div id='profile-pic-container'><img id='profile-pic' src={defaultProfilePic}/></div>
          <div id='profile-info'>
            <div style={{fontWeight: 'bold', fontSize: '1.5em'}}>{details.display_name}</div>
            <div>{details.role}</div>
            <div style={{display: 'flex', alignItems: 'center'}}>
              <div>{details.rating}</div>
              &nbsp;
              <img src={starIcon} style={{height: '1em'}}/>
            </div>
            <div>{details.num_connections} connection(s)</div>
          </div>
          <button style={{marginLeft: '45vw'}} onClick={handleOpen}>Edit</button>
        </div>
        <Modal open={open} onClose={handleClose}>
          <ProfileModalContent details={details} setDetails={setDetails} handleClose={handleClose} firebaseApp={firebaseApp} />
        </Modal>
        <div className="profile-row">
          <div className='profile-box'>
            <div className='profile-box-header'>
              <div className='profile-box-header-icon'><img src={taskIcon}/></div>
              <div className='profile-box-header-title'></div>
            </div>
            <div>

            </div>
          </div>
          <div className='profile-box'>
            <div className='profile-box-header'>
              <div className='profile-box-header-icon'><img /></div>
              <div className='profile-box-header-title'></div>
            </div>
            <div>

            </div>
          </div>
        </div>
        <div className="profile-row">
          <div className='profile-box'>
            <div className='profile-box-header'>
              <div className='profile-box-header-icon'><img src={starIcon}/></div>
              <div className='profile-box-header-title'></div>
            </div>
            <div>

            </div>
          </div>
          <div className='profile-box'>
            <div className='profile-box-header'>
              <div className='profile-box-header-icon'><img /></div>
              <div className='profile-box-header-title'></div>
            </div>
            <div>

            </div>
          </div>
        </div>
      </div>
    )
  )
}

export default Profile;
