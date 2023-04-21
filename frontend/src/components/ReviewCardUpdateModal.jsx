import React, { forwardRef, useState } from "react";
import { makeRequest } from "../helpers";
import './ReviewCardUpdateModal.css'

const ReviewCardUpdateModal = forwardRef((props, ref) => {
  const [buttonText, setButtonText] = useState("Update Review");

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (buttonText === "...") return;
    setButtonText("...");

    const body = {
      reviewee_uid: props.review.reviewee_uid,
      pid: Number(props.review.pid),
      communication: event.target.communication.value,
      time_management: event.target.timeManagement.value,
      task_quality: event.target.taskQuality.value,
      comment: event.target.comment.value
    }

    const data = await makeRequest("/reputation/update_review", "POST", body, props.uid);
    setButtonText("Update Review");
    if (data.code && data.code !== 200) alert(`${data.name}\n${data.message}`);
    else props.onClose();
  }

  return (
    <form id="reputation-modal" onSubmit={handleSubmit}>
      <br />
      <span style={{ display: "inline-block", width: "15em" }}><label htmlFor='communication'><h3 style={{ marginBottom: "0", display: 'inline' }}>Communication</h3></label></span>
      <select name='communication' id='communication' defaultValue={props.review.communication}>
        <option value={1}>1</option>
        <option value={2}>2</option>
        <option value={3}>3</option>
        <option value={4}>4</option>
        <option value={5}>5</option>
      </select>
      <br />
      <br />
      <span style={{ display: "inline-block", width: "15em" }}><label htmlFor='timeManagement'><h3 style={{ marginBottom: "0", display: 'inline' }}>Time Management</h3></label></span>
      <select name='timeManagement' id='timeManagement' defaultValue={props.review.time_management}>
        <option value={1}>1</option>
        <option value={2}>2</option>
        <option value={3}>3</option>
        <option value={4}>4</option>
        <option value={5}>5</option>
      </select>
      <br />
      <br />
      <span style={{ display: "inline-block", width: "15em" }}><label htmlFor='taskQuality'><h3 style={{ marginBottom: "0", display: 'inline' }}>Task Quality</h3></label></span>
      <select name='taskQuality' id='taskQuality' defaultValue={props.review.task_quality}>
        <option value={1}>1</option>
        <option value={2}>2</option>
        <option value={3}>3</option>
        <option value={4}>4</option>
        <option value={5}>5</option>
      </select>
      <label htmlFor='comment'><h3 style={{ marginBottom: "0" }}>Optional Comment</h3></label><br />
      <textarea name='remove' id='comment' placeholder="Enter a commment..." defaultValue={props.review.comment} />
      <br />
      <br />
      <button type="submit">{buttonText}</button>&nbsp;&nbsp;
      <button onClick={() => props.onClose()} style={{ backgroundColor: 'gray' }}>Cancel</button>
    </form>
  );
});

export default ReviewCardUpdateModal;
