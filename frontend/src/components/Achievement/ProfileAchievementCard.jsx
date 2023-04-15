import React from "react";
import './ProfileAchievementCard.css';

import taskSilver from '../../assets/achievement-icons/task silver.png'
import taskGold from '../../assets/achievement-icons/task gold.png'
import projSilver from '../../assets/achievement-icons/proj silver.png'
import projGold from '../../assets/achievement-icons/proj gold.png'
import bnoc from '../../assets/achievement-icons/bnoc.png'
import octo from '../../assets/achievement-icons/octopus.png'
import wolf from '../../assets/achievement-icons/lone wolf.png'
import review from '../../assets/achievement-icons/review.png'

const ProfileAchievementCard = ({ aid, title }) => {
  const renderIcon = () => {
    aid = 1;
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

  return (
    <div className="achievement-card">
      <div className="achievement-content">
        <img src={renderIcon()}></img>
        <div className="achievement-title">I also leave google restaurant reviews{title}</div>
      </div>
    </div>
  )
}

export default ProfileAchievementCard;
