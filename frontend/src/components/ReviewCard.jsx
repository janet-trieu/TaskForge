import React, { useState } from "react";
import userIcon from '../assets/default user icon.png';
import editIcon from '../assets/edit.png';
import { Modal } from "@mui/material";
import ReviewCardUpdateModal from './ReviewCardUpdateModal.jsx'

const ReviewCard = (props) => {
  const [open, setOpen] = useState(false);
  const handleOpen = () => { setOpen(true) };
  const handleClose = () => { setOpen(false) };

  let photo = props.review.photo;
  if (!photo) {
    photo = userIcon;
  }

  return (
    <div className="review-card">
      <div className="review-card-header">
        {location.pathname !== '/reputation' && props.review.reviewer_uid === props.uid &&
          <div className="edit-icon" onClick={handleOpen} style={{ cursor: 'pointer' }}>
            <img src={editIcon} />
          </div>
        }
        <div>{props.review.reviewer_name}'s Review</div>
        <div>{props.review.date}</div>
      </div>
      <div className="review-card-body">
        <div className="review-card-info">
          <div>{props.review.comment}</div>
        </div>
        <div className="review-card-reputation">
          <div>
            <div>Communication</div>
            <div>Time Management</div>
            <div>Task Quality</div>
          </div>
          <div>
            <div>{props.review.communication}</div>
            <div>{props.review.time_management}</div>
            <div>{props.review.task_quality}</div>
          </div>
        </div>
      </div>
      <Modal open={open} onClose={handleClose}>
        <ReviewCardUpdateModal review={props.review} onClose={handleClose} uid={props.uid}/>
      </Modal>
    </div>
  )
}

export default ReviewCard;
