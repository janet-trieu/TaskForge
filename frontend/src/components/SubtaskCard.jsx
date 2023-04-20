import React, { useState } from "react";
import { makeRequest } from "../helpers";

const SubtaskCard = (props) => {
  const [buttonText, setButtonText] = useState("Update");
  const assignees = props.subtask.assignees && props.subtask.assignees !== "" ? props.subtask.assignees.join("\n") : "";

  const handleSubmit = async (event) => {
    event.preventDefault();
    event.stopPropagation();

    if (buttonText === "...") return;
    setButtonText("...");

    let newAssignees = event.target.assignees.value.split("\n");
    if (newAssignees[0] === "") newAssignees = [];

    const body = {
      pid: props.pid,
      stid: props.subtask.stid,
      title: event.target.title.value,
      description: event.target.description.value,
      deadline: event.target.deadline.value,
      workload: event.target.workload.value,
      priority: event.target.priority.value,
      status: event.target.status.value,
      assignees: newAssignees
    }

    const data = await makeRequest("/subtask/update", "POST", body, props.uid);
    setButtonText("Update");
    if (data && data.code && data.code !== 200) alert(data.message);
    // else alert(`Subtask ${props.subtask.stid} updated!`);
  }

  return (
    <form className="subtask-card" onSubmit={handleSubmit}>
      <div>{props.subtask.stid}</div>
      <textarea id="title" name="title" defaultValue={props.subtask.title}/>
      <textarea id="description" name="description" defaultValue={props.subtask.description}/>
      <select id="status" name="status" defaultValue={props.subtask.status}>
        <option value="Not Started">Not Started</option>
        <option value="In Progress">In Progress</option>
        <option value="In Review/Testing">In Review/Testing</option>
        <option value="Blocked">Blocked</option>
        <option value="Completed">Completed</option>
      </select>
      <textarea id="assignees" name="assignees" defaultValue={assignees} placeholder="One email per line..."/>
      <input type="text" id="deadline" name="deadline" defaultValue={props.subtask.deadline} placeholder="DD/MM/YYY"/>
      <input type="text" id="workload" name="workload" defaultValue={props.subtask.workload} placeholder="Workload..." style={{width: "2em"}}/>
      <select id="priority" name="priority" defaultValue={props.subtask.priority}>
        <option value="">No priority</option>
        <option value="Low">Low</option>
        <option value="Moderate">Moderate</option>
        <option value="High">High</option>
      </select>
      <button type="submit">{buttonText}</button>
    </form>
  )
}

export default SubtaskCard;