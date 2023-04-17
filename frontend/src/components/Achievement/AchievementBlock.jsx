import React from "react";
import './AchievementBlock.css'
import taskSilver from '../../assets/achievement-icons/task silver.png'
import taskGold from '../../assets/achievement-icons/task gold.png'
import projSilver from '../../assets/achievement-icons/proj silver.png'
import projGold from '../../assets/achievement-icons/proj gold.png'
import bnoc from '../../assets/achievement-icons/bnoc.png'
import octo from '../../assets/achievement-icons/octopus.png'
import wolf from '../../assets/achievement-icons/lone wolf.png'
import review from '../../assets/achievement-icons/review.png'

const AchievementBlock = ({aid, title, description}) => {
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

  return (
    <div className="achievement-block">
      <div className="achievement-block-content">
        <img src={renderIcon()}></img>
        <div className="achievement-block-details">
          <div className="achievement-block-title">{title}</div>
          <div className="achievement-block-description">{description}</div>
        </div>
      </div>
    </div>
  )
}

export default AchievementBlock;
