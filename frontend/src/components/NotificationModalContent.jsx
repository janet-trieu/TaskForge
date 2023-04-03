import React, { forwardRef, useState, useEffect } from "react";
import { useLocation } from 'react-router-dom';
import { makeRequest } from "../helpers";
import './NotificationModalContent.css';
import NotificationCard from "./NotificationCard";

const NotificationModalContent = forwardRef((props, ref) => {
  const [isLoading, setIsLoading] = useState('Loading...');
  const [data, setData] = useState();
  const location = useLocation();

  useEffect(async () => {
    const data = await makeRequest('/notifications/get', 'GET', null, props.uid);
    if (data.error) alert(data.error);
    else {
      setData(data);
      setIsLoading(false);
    }
  }, [location])

  return (
    <div id="notifications-modal">
      {/* {isLoading || (
        data.map((info) => {
          return <div>{info.notification_msg}</div>
        })
      )} */}
      <NotificationCard />
      <NotificationCard />
      <NotificationCard />
      <NotificationCard />
      <NotificationCard />
      <NotificationCard />
      <NotificationCard />
      <NotificationCard />
      <NotificationCard />
    </div>
  );
});

export default NotificationModalContent;