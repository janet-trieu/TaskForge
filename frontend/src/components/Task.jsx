import React from 'react';
import styled from 'styled-components';
import { Draggable } from 'react-beautiful-dnd';

const Container = styled.div`
  border: 1px solid lightgrey;
  border-radius: 2px;
  padding: 8px;
  margin-bottom: 8px;
  background-color: white;
`;

const Task = ({ idx }) => {
  return (
    <Draggable draggableId={`${idx}`} index={idx}>
      {provided => (
        <Container
          {...provided.draggableProps}
          {...provided.dragHandleProps}
          innerRef={provided.innerRef}
        >
          Hello.
        </Container>
      )}
    </Draggable>
  );
}

export default Task;
