import React from "react";

const ReviewWriteCard = (props) => {

  return (
      <form className="review-write-card">
        <div className="review-write-card-header">
          <div>Write a Review</div>
        </div>
        <div className="review-write-card-body">
          <div className="review-write-card-info">
            <label>Task Description</label><br />
            <input id="" />
            <label>Optional Comment</label><br />
            <input />
          </div>
          <div className="review-write-card-reputation">
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
