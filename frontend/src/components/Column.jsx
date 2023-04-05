import React from "react";
import styled from 'styled-components';
import { Droppable } from "react-beautiful-dnd";
import TaskCard from "./TaskCard";

const Container = styled.div`
  margin: 8px;
  border: 1px solid lightgrey;
  border-radius: 10px;
  background-color: #f3f3f3;
`;
const Title = styled.h3`
  padding: 8px;
`;
const TaskList = styled.div`
  padding: 8px;
  max-height: 50vh;
  overflow: auto;
  width: 250px;
`;

const Column = (props) => {

  return (
    <Container>
      <Title>{props.column.title} - {props.tasks.length} TASKS</Title>
      <Droppable droppableId={props.column.id}>
        {provided => (
          <TaskList ref={provided.innerRef} {...provided.droppableProps}>
            {props.tasks.map((task, index) => (
                <TaskCard key={task.id} task={task} index={index} uid={props.uid}/>
              ))}
            {provided.placeholder}
          </TaskList>
        )}
      </Droppable>
    </Container>
  );
}

export default Column;