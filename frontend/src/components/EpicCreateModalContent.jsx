import React, { forwardRef } from "react";
import { makeRequest } from "../helpers";

const EpicCreateModalContent = forwardRef((props, ref) => {

  const handleSubmit = async (event) => {
    event.preventDefault();

    const body = {
      pid: Number(props.pid),
      title: event.target.title.value,
      description: event.target.description.value,
      colour: event.target.colour.value,
    }

    if (!body.title) { alert('Please enter an epic title.'); return; }
    if (!body.description) { alert('Please enter an epic description.'); return; }
    if (!body.colour) { alert('Please enter an epic colour.'); return; }

    const data = await makeRequest("/epic/create", "POST", body, props.uid);
    if (data.code && data.code !== 200) alert(`${data.name}\n${data.message}`);
    else {
      // insert epic to board??
      props.handleClose();
    }
  }

  return (
    <form id="project-modal" className="task-create-modal" onSubmit={handleSubmit}>
      <label htmlFor="title"><h3>Title</h3></label>
      <input type="text" id="title" name="title" style={{ width: '20em', marginTop: '0' }} placeholder="Add a task title..." />

      <label htmlFor="description"><h3>Description</h3></label>
      <textarea id="description" name="description" placeholder="Add a description..." />

      <label htmlFor="colour"><h3>Colour</h3></label>
      <div className="radio-group">
        <div className="radio">
          <input type="radio" id="red" name="colour" value="#ffadad" />
          <label htmlFor="red" style={{ color: "#ffadad", fontWeight:"bold" }}>Red</label>
        </div>
        <div className="radio">
          <input type="radio" id="yellow" name="colour" value="#ffee93" />
          <label htmlFor="yellow" style={{ color: "#ffee93", fontWeight:"bold" }}>Yellow</label>
        </div>
        <div className="radio">
          <input type="radio" id="green" name="colour" value="#c4e6a9" />
          <label htmlFor="green" style={{ color: "#c4e6a9", fontWeight:"bold" }}>Green</label>
        </div>
        <div className="radio">
          <input type="radio" id="blue" name="colour" value="#a3c4f3" />
          <label htmlFor="blue" style={{ color: "#a3c4f3", fontWeight:"bold" }}>Blue</label>
        </div>
        <div className="radio">
          <input type="radio" id="purple" name="colour" value="#bdb2ff" />
          <label htmlFor="purple" style={{ color: "#bdb2ff", fontWeight:"bold" }}>Purple</label>
        </div>
      </div>
      <br />
      <br />
      <button type="submit">Save Changes</button>
    </form>
  );
});

export default EpicCreateModalContent;