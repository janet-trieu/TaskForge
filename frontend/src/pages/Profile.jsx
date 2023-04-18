import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { makeRequest } from "../helpers";
import starIcon from "../assets/star.png";
import defaultProfilePic from '../assets/default project icon.png'
import taskIcon from '../assets/tasks.png';
import achievementIcon from '../assets/profile achievement.png'
import { Modal } from "@mui/material";
import ProfileModalContent from "../components/ProfileModalContent";
import './Profile.css'

import AchievementCard from '../components/Achievement/ProfileAchievementCard'

const Profile = ({ firebaseApp }) => {
  const location = useLocation();
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState("Loading...");
  const [isLoadingAchievements, setIsLoadingAchievements] = useState("Loading...");
  const [details, setDetails] = useState();
  const [achievements, setAchievements] = useState([]);
  const [isUser, setIsUser] = useState();
  const [open, setOpen] = useState(false);
  const [hideAchievements, setHideAchievements] = useState();
  const handleOpen = () => { setOpen(true) };
  const handleClose = () => { setOpen(false) };

  const getInformation = async () => {
    if (location.pathname === '/profile') {
      setIsUser(true);
      const uid = await firebaseApp.auth().currentUser.uid;
      const data = await makeRequest('/profile/details', 'GET', null, uid);
      if (data.error) alert(data.error);
      else {
        setDetails(data);
        setIsLoading(false);
      }

      {/* Achievement */ }
      const achievementsData = await makeRequest('/achievements/view/my', 'GET', null, uid);
      if (achievementsData.error) alert(achievementsData.error);
      else {
        const recentAchievements = achievementsData.slice(0, 3);
        setAchievements(recentAchievements);
        setIsLoadingAchievements(false);
      }
    } else {
      setIsUser(false);
      const uid = await firebaseApp.auth().currentUser.uid;
      const requested_uid = location.pathname.split('/')[2];
      const data = await makeRequest(`/connections/details?uid=${requested_uid}`, 'GET', null, uid);
      if (data.error) alert(data.error);
      else {
        setDetails(data);
        setIsLoading(false);
      }

      {/* Achievement */ }
      const achievementsData = await makeRequest('/achievements/view/notmy', 'GET', { conn_uid: requested_uid }, uid);
      if (achievementsData.error) alert(achievementsData.error);
      else {
        const recentAchievements = achievementsData.slice(0, 3);
        setAchievements(recentAchievements);
        setIsLoadingAchievements(false);
      }
    }
  }

  const handleAchievementClick = () => {
    if (isUser) {
      navigate('/achievements')
    } else {
      const requested_uid = location.pathname.split('/')[2];
      navigate(`/achievements/${requested_uid}`)
    }
  }

  const checkHideVisibility = async () => {
    const data = await makeRequest(`/achievements/get_hide_visibility?uid=${details.uid}`, 'GET', null, firebaseApp.auth().currentUser.uid);
    if (data.error) alert(data.error);
    if (data === true && !isUser) setHideAchievements(true);
    else setHideAchievements(false);
  };

  useEffect(() => {
    getInformation();
    checkHideVisibility();
  }, []);

  return (
    isLoading || (
      <div id='profile-page'>
        <div id='profile-header'>
          <div id='profile-pic-container'><img id='profile-pic' src={details.photo_url || defaultProfilePic} /></div>
          <div id='profile-info'>
            <div style={{ fontWeight: 'bold', fontSize: '1.5em' }}>{details.display_name}</div>
            <div>{details.email}</div>
            <div>{details.role}</div>
            <div style={{ display: 'flex', alignItems: 'center' }}>
              <div>{details.rating}</div>
              &nbsp;
              <img src={starIcon} style={{ height: '1em', width: '1em' }} />
            </div>
            <div>{details.num_connections} connection(s)</div>
          </div>
          <button className={isUser ? "" : "hide"} style={{ marginLeft: '45vw' }} onClick={handleOpen}>Edit</button>
        </div>
        <Modal open={open} onClose={handleClose}>
          <ProfileModalContent details={details} setDetails={setDetails} handleClose={handleClose} firebaseApp={firebaseApp} />
        </Modal>
        <div className="profile-row">
          <div className='profile-box'>
            <div className="profile-box-content">
              <div className='profile-box-header'>
                <div className='profile-box-header-icon'><img src={taskIcon} /></div>
                <div className='profile-box-header-title'></div>
                <button onClick={() => navigate(location.pathname === "/profile" ? "/tasks" : `/tasks/${location.pathname.split('/')[2]}`)}>Assigned Task List</button>
              </div>
              <div>
              </div>
            </div>
          </div>
          <div className='profile-box'>
            <div className="profile-box-content">
              <div className='profile-box-header'>
                <div className='profile-box-header-icon'><img /></div>
                <div className='profile-box-header-title'></div>
              </div>
              <div>
              </div>
            </div>
          </div>
        </div>
        <div className="profile-row">
          <div className='profile-box' onClick={() => navigate(location.pathname === "/profile" ? "/reputation" : `/reputation/${location.pathname.split('/')[2]}`)}>
            <div className="profile-box-content">
              <div className='profile-box-header'>
                <div className='profile-box-header-icon'><img src={starIcon} /></div>
                <div className='profile-box-header-title'>Reputation</div>
              </div>
              <div id="profile-reputation-box">
                <div>
                  <div>Communication</div>
                  <div>Time Management</div>
                  <div>Task Quality</div>
                </div>
                <div>
                  <div>##.#</div>
                  <div>##.#</div>
                  <div>##.#</div>
                </div>
              </div>
            </div>
          </div>
          <div className={!hideAchievements ? "" : "hide"}>
            <div className='profile-box' onClick={handleAchievementClick}>
              <div className="profile-box-content">
                <div className='profile-box-header'>
                  <div className='profile-box-header-icon'><img src={achievementIcon} /></div>
                  <div className='profile-box-header-title'>Achievements</div>
                </div>
                {isLoadingAchievements || (
                  <div className="badges">
                    {achievements.map((achievement, idx) => {
                      return <AchievementCard key={idx} aid={achievement.aid} title={achievement.title} />
                    })}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div >
    )
  )
}

export default Profile;
