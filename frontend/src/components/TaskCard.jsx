import React, { useState, useEffect } from "react";
import styled from 'styled-components';
import Modal from '@mui/material/Modal';
import TaskModalContent from "./TaskModalContent";
import './TaskCard.css'

const Container = styled.div`
  border: 1px solid lightgrey;
  border-radius: 2px;
  padding: 8px;
  margin-bottom: 8px;
  background-color: white;
`;

const TaskCard = (props) => {
  const [open, setOpen] = useState(false);
  const handleOpen = () => { setOpen(true) };
  const handleClose = () => { setOpen(false) };

  let epic = null;
  for (const curr of props.epics) {
    if (curr.eid === props.task.eid) epic = curr;
  }

  return (
    <>
      <Container onClick={handleOpen}>
        {epic !== null ? <div className="task-epic" style={{backgroundColor: epic.colour}}>{epic.title}</div> : <></>}
        <div className="task-title">{props.task.title}</div>
        {props.task.deadline !== "" ? <div className="task-deadline">{props.task.deadline}</div> : <></>}
        {props.task.priority !== "" ? <div className={`task-priority ${props.task.priority}`}>{props.task.priority}</div> : <></>}
      </Container>
      <Modal open={open} onClose={handleClose}>
        <TaskModalContent details={props.task} uid={props.uid} epics={props.epics} tasks={props.tasks} setTasks={props.setTasks} setOpen={setOpen} forceUpdate={props.forceUpdate} pid={props.pid}/>
      </Modal>
    </>
  );
}

export default TaskCard;