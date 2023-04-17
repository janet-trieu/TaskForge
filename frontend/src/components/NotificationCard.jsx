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
      data = await makeRequest('/connections/request_respond', 'POST', { nid: content.nid, response: response === "accept" }, uid);
    } else if (content.type === "project_invite") {
      const body = {
        pid: content.pid,
        accept: response === "accept",
        msg: response === "accept" ? "The user has accepted." : "The user has declined."
      }
      data = await makeRequest('/projects/invite/respond', 'POST', body, uid);
    } else {
      if (response === "accept") {
        data = await makeRequest('/projects/remove', 'POST', { pid: content.pid, uid_to_be_removed: content.uid_sender }, uid);
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

  const handleShare = async () => {
    const emails = prompt("Enter email addresses separated by commas:");
    const emailArray = emails.split(",");
    const data = await makeRequest("/achievements/share", "POST", { receiver_emails: emailArray, aid: content.aid }, uid);
    alert("Shared");
  };

  const handleDeleteNotification = async () => {
    await makeRequest('/notifications/clear', 'DELETE', { nid: content.nid }, uid)
  }
  return (
    <div className="notification-card">
      <h4 style={{ margin: '0' }}>{content.notification_msg}</h4>
      <div className={show ? "" : "hide"} style={{ marginTop: '1em' }}>
        <button style={{ backgroundColor: 'seagreen' }} onClick={() => handleResponse('accept')}>Accept</button>&nbsp;&nbsp;
        <button style={{ backgroundColor: 'firebrick' }} onClick={() => handleResponse('decline')}>Decline</button>
      </div>
      <div className={hasResponded ? "" : "hide"} >
        <p>You chose to {hasResponded}.</p>
      </div>
      <button onClick={handleDeleteNotification}>Delete</button>
      {content.type === "achievement" && (
        <button onClick={handleShare}>Share</button>
      )}
    </div>
  )
}

export default NotificationCard;
