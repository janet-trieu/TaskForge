import React, { forwardRef } from "react";
import { makeRequest } from "../helpers";

const ProjectModalContent = forwardRef((props, ref) => {

  const epicList = []
  for (const epic of props.epics) {
    epicList.push(<select value={epic.title}>{epic.title}</select>);
  }

  const handleSubmit = async (event) => {
    event.preventDefault();
    const assigneesValue = event.target.assignees.value;
    const assignees = assigneesValue ? assigneesValue.split(", ") : [];
    let eid = null;
    for (const epic of props.epics) {
      if (epic.title === event.target.epics.value) {eid = epic.eid};
    }
    const body = {
      pid: Number(props.pid),
      eid,
      assignees,
      title: event.target.title.value,
      description: event.target.description.value,
      deadline: event.target.deadline.value,
      workload: event.target.workload.value,
      priority: event.target.priority.value,
      status: event.target.status.value
    }

    if (!body.title) {alert('Please enter a task title.'); return;}
    if (!body.description) {alert('Please enter a task description.'); return;}

    const data = await makeRequest("/task/create", "POST", body, props.uid);
    if (data.code && data.code !== 200) alert(`${data.name}\n${data.message}`);
    else {
      // insert task to board??
      props.handleClose();
    }
  }

  return (
    <form id="project-modal" className="task-create-modal" onSubmit={handleSubmit}>
      <label htmlFor="title"><h3>Title</h3></label>
      <input type="text" id="title" name="title" style={{width: '20em', marginTop: '0'}} placeholder="Add a task title..." />

      <label htmlFor="description"><h3>Description</h3></label>
      <textarea id="description" name="description" placeholder="Add a description..." />

      <label htmlFor="epic"><h3>Epic</h3></label>
      <select id="epic" name="epic">
        <option value="">Choose an epic...</option>
        {epicList.map((epic) => {return epic})}
      </select>

      <label htmlFor="deadline"><h3>Deadline</h3></label>
      <input type="text" id="deadline" name="deadline" style={{width: '20em', marginTop: '0'}} placeholder="DD/MM/YYYY" />

      <h3>Status</h3>
      <div id="radio-group">
        <div className="radio">
          <input type="radio" id="notStarted" name="status" value="Not Started"/>
          <label htmlFor="notStarted">Not Started</label>
        </div>
        <div className="radio">
          <input type="radio" id="inProgress" name="status" value="In Progress"/>
          <label htmlFor="inProgress">In Progress</label>
        </div>
        <div className="radio">
          <input type="radio" id="inReview" name="status" value="In Review/Testing"/>
          <label htmlFor="inReview">In Review/Testing</label>
        </div>
        <div className="radio">
          <input type="radio" id="completed" name="status" value="Completed"/>
          <label htmlFor="completed">Completed</label>
        </div>
        <div className="radio">
          <input type="radio" id="blocked" name="status" value="Blocked"/>
          <label htmlFor="blocked">Blocked</label>
        </div>
      </div>

      <label htmlFor="assignees"><h3>Assignees</h3></label>
      <input type="text" id="assignees" name="assignees" style={{width: '20em', marginTop: '0'}} placeholder="e.g. user1@email.com, user2@email.com, ..." />
      
      <label htmlFor="workload"><h3>Workload</h3></label>
      <input type="text" id="workload" name="workload" style={{width: '20em', marginTop: '0'}} placeholder="Add a workload..." />

      <label htmlFor="priority"><h3>Priority</h3></label>
      <input type="text" id="priority" name="priority" style={{width: '20em', marginTop: '0'}} placeholder="Add a priority..." />
      
      <br />
      <br />
      <button type="submit">Save Changes</button>
    </form>
  );
});

export default ProjectModalContent;