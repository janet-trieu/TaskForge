import React from 'react';
import styled from 'styled-components';
import { Droppable } from 'react-beautiful-dnd';
import Task from "./Task"

const Container = styled.div`
  margin: 8px;
  border: 1px solid lightgrey;
  border-radius: 2px;
`;
const Title = styled.h3`
  padding: 8px;
`;
const TaskList = styled.div`
  padding: 8px;
`;

const Column = ({ idx }) => {
  return (
    <Container>
      <Title>Task List Name</Title>
      <Droppable droppableId={`${idx}`}>
        {provided => (
          <TaskList innerRef={provided.innerRef} {...provided.droppableProps}>
            <Task idx={0} />
            <Task idx={1} />
            <Task idx={2} />
            {provided.placeholder}
          </TaskList>
        )}
      </Droppable>
    </Container>
  );
}

export default Column;
