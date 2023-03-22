import React from "react";
import { Draggable } from 'react-beautiful-dnd';
import TaskCardContainer from './TaskCardContainer';

const TaskCard = ({ did, didx }) => {
  return (
    <Draggable draggableId={did} index={didx}>
      {(provided) => (
        <TaskCardContainer {...provided.draggableProps} {...provided.dragHandleProps} innerRef={provided.innerRef}></TaskCardContainer>
      )}
    </Draggable>
  )
}

export default TaskCard;
