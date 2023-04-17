import React from "react";
import userIcon from '../assets/default user icon.png';

const ReviewCard = (props) => {
  let photo = props.review.photo;
  if (!photo) {
    photo = userIcon;
  }

  const isWriter = props.review.reviewer_uid === props.uid;

  return (
      <div className="review-card">
        <div className="review-card-header">
          <div>{props.review.display_name}'s Review</div>
          <div>{props.review.date}</div>
        </div>
        <div className="review-card-body">
          <div className="review-card-info">
            <div>Task Description</div>
            <div>Optional Comment</div>
          </div>
          <div className="review-card-reputation">
            <div>
              <div>Communication</div>
              <div>Time Management</div>
              <div>Task Quality</div>
            </div>
            <div>
              <div>##.#</div>
              <div>##.#</div>
              <div>##.#</div>
            </div>
          </div>
        </div>
      </div>
    )
}

export default ReviewCard;
