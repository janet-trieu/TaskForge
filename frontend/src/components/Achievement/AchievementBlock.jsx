import React, { useState, useEffect } from "react";
import { makeRequest } from "../../helpers";
import './AchievementBlock.css'
import taskSilver from '../../assets/achievement-icons/task silver.png'
import taskGold from '../../assets/achievement-icons/task gold.png'
import projSilver from '../../assets/achievement-icons/proj silver.png'
import projGold from '../../assets/achievement-icons/proj gold.png'
import bnoc from '../../assets/achievement-icons/bnoc.png'
import octo from '../../assets/achievement-icons/octopus.png'
import wolf from '../../assets/achievement-icons/lone wolf.png'
import review from '../../assets/achievement-icons/review.png'

const AchievementBlock = ({ uid, aid, title, description, isUser }) => {
  const renderIcon = () => {
    switch (aid) {
      case 0:
        return taskSilver;
      case 1:
        return taskGold;
      case 2:
        return projSilver;
      case 3:
        return projGold;
      case 4:
        return bnoc;
      case 5:
        return octo;
      case 6:
        return wolf;
      case 7:
        return review;
      default:
        return null;
    }
  }

  const handleShare = async () => {
    const emails = prompt("Enter email addresses separated by commas:");
    const emailArray = emails.split(",");
    const data = await makeRequest("/achievements/share", "POST", { receiver_emails: emailArray, aid: aid }, uid);
    alert("Shared");
  };

  return (
    <div className="achievement-block">
      <div className="achievement-block-content">
        <img src={renderIcon()}></img>
        <div className="achievement-block-details">
          <div className="achievement-block-title">{title}</div>
          <div className="achievement-block-description">{description}</div>
          {isUser ? <button onClick={handleShare}>Share</button> : null}
        </div>
      </div>
    </div>
  )
}

export default AchievementBlock;
