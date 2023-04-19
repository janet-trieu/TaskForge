import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { makeRequest, fileToDataUrl } from "../helpers";
import defaultProjectIcon from "../assets/default project icon.png"

const CreateProject = ({ firebaseApp }) => {
  const [icon, setIcon] = useState(defaultProjectIcon);
  const navigate = useNavigate();

  const uploadHandler = async (event) => {
    if (!event.target.files[0]) {
      setIcon(defaultProjectIcon);
    } else {
      const file = event.target.files[0];
      const dataUrl = await fileToDataUrl(file);
      if (!dataUrl) setIcon(defaultProjectIcon);
      else setIcon(dataUrl);
    }
  }
  const cancelButtonHandler = () => navigate('/projects');
  const createButtonHandler = async (event) => {
    event.preventDefault();

    const body = {
      name: event.target.name.value,
      description: event.target.description.value,
      due_date: null,
      status: null,
      picture: icon
    }

    if (!body.name) {alert('Please enter a project name.'); return;}
    if (!body.description) {alert('Please enter a project type.'); return;}
    if (body.picture === defaultProjectIcon) {alert('Please upload a project icon.'); return;}

    const uid = await firebaseApp.auth().currentUser.uid;
    const data1 = await makeRequest("/projects/create", "POST", body, uid);
    if (data1.error) alert(data1.error);
    else {
      if (event.target.invites.value) {
        const invites = event.target.invites.value.split(", ");
        const data2 = await makeRequest('/projects/invite', "POST", {receiver_emails: invites, pid: data1}, uid)
        if (data2.error) {alert(data2.error); return;}
      }
      
      alert('Project has been successfully created!');
      navigate('/projects');
    }
  };

  return (
    <div id='create-project-page'>
      <h2>Project Information</h2>
      <form onSubmit={createButtonHandler} id='create-project-form'>
        <div id='project-create-icon-container'>
          <div className="project-icon-container"><img className="project-icon" src={icon}></img></div>
          <label htmlFor="project-icon-upload">Upload icon</label>
          <input type="file" id="project-icon-upload" className="hide" onChange={uploadHandler} />
        </div>
        <br />
        <label htmlFor='project-name'>Project Name</label><br />
        <input type='text' name='name' id='project-name' /><br />
        <br />
        <label htmlFor='project-description'>Project Description</label><br />
        <input type='text' name='description' id='project-description' placeholder="e.g. Software Project" /><br />
        <br />
        <label htmlFor='project-invite'>Invite People to Project</label><br />
        <p style={{fontSize: '0.8em', margin: '0'}}>Must be a list of emails separated by a comma and a space ", "</p>
        <input type='text' name='invites' id='project-invite' placeholder="e.g. user1@email.com, user2@email.com, ..."/><br />
        <br />
        <button style={{backgroundColor: 'gray'}} onClick={cancelButtonHandler}>Cancel</button>
        &nbsp;&nbsp;
        <button type='submit'>Create</button>
      </form>
    </div>
  )
}

export default CreateProject;
