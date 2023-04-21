import React, { forwardRef, useState, useEffect } from "react";
import { useLocation } from 'react-router-dom';
import { makeRequest } from "../helpers";
import './NotificationModalContent.css';
import NotificationCard from "./NotificationCard";

const NotificationModalContent = forwardRef((props, ref) => {
  const [isLoading, setIsLoading] = useState('Loading...');
  const [data, setData] = useState();
  const location = useLocation();

  const handleClearNotifications = async () => {
    const response = await makeRequest('/notifications/clearall', 'DELETE', null, props.firebaseApp.auth().currentUser.uid)
    if (response && response.error) alert(response.error);
    else setData([]);
  };

  useEffect(async () => {
    const data = await makeRequest('/notifications/get', 'GET', null, props.firebaseApp.auth().currentUser.uid);
    if (data && data.error) alert(data.error);
    else {
      setData(data);
      setIsLoading(false);
    }
  }, [location])

  return (
    <div id="notifications-modal">
      {isLoading || (
        <>
          <button id="clear-button" onClick={handleClearNotifications}>Clear all notifications</button>
          {data.map((info, idx) => {
            return <NotificationCard key={idx} content={info} uid={props.firebaseApp.auth().currentUser.uid} />
          })}
        </>
      )}
    </div>
  );
});

export default NotificationModalContent;