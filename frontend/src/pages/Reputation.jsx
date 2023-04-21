import React, { useState, useEffect } from "react";
import ReviewCard from '../components/ReviewCard';
import { makeRequest } from "../helpers";
import './Reputation.css';
import { useLocation } from 'react-router-dom';

const Reputation = ({ firebaseApp }) => {
  const [isLoading, setIsLoading] = useState('Loading...');
  const [reviews, setReviews] = useState();
  const [name, setName] = useState([]);
  const currentUser = firebaseApp.auth().currentUser;
  const location = useLocation();
  const viewee = location.pathname === "/reputation" ? currentUser.uid : location.pathname.split('/')[2];

  useEffect(async () => {
    const nameData = await makeRequest(`/achievements/name?uid=${viewee}`, 'GET', null, currentUser.uid);
    const data = await makeRequest(`/reputation/view_reputation?viewee_uid=${viewee}`, 'GET', null, currentUser.uid);
    if (data.error) alert(data.error);
    else {
      setName(nameData);
      setReviews(data);
      setIsLoading(false);
    }
  }, []);

  return (
    <div id="reputation-container">
      <div id="reputation-header">
        <h3 id="reuptation-title">{name.display_name}'s Reputation</h3>
      </div>
      {isLoading || (
        <div id="review-card-container">
          {reviews.reviews.map((review, idx) => {
            return <ReviewCard key={idx} review={review} uid={currentUser.uid}/>
          })}
        </div>
      )}
    </div>
  )
}

export default Reputation;
