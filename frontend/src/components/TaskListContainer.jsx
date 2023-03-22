import React from "react";
import { Droppable } from 'react-beautiful-dnd';
import TaskCard from "./TaskCard";
import TaskList from "./TaskList";

const TaskListContainer = ({ did, didx }) => {
  const tasks = [0, 1, 2]
  return (
    <div className="task-list">
      <div>Task List Name</div>
      <Droppable droppableId={did} index={didx}>
        {(provided) => (
          <TaskList innerRef={provided.innerRef} {...provided.droppableProps}>
            {tasks.map(idx => <TaskCard did={`${idx}`} didx={idx} key={idx} />)}
            {provided.placeholder}
          </TaskList>
        )}
      </Droppable>
    </div>
  )
}

export default TaskListContainer;
