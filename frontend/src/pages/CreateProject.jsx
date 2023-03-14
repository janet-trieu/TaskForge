import React from "react";
import { useNavigate } from "react-router-dom";
import { makeRequest } from "../helpers";

const CreateProject = ({ firebaseApp }) => {
  const navigate = useNavigate();
  const cancelButtonHandler = () => navigate('/projects');
  const createButtonHandler = async (event) => {
    event.preventDefault();
    
    const body = {
      name: event.target.name.value,
      type: event.target.type.value,
      invites: event.target.invites.value
    }

    if (!body.name) {alert('Please enter a project name.'); return;}
    if (!body.type) {alert('Please enter a project type.'); return;}

    const data = await makeRequest("/createproject", "POST", body, firebaseApp.auth().currentUser.id);
    if (data.error) alert(data.error);
    else { 
      alert('Project has been successfully created!')
      navigate('/projects');
    }
  };
  
  return (
    <div id='create-project-page'>
      <h2>Project Information</h2>
      <form onSubmit={createButtonHandler} id='create-project-form'>
        <label htmlFor='project-name'>Project Name</label><br />
        <input type='text' name='name' id='project-name' /><br />
        <br />
        <label htmlFor='project-type'>Project Type</label><br />
        <input type='text' name='type' id='project-type' placeholder="e.g. Software Project" /><br />
        <br />
        <label htmlFor='project-invite'>Invite People to Project</label><br />
        <input type='text' name='invites' id='project-invite' /><br />
        <br />
        <button onClick={cancelButtonHandler}>Cancel</button> &nbsp; <button type='submit'>Create</button>
      </form>
    </div>
  )
}

export default CreateProject;
