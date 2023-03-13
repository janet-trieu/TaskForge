import React from "react";
import notificationIcon from '../assets/notification.png';

const Header = () => {
  return (
    <div id="header">
      <img src={notificationIcon} style={{height: '40%', marginRight: '3vw'}}/>
    </div>
  )
};

export default Header;
