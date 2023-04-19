import React, { forwardRef, useState, useEffect } from "react";
import { makeRequest } from "../helpers";
import { Modal } from "@mui/material";
import SubtaskCard from "./SubtaskCard";
import TaskSubtasksCreateModalContent from "./TaskSubtasksCreateModalContent";

const TaskSubtasksModalContent = forwardRef((props, ref) => {
  const [isLoading, setIsLoading] = useState("Loading...");
  const [subtasks, setSubtasks] = useState();
  const [openCreate, setOpenCreate] = useState(false);
  const handleOpenCreate = () => { setOpenCreate(true) };
  const handleCloseCreate = () => { setOpenCreate(false) };

  // const testSubtask = {
  //   stid: "EXA-001",
  //   title: "This is the task title.",
  //   description: "This is the description of the subtask.",
  //   status: "In Progress",
  //   deadline: "01/01/2001",
  //   workload: 3,
  //   priority: "Low",
  //   assignees: ["test@email.com", "test1@email.com", "test2@email.com"]
  // }

  useEffect(async () => {
    const data = await makeRequest("/subtasks/get_all", "GET", {tid: props.tid}, props.uid);
    if (data.code && data.code !== 200) alert(data.message);
    else {
      console.log(data)
      setSubtasks(data);
      setIsLoading(false);
    }
  }, []);

  return (
    <div id="task-subtasks-modal">
      {/* Create subtask option */}
      <button type="button" style={{width: '100%', marginBottom: '2em'}} onClick={handleOpenCreate}>Create Subtask</button>
      <Modal open={openCreate} onClose={handleCloseCreate}>
        <TaskSubtasksCreateModalContent uid={props.uid} tid={props.tid} handleClose={handleCloseCreate} subtasks={subtasks} setSubtasks={setSubtasks} pid={props.pid} />
      </Modal>
      {/* View subtasks */}
      <div id="subtask-card-container">
        {isLoading || subtasks.map((subtask, idx) => {
          return <SubtaskCard key={idx} uid={props.uid} subtask={subtask}/>
        })}
        {/* <SubtaskCard uid={props.uid} subtask={testSubtask}/> */}
      </div>
    </div>
  );
});

export default TaskSubtasksModalContent;