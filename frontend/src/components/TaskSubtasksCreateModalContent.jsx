import React, { forwardRef, useState } from "react";
import { makeRequest } from "../helpers";

const TaskSubtasksCreateModalContent = forwardRef((props, ref) => {

  const handleSubmit = async (event) => {
    event.preventDefault();
    event.stopPropagation();
    const assigneesValue = event.target.assignees.value;
    const assignees = assigneesValue ? assigneesValue.split(", ") : [];
    const body = {
      pid: Number(props.pid),
      tid: Number(props.tid),
      assignees,
      title: event.target.title.value,
      description: event.target.description.value,
      deadline: event.target.deadline.value,
      workload: event.target.workload.value,
      priority: event.target.priority.value,
      status: event.target.status.value
    }

    if (!body.title) {alert('Please enter a subtask title.'); return;}
    if (!body.description) {alert('Please enter a subtask description.'); return;}

    const data = await makeRequest("/subtask/create", "POST", body, props.uid);
    if (data.code && data.code !== 200) alert(`${data.name}\n${data.message}`);
    else {
      // const newTasks = props.tasks;
      // newTasks[body.status].unshift(data);
      // props.setTasks(newTasks);
      props.handleClose();
    }
  }

  return (
    <form id="project-modal" className="task-create-modal" onSubmit={handleSubmit}>
      <label htmlFor="title"><h3>Title</h3></label>
      <input type="text" id="title" name="title" style={{width: '20em', marginTop: '0'}} placeholder="Add a subtask title..." />

      <label htmlFor="description"><h3>Description</h3></label>
      <textarea id="description" name="description" placeholder="Add a description..." />

      <label htmlFor="deadline"><h3>Deadline</h3></label>
      <input type="text" id="deadline" name="deadline" style={{width: '20em', marginTop: '0'}} placeholder="DD/MM/YYYY" />

      <label htmlFor='status'><h3 style={{marginBottom: "0"}}>Status</h3></label>
      <select name='status' id='status'>
        <option value="Not Started">Not Started</option>
        <option value="In Progress">In Progress</option>
        <option value="In Review/Testing">In Review/Testing</option>
        <option value="Blocked">Blocked</option>
        <option value="Completed">Completed</option>
      </select>

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

export default TaskSubtasksCreateModalContent;