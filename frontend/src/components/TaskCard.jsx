import React, { useState } from "react";
import styled from 'styled-components';
import Modal from '@mui/material/Modal';
import TaskModalContent from "./TaskModalContent";

const Container = styled.div`
  border: 1px solid lightgrey;
  border-radius: 2px;
  padding: 8px;
  margin-bottom: 8px;
  background-color: white;
`;

const TaskCard = (props) => {
  const [open, setOpen] = useState(false);
  const handleOpen = () => {setOpen(true)};
  const handleClose = () => {setOpen(false)};
  return (
    <>
      <Container onClick={handleOpen}>
        {props.task.title}
      </Container>
      <Modal open={open} onClose={handleClose}>
        <TaskModalContent details={props.task} uid={props.uid} epics={props.epics} setTasks={props.setTasks}/>
      </Modal>
    </>
  );
}

export default TaskCard;