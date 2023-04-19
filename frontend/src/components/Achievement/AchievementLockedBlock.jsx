import React from "react";
import './AchievementBlock.css'
import lockIcon from '../../assets/achievement-icons/locked.png'

const AchievementBlock = ({ title, description}) => {

  return (
    <div className="achievement-block">
      <div className="achievement-block-content">
        <img src={lockIcon}></img>
        <div className="achievement-block-details">
          <div className="achievement-block-title">{title}</div>
          <div className="achievement-block-description">{description}</div>
        </div>
      </div>
    </div>
  )
}

export default AchievementBlock;
