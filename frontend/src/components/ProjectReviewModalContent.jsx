import React, { forwardRef } from "react";
import { makeRequest } from "../helpers";

const ProjectReviewModalContent = forwardRef((props, ref) => {

  const idx = props.memberUids.findIndex((member) => {return member === props.uid});
  const memberNames = props.memberNames.toSpliced(idx, 1);
  const memberUids = props.memberUids.toSpliced(idx, 1);

  const handleSubmit = async (event) => {
    event.preventDefault();

    const body= {
      reviewee_uid: event.target.reviewee.value,
      pid: Number(props.pid),
      communication: event.target.communication.value,
      time_management: event.target.timeManagement.value,
      task_quality: event.target.taskQuality.value,
      comment: event.target.comment.value
    }

    const data = await makeRequest("/reputation/add_review", "POST", body, props.uid)
    if (data.code && data.code !== 200) alert(`${data.name}\n${data.message}`);
    else props.handleClose();
  }

  return (
    <form id="project-modal" onSubmit={handleSubmit}>
      <label htmlFor='reviewee'><h3 style={{marginBottom: "0"}}>Reviewee</h3></label>
      <select name='reviewee' id='reviewee'>
        <option value={false}>Choose a user...</option>
        {memberNames.map((name, idx) => {return <option key={idx} value={memberUids[idx]}>{name}</option>})}
      </select>
      <br />
      <br />
      <span style={{display: "inline-block", width: "15em"}}><label htmlFor='communication'><h3 style={{marginBottom: "0", display: 'inline'}}>Communication</h3></label></span>
      <select name='communication' id='communication'>
        <option value={1}>1</option>
        <option value={2}>2</option>
        <option value={3}>3</option>
        <option value={4}>4</option>
        <option value={5}>5</option>
      </select>
      <br />
      <br />
      <span style={{display: "inline-block", width: "15em"}}><label htmlFor='timeManagement'><h3 style={{marginBottom: "0", display: 'inline'}}>Time Management</h3></label></span>
      <select name='timeManagement' id='timeManagement'>
        <option value={1}>1</option>
        <option value={2}>2</option>
        <option value={3}>3</option>
        <option value={4}>4</option>
        <option value={5}>5</option>
      </select>
      <br />
      <br />
      <span style={{display: "inline-block", width: "15em"}}><label htmlFor='taskQuality'><h3 style={{marginBottom: "0", display: 'inline'}}>Task Quality</h3></label></span>
      <select name='taskQuality' id='taskQuality'>
        <option value={1}>1</option>
        <option value={2}>2</option>
        <option value={3}>3</option>
        <option value={4}>4</option>
        <option value={5}>5</option>
      </select>
      <label htmlFor='comment'><h3 style={{marginBottom: "0"}}>Optional Comment</h3></label><br />
      <textarea name='remove' id='comment' placeholder="Enter a commment..." />
      <br />
      <br />
      <button type="submit">Send Review</button>&nbsp;&nbsp;
      <button onClick={() => props.handleClose()} style={{backgroundColor: 'gray'}}>Cancel</button>
    </form>
  );
});

export default ProjectReviewModalContent;
