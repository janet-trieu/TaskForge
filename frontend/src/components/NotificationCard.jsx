import React, { useState } from "react";
import './NotificationCard.css';
import { makeRequest } from '../helpers.js';

const actionTypes = ["connection_request", "project_invite", "leave_request"];

const NotificationCard = ({ content, uid }) => {
  const [show, setShow] = useState(actionTypes.includes(content.type));
  const [hasResponded, setHasResponded] = useState(false);

  const handleResponse = async (response) => {
    let data = null;
    if (content.type === "connection_request") {
      data = await makeRequest('/connections/request_respond', 'POST', {nid: content.nid, response: response === "accept"}, uid);
    } else if (content.type === "project_invite") {
      const body = {
        pid: content.pid,
        accept: response === "accept",
        msg: response === "accept" ? "The user has accepted." : "The user has declined."
      }
      data = await makeRequest('/projects/invite/respond', 'POST', body, uid);
    } else {
      if (response === "accept") {
        data = await makeRequest('/projects/remove', 'POST', {pid: content.pid, uid_to_be_removed: content.uid_sender}, uid);
      } else {
        data = {};
      }
    }
    if (data.error) alert(data.error);
    else {
      setShow(false);
      setHasResponded(response);
    }
  }
  return (
    <div className="notification-card">
      <h4 style={{margin: '0'}}>{content.notification_msg}</h4>
      <div className={show ? "" : "hide"} style={{marginTop: '1em'}}>
        <button style={{backgroundColor: 'seagreen'}} onClick={() => handleResponse('accept')}>Accept</button>&nbsp;&nbsp;
        <button style={{backgroundColor: 'firebrick'}} onClick={() => handleResponse('decline')}>Decline</button>
      </div>
      <div className={hasResponded ? "" : "hide"} >
        <p>You chose to {hasResponded}.</p>
      </div>
    </div>
  )
}

export default NotificationCard;
