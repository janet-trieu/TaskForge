import React, { forwardRef, useState } from "react";
import { makeRequest, fileToDataUrl } from "../helpers";
import defaultProjectIcon from "../assets/default project icon.png"

const ProjectModalContent = forwardRef((props, ref) => {
  const [icon, setIcon] = useState(props.details.picture);
  const [buttonText, setButtonText] = useState("Save Changes");
  
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

    if (buttonText === "...") return;
    setButtonText("...");

    const body = {
      pid: props.details.pid,
      updates: {
        name: event.target.name.value,
        description: event.target.description.value,
        due_date: event.target.dueDate.value,
        status: event.target.status.value,
        picture: icon
      }
    }

    if (!body.updates.name) {alert('Please enter a project name.'); setButtonText("Save Changes"); return;}
    if (!body.updates.description) {alert('Please enter a project type.'); setButtonText("Save Changes"); return;}
    if (body.updates.picture === defaultProjectIcon) {alert('Please upload a project icon.'); setButtonText("Save Changes"); return;}

    const data = await makeRequest("/projects/update", "POST", body, props.uid);
    setButtonText("Save Changes");
    if (data.code && data.code !== 200) alert(`${data.name}\n${data.message}`);
    else {
      let details = props.details;
      details.name = body.updates.name;
      details.description = body.updates.description;
      details.due_date = body.updates.due_date;
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

      <br />
      <br />
      <button type="submit">{buttonText}</button>
    </form>
  );
});

export default ProjectModalContent;