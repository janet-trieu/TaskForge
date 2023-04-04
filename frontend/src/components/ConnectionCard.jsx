import React from "react";
import './ConnectionCard.css';
import userIcon from '../assets/default user icon.png';
import { useNavigate } from "react-router-dom";

const ConnectionCard = ({ photo, displayName, role, uid }) => {
  const navigate = useNavigate();

  if (!photo) {
    photo = userIcon
  }

  return (
      <div className="connection-card" onClick={() => navigate(`/profile/${uid}`)}>
        <img src={photo}></img>
        <div className="connection-card-info">
          <div style={{fontWeight: 'bold'}}>{displayName}</div>
          <div style={{color: 'gray'}}>{role}</div>
        </div>
      </div>
    )
}

export default ConnectionCard;
