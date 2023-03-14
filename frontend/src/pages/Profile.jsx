import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import { makeRequest } from "../helpers";
import starIcon from "../assets/star.png";
import defaultProfilePic from '../assets/default project icon.png'
import taskIcon from '../assets/tasks.png';

const Profile = ({ firebaseApp }) => {
  const location = useLocation();
  const [isLoading, setIsLoading] = useState("Loading...");
  const [data, setData] = useState();

  const getInformation = async () => {
    if (location.pathname === '/projects') {
      const uid = await firebaseApp.auth().currentUser.uid;
      const data = await makeRequest(`/profile/${uid}`, 'GET', null, uid);
      if (data.error) alert(data.error);
      else {
        setIsLoading(false);
        setData(data);
      }
    } else {
      const uid = await firebaseApp.auth().currentUser.uid;
      const requested_uid = location.pathname.split('/')[2];
      const data = await makeRequest(`/profile/${uid}`, 'GET', {uid: requested_uid}, uid);
      if (data.error) alert(data.error);
      else {
        setIsLoading(false);
        setData(data);
      }
    }
  }
  useEffect(getInformation, []);

  return (
    // isLoading || (

      <div id='profile-page'>
        <div id='profile-header'>
          <div id='profile-pic-container'><img id='profile-pic' src={defaultProfilePic}/></div>
          <div id='profile-info'>
            <div style={{fontWeight: 'bold', fontSize: '1.5em'}}>Your Name</div>
            <div>Your Role</div>
            <div style={{display: 'flex', alignItems: 'center'}}>
              <div>2.55</div>
              &nbsp;
              <img src={starIcon} style={{height: '1em'}}/>
            </div>
            <div>5 connections</div>
          </div>
        </div>
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
  //)
}

export default Profile;
