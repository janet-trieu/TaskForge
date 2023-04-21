import React, { forwardRef, useState } from "react";
import { makeRequest } from "../helpers";

const ProjectRemoveModalContent = forwardRef((props, ref) => {
  const [buttonText, setButtonText] = useState("Remove");
  const handleSubmit = async (event) => {
    event.preventDefault();
    if (buttonText === "...") return;
    if (!event.target.remove.value) {
        alert("Please enter an email.");
        return;
    }
    
    const emailRegex = /^\S+@\S+\.\S+$/;
    const inputValue = event.target.remove.value.trim();
    if (!emailRegex.test(inputValue)) {
      alert("Please enter a valid email address.");
      return;
    }

    setButtonText("...");
    const data = await makeRequest("/projects/remove", "POST", {pid: Number(props.pid), email_removed: event.target.remove.value}, props.uid)
    setButtonText("Remove");
    if (data.error) alert(data.error);
    else props.handleClose();
  }

  return (
    <form id="project-modal" onSubmit={handleSubmit}>
      <label htmlFor='project-remove'>
        <h3 style={{marginBottom: '0'}}>Remove Members from Project</h3>
      </label>
      <input type='text' name='remove' id='project-remove' placeholder="Enter email" style={{width: '35em'}}/>
      <br />
      <br />
      <button type="submit">{buttonText}</button>&nbsp;&nbsp;
      <button onClick={() => props.handleClose()} style={{backgroundColor: 'gray'}}>Cancel</button>
    </form>
  );
});

export default ProjectRemoveModalContent;