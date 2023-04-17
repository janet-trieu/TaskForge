import React from "react";
import styled from 'styled-components';
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
      <Title>{props.title} - {props.tasks.length} TASKS</Title>
      <TaskList>
        {props.tasks.map((task, idx) => (
          <TaskCard key={idx} task={task} uid={props.uid} epics={props.epics} tasks={props.taskState} setTasks={props.setTasks} forceUpdate={props.forceUpdate}/>
        ))}
      </TaskList>
    </Container>
  );
}

export default Column;