import React, { forwardRef } from "react";
import { makeRequest } from "../helpers";

const ProjectInviteModalContent = forwardRef((props, ref) => {
  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!event.target.invites.value) {alert("Please enter at least one member email."); return;}
    const invites = event.target.invites.value.split(", ");
    const data = await makeRequest('/projects/invite', "POST", {receiver_emails: invites, pid: Number(props.pid)}, props.uid);

    if (data.code && data.code !== 200) alert(`${data.name}\n${data.message}`);
    else props.handleClose();
  }

  return (
    <form id="project-modal" onSubmit={handleSubmit}>
      <label htmlFor='project-invite'>
        <h3 style={{marginBottom: '0'}}>Invite People to Project</h3>
        <p style={{ margin: '0'}}>Must be a list of emails separated by a comma and a space ", "</p>
      </label>
      <input type='text' name='invites' id='project-invite' placeholder="e.g. user1@email.com, user2@email.com, ..." style={{width: '35em'}}/>
      <br />
      <br />
      <button type="submit">Send Invites</button>&nbsp;&nbsp;
      <button onClick={() => props.handleClose()} style={{backgroundColor: 'gray'}}>Cancel</button>
    </form>
  );
});

export default ProjectInviteModalContent;