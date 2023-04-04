import React, { forwardRef } from "react";
import { makeRequest } from "../helpers";

const ProjectRemoveModalContent = forwardRef((props) => {
  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!event.target.remove.value) {
        alert("Please enter a UID.");
        return;
    }
    const data = await makeRequest("/projects/remove", "POST", {pid: Number(props.pid), uid_to_be_removed: event.target.remove.value}, props.uid)
    if (data.error) alert(data.error);
    else props.handleClose();
  }

  return (
    <form id="project-modal" onSubmit={handleSubmit}>
      <label htmlFor='project-remove'>
        <h3 style={{marginBottom: '0'}}>Remove Members from Project</h3>
        <p style={{ margin: '0'}}>Must be the user's ID</p>
      </label>
      <br />
      <input type='text' name='remove' id='project-remove' placeholder="Enter UID" style={{width: '35em'}}/>
      <br />
      <br />
      <button type="submit">Remove</button>&nbsp;&nbsp;
      <button onClick={() => props.handleClose()} style={{backgroundColor: 'gray'}}>Cancel</button>
    </form>
  );
});

export default ProjectRemoveModalContent;