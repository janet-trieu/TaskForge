import React, { forwardRef, useState } from "react";
import { makeRequest } from "../helpers";
import { Modal } from "@mui/material";
import TaskAssignModalContent from "./TaskAssignModalContent";
import TaskCommentsModalContent from "./TaskCommentsModalContent";
import TaskSubtasksModalContent from "./TaskSubtasksModalContent";

const TaskModalContent = forwardRef(({ details, uid, epics, tasks, setTasks, setOpen, forceUpdate }, ref) => {

  const [openAssign, setOpenAssign] = useState(false);
  const handleOpenAssign = () => { setOpenAssign(true) };
  const handleCloseAssign = () => { setOpenAssign(false) };
  const [openComments, setOpenComments] = useState(false);
  const handleOpenComments = () => { setOpenComments(true) };
  const handleCloseComments = () => { setOpenComments(false) };
  const [openSubtasks, setOpenSubtasks] = useState(false);
  const handleOpenSubtasks = () => { setOpenSubtasks(true) };
  const handleCloseSubtasks = () => { setOpenSubtasks(false) };

  const epicList = []
  for (const epic of epics) {
    epicList.push(<option value={epic.title}>{epic.title}</option>);
  }

  // const [isLoading, setIsLoading] = useState(<div className="task-modal"><CircularProgress /></div>);
  // const [data, setData] = useState();

  // useEffect(async () => {
  //   const data = await makeRequest(`/task/details?tid=${props.tid}`, 'GET', null, props.uid);
  //   if (data.error) alert(data.error);
  //   else {
  //     setData(data);
  //     setIsLoading(false);
  //   }
  // }, []);
  const handleSubmit = async (event) => {
    event.preventDefault();
    console.log(event);

    let eid = "None";
    for (const epic of epics) {
      if (epic.title === event.target.epic.value) {eid = epic.eid}
    }

    const body = {
      tid: details.tid,
      eid,
      assignees: details.assignees,
      title: event.target.title.value,
      description: event.target.description.value,
      deadline: event.target.deadline.value,
      workload: event.target.workload.value,
      priority: event.target.priority.value,
      status: event.target.status.value,
      flagged: event.target.flagged.value
    }
    const data = await makeRequest('/task/update', 'POST', body, uid);
    if (data.error) alert(data.error);
    else {
      setOpen(false)
      if (body.status !== details.status) {
        const newTasks = tasks;
        const idx = newTasks[details.status].findIndex((task) => {return task.tid === details.tid});
        newTasks[details.status].splice(idx, 1);
        newTasks[body.status].unshift(data);
        setTasks(newTasks);
        forceUpdate();
      } else {
        const newTasks = tasks;
        const idx = newTasks[details.status].findIndex((task) => {return task.tid === details.tid});
        newTasks[details.status].splice(idx, 1, data);
        setTasks(newTasks);
        forceUpdate();
      }
    }
  }

  return ( /*isLoading ||*/
    <form className="task-modal" onSubmit={handleSubmit}>
      <div id="task-left-section">
        <label htmlFor="title"><h3>Title</h3></label>
        <input type="text" id="title" name="title" defaultValue={details.title}/>
        <label htmlFor="description"><h3>Description</h3></label>
        <textarea placeholder="Add a description..." id="description" name="description" defaultValue={details.description} />
        <h3>Attachments</h3><br />
        <button type="button" onClick={handleOpenComments}>Comments</button>
        <Modal open={openComments} onClose={handleCloseComments}>
          <TaskCommentsModalContent uid={uid} tid={details.tid} comments={details.comments} handleClose={handleCloseComments} />
        </Modal>
        <button type="button" onClick={handleOpenSubtasks}>Subtasks</button>
        <Modal open={openSubtasks} onClose={handleCloseSubtasks}>
          <TaskSubtasksModalContent uid={uid} tid={details.tid} subtasks={details.subtasks} handleClose={handleCloseSubtasks} />
        </Modal>
      </div>
      <div id="task-right-section">
        <div>
          <label htmlFor="status"><h3>Status</h3></label>
          <label htmlFor="deadline"><h3>Deadline</h3></label>
          <h3>Assignee(s)</h3>
          <label htmlFor="priority"><h3>Priority</h3></label>
          <label htmlFor="workload"><h3>Workload</h3></label>
          <h3>Epic</h3>
          <h3>Flagged</h3>
          <button type="submit">Save Changes</button>
        </div>
        <div>
          <select id="status" name="status" style={{marginTop: '1.8em', marginBottom: '0.55em'}} defaultValue={details.status}>
            <option value="Not Started">Not Started</option>
            <option value="In Progress">In Progress</option>
            <option value="In Review/Testing">In Review/Testing</option>
            <option value="Blocked">Blocked</option>
            <option value="Completed">Completed</option>
          </select>
          <br />
          <input type="text" id="deadline" name="deadline" defaultValue={details.deadline} />
          <div style={{minHeight: '2em', maxHeight: '2em', marginTop: '1em', overflow: 'scroll', overflowX: 'hidden'}}>
            {details.assignee_emails.map((assignee, idx) => {return <h3 key={idx} style={{fontWeight: "normal", margin: '0'}}>{assignee}</h3>})}
          </div>
          <input type="text" id="priority" name="priority" defaultValue={details.priority} />
          <br />
          <input type="text" id="workload" name="workload" defaultValue={details.workload} />
          <br />
          <select id="epic" name="epic" style={{marginTop: '1.5em'}} defaultValue={details.epic}>
            <option value="None">None</option>
            {epicList.map((epic) => {return epic})}
          </select>
          <br />
          <select id="flagged" name="flagged" style={{marginTop: '2em'}} defaultValue={details.flagged}>
            <option value={true}>Yes</option>
            <option value={false}>No</option>
          </select>
          <br />
          <br />
          <button type="button" onClick={handleOpenAssign}>Reassign Task</button>
          <Modal open={openAssign} onClose={handleCloseAssign}>
            <TaskAssignModalContent uid={uid} tid={details.tid} emails={details.assignee_emails} handleClose={handleCloseAssign} />
          </Modal>
        </div>
      </div>
    </form>
  );
});

export default TaskModalContent;