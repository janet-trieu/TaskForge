import React, { useState } from "react";
import styled from 'styled-components';
import { Draggable } from 'react-beautiful-dnd';
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
    <Draggable draggableId={props.task.id} index={props.index}>
      {provided => (<>
        <Container
          {...provided.draggableProps}
          {...provided.dragHandleProps}
          ref={provided.innerRef}
          onClick={handleOpen}
        >
          {props.task.content}
        </Container>
        <Modal open={open} onClose={handleClose}>
          <TaskModalContent content={props.task.content} />
        </Modal>
      </>)}
    </Draggable>
  );
}

export default TaskCard;