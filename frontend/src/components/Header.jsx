import React, { useEffect, useState } from "react";
import notificationIcon from '../assets/notification.png';
import { useNavigate, useLocation } from "react-router-dom";
import { Modal } from '@mui/material';
import NotificationModalContent from "./NotificationModalContent";

const Header = ({ firebaseApp }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const [projectCreateHide, setProjectCreateHide] = useState('');
  const [projectViewHide, setProjectViewHide] = useState('');
  const [openNotifications, setOpenNotifications] = useState(false);
  const handleOpenNotifications = () => {setOpenNotifications(true)};
  const handleCloseNotifications = () => {setOpenNotifications(false)};

  useEffect(() => {
    location.pathname === '/projects' 
      ? setProjectCreateHide('') 
      : setProjectCreateHide('hide');

    location.pathname.includes('/projects/') && location.pathname !== '/projects/create'
      ? setProjectViewHide('') 
      : setProjectViewHide('hide');
  }, [location])

  const switchView = (view) => {
    const pid = location.pathname.split('/')[2];
    navigate(`/projects/${pid}/${view}`);
  }

  return (
    <div id="header">
      <div className={`create-project-button ${projectCreateHide}`} style={{marginLeft: '3vw'}} onClick={() => navigate('/projects/create')}>
        Start a new project
      </div>
      <div>
        <button className={`task-view-button ${projectViewHide}`} style={{marginLeft: '3vw', marginRight: '1vw'}} onClick={() => {switchView('task')}}>Backlog</button>
        <button className={`board-view-button ${projectViewHide}`} onClick={() => {switchView('board')}}>Task Board</button>
      </div>
      <div></div>
      <img src={notificationIcon} style={{height: '3em', width: 'auto', marginRight: '3vw'}} onClick={handleOpenNotifications} />
      <Modal open={openNotifications} onClose={handleCloseNotifications}>
        <NotificationModalContent handleClose={handleCloseNotifications} firebaseApp={firebaseApp} />
      </Modal>
    </div>
  )
};

export default Header;
