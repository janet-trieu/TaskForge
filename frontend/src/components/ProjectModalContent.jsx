import React, { forwardRef, useState } from "react";
import { makeRequest, fileToDataUrl } from "../helpers";
import defaultProjectIcon from "../assets/default project icon.png"

const ProjectModalContent = forwardRef((props, ref) => {
  const [icon, setIcon] = useState(props.details.picture);
  
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

  const handleSubmit = async (event) => {
    event.preventDefault();

    const body = {
      pid: props.details.pid,
      updates: {
        name: event.target.name.value,
        description: event.target.description.value,
        due_date: event.target.dueDate.value,
        team_strength: Number(event.target.teamStrength.value),
        status: event.target.status.value,
        picture: icon
      }
    }

    if (!body.updates.name) {alert('Please enter a project name.'); return;}
    if (!body.updates.description) {alert('Please enter a project type.'); return;}
    if (body.updates.picture === defaultProjectIcon) {alert('Please upload a project icon.'); return;}

    const data = await makeRequest("/projects/update", "POST", body, props.uid);
    if (data.code && data.code !== 200) alert(`${data.name}\n${data.message}`);
    else {
      let details = props.details;
      details.name = body.updates.name;
      details.description = body.updates.description;
      details.due_date = body.updates.due_date;
      details.team_strength = body.updates.team_strength;
      details.status = body.updates.status;
      details.picture = body.updates.picture;
      props.setDetails(details);
      props.handleClose();
    }
  }

  return (
    <form id="project-modal" onSubmit={handleSubmit}>
      <h3>Icon</h3>
        <div id='project-create-icon-container'>
          <div className="project-icon-container"><img className="project-icon" src={icon}></img></div>
          <label htmlFor="project-icon-upload">Change icon</label>
          <input type="file" id="project-icon-upload" className="hide" onChange={uploadHandler} />
        </div>

        <label htmlFor="name"><h3>Name</h3></label>
        <input type="text" id="name" name="name" style={{width: '20em', marginTop: '0'}} defaultValue={props.details.name}/>

        <label htmlFor="description"><h3>Description</h3></label>
        <textarea id="description" name="description" placeholder="Add a description..." defaultValue={props.details.description}></textarea>

        <h3>Status</h3>
        <div id="radio-group">
          <div className="radio">
            <input type="radio" id="notStarted" name="status" defaultChecked={"Not Started" === props.details.status} value="Not Started"/>
            <label htmlFor="notStarted">Not Started</label>
          </div>
          <div className="radio">
            <input type="radio" id="inProgress" name="status" defaultChecked={"In Progress" === props.details.status} value="In Progress"/>
            <label htmlFor="inProgress">In Progress</label>
          </div>
          <div className="radio">
            <input type="radio" id="inReview" name="status" defaultChecked={"In Review" === props.details.status} value="In Review"/>
            <label htmlFor="inReview">In Review/Testing</label>
          </div>
          <div className="radio">
            <input type="radio" id="completed" name="status" defaultChecked={"Completed" === props.details.status} value="Completed"/>
            <label htmlFor="completed">Completed</label>
          </div>
          <div className="radio">
            <input type="radio" id="blocked" name="status" defaultChecked={"Blocked" === props.details.status} value="Blocked"/>
            <label htmlFor="blocked">Blocked</label>
          </div>
        </div>

        <label htmlFor="dueDate"><h3>Due Date</h3></label>
        <input type="text" id="dueDate" name="dueDate" style={{width: '20em', marginTop: '0'}} placeholder="DD/MM/YYYY" defaultValue={props.details.due_date}/>

        <label htmlFor="teamStrength"><h3>Team Strength</h3></label>
        <input type="text" id="teamStrength" name="teamStrength" style={{width: '20em', marginTop: '0'}} placeholder="Add a team strength..." defaultValue={props.details.team_strength}/>
        <br />
        <br />
        <button type="submit">Save Changes</button>
    </form>
  );
});

export default ProjectModalContent;