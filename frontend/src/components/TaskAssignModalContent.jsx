import React, { forwardRef, useState, useEffect } from "react";
import { makeRequest } from "../helpers";

const TaskAssignModalContent = forwardRef((props, ref) => {
  const [buttonText, setButtonText] = useState("Assign");
  const emails = props.emails.join(", ");

  const handleSubmit = async (event) => {
    event.preventDefault();
    event.stopPropagation();

    if (buttonText === "...") return;
    setButtonText("...");

    const new_assignees = event.target.taskAssignees.value.split(", ");
    const data = await makeRequest('/task/assign', 'POST', {tid: props.tid, new_assignees}, props.uid);
    setButtonText("Assign");
    if (data.error) alert(data.error);
    else props.handleClose();
  }

  return (
    <form id="task-assign-modal" className="task-modal" onSubmit={handleSubmit}>
      <label htmlFor="taskAssignees"><h3 style={{margin: '0'}}>Assignee Emails</h3></label>
      <textarea id="taskAssignees" name="taskAssignees" placeholder="e.g. user@email.com" defaultValue={emails} />
      <br />
      <br />
      <button type="submit">{buttonText}</button>
    </form>
  );
});

export default TaskAssignModalContent;