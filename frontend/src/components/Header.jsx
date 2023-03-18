import React, { useEffect, useState } from "react";
import notificationIcon from '../assets/notification.png';
import { useNavigate, useLocation } from "react-router-dom";

const Header = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [hide, setHide] = useState('');

  useEffect(() => {
    if (location.pathname === '/projects') setHide('');
    else setHide('hide');
  }, [location])

  return (
    <div id="header">
      <div className={`create-project-button ${hide}`} style={{marginLeft: '3vw'}} onClick={() => navigate('/projects/create')}>
        Start a new project
      </div>
      <div></div>
      <img src={notificationIcon} style={{height: '40%', marginRight: '3vw'}}/>
    </div>
  )
};

export default Header;
