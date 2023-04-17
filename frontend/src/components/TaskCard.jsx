import React, { useState, useEffect } from "react";
import { makeRequest } from "../helpers";
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
  const [isLoading, setIsLoading] = useState("Loading...");
  const [epicDetails, setEpicDetails] = useState();
  const handleOpen = () => { setOpen(true) };
  const handleClose = () => { setOpen(false) };

  const getEpicData = async () => {
    if (props.task.eid !== null) {
      const data = await makeRequest(`/epic/details?eid=${props.task.eid}`, 'GET', null, props.uid);
      if (data.error) alert(data.error);
      else {
        setEpicDetails(data);
        setIsLoading(false);
      }
    } else {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    getEpicData();
  }, []);

  return (
    <>
      {isLoading || (
        <Container onClick={handleOpen}>
          <div className="task-epic">{epicDetails.title}</div>
          <div className="task-title">{props.task.title}</div>
          <div className="task-deadline">{props.task.deadline}</div>
          <div className="task-priority">{props.task.priority}</div>
        </Container>
      )}
      <Modal open={open} onClose={handleClose}>
        <TaskModalContent details={props.task} uid={props.uid} epics={props.epics} tasks={props.tasks} setTasks={props.setTasks} setOpen={setOpen} forceUpdate={props.forceUpdate} />
      </Modal>
    </>
  );
}

export default TaskCard;