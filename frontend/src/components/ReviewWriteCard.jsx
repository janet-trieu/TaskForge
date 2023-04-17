import React from "react";

const ReviewWriteCard = (props) => {

  return (
      <form className="review-card">
        <div className="review-card-header">
          <div>Write a Review</div>
        </div>
        <div className="review-card-body">
          <div className="review-card-info">
            <label>Task Description</label><br />
            <input id="" />
            <label>Optional Comment</label><br />
            <input />
          </div>
          <div className="review-card-reputation">
            <div>
              <label>Communication</label>
              <label>Time Management</label>
              <label>Task Quality</label>
            </div>
            <div>
              <input />
              <input />
              <input />
            </div>
          </div>
        </div>
      </form>
    )
}

export default ReviewWriteCard;
