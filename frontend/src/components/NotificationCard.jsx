import React from "react";
import './NotificationCard.css';

// connection request
// project invite
// leave request

const NotificationCard = ({ content }) => {
  const handleResponse = (response) => {

  }
  return (
    <div className="notification-card">
      <h4 style={{margin: '0'}}>{content.notification_msg}</h4>
      <div className={(content.type === 'welcome') ? "" : "hide"} style={{marginTop: '1em'}}>
        <button style={{backgroundColor: 'seagreen'}} onClick={() => handleResponse('accept')}>Accept</button>&nbsp;&nbsp;
        <button style={{backgroundColor: 'firebrick'}} onClick={() => handleResponse('decline')}>Decline</button>
      </div>
    </div>
  )
}

export default NotificationCard;
