import React from "react";
import notificationIcon from '../assets/notification.png';
import { useNavigate } from "react-router-dom";

const Header = () => {
  const navigate = useNavigate();
  return (
    <div id="header">
      <div className='create-project-button' style={{marginLeft: '3vw'}} onClick={() => navigate('/projects/create')}>
        Start a new project
      </div>
      <img src={notificationIcon} style={{height: '40%', marginRight: '3vw'}}/>
    </div>
  )
};

export default Header;
