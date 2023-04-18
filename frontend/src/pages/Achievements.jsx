import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import { makeRequest } from "../helpers";
import AchievementBlock from "../components/Achievement/AchievementBlock";
import AchievementLockedBlock from "../components/Achievement/AchievementLockedBlock";
import './Achievements.css'

const Achievements = ({ firebaseApp }) => {
  const location = useLocation();
  const [isLoading, setIsLoading] = useState("Loading...");
  const [achievements, setAchievements] = useState([]);
  const [locked, setLocked] = useState([]);
  const [name, setName] = useState([]);
  const [isUser, setIsUser] = useState()
  const uid = firebaseApp.auth().currentUser.uid;

  useEffect(async () => {
    if (location.pathname === '/achievements') {
      setIsUser(true);
      const data = await makeRequest('/achievements/view/my', 'GET', null, uid);
      const lockedData = await makeRequest(`/achievements/locked?uid=${uid}`, 'GET', null, uid);
      const nameData = await makeRequest(`/achievements/name?uid=${uid}`, 'GET', null, uid);
      if (data.error) alert(data.error);
      else {
        setAchievements(data);
        setIsLoading(false);
        setLocked(lockedData);
        setName(nameData);
      }
    } else {
      setIsUser(false);
      const requested_uid = location.pathname.split('/')[2];
      const data = await makeRequest('/achievements/view/notmy', 'GET', {conn_uid: requested_uid}, uid);
      const lockedData = await makeRequest(`/achievements/locked?uid=${requested_uid}`, 'GET', null, uid);
      const nameData = await makeRequest(`/achievements/name?uid=${requested_uid}`, 'GET', null, uid);
      if (data.error) alert(data.error);
      else {
        setAchievements(data);
        setIsLoading(false);
        setLocked(lockedData);
        setName(nameData);
      }
    }
  }, []);

  return (
    isLoading || (
      <div className="achievement-container">
        <div className="achievement-header">
          <h2>{name.display_name}'s Achievements</h2>
        </div>
        <div className="achievement-body">
          {achievements.map((achievement, idx) => {
            return <AchievementBlock key={idx} uid={uid} aid={achievement.aid} title={achievement.title} description={achievement.description} isUser={isUser} />
          })}
          {locked.map((lock, idx) => {
            return <AchievementLockedBlock key={idx} title={lock.title} description={lock.description} />
          })}
        </div>
      </div>
    )
  )
}

export default Achievements;
