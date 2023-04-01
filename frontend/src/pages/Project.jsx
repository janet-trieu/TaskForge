import React, { useState, useEffect } from "react";
import { useParams } from 'react-router-dom';
import { makeRequest } from '../helpers';
import { DragDropContext } from 'react-beautiful-dnd';
import Column from "./Column";
import './Project.css';
import testData from '../testData';

const Project = ({ firebaseApp }) => {
  const [stateIsLoading, setstateIsLoading] = useState('Loading...');
  const [detailsIsLoading, setDetailsIsLoading] = useState('Loading...');
  const [details, setDetails] = useState();
  const [state, setState] = useState(testData);
  const {pid} = useParams();

  useEffect(async () => {
    const data = await makeRequest(`/projects/view?pid=${pid}`, 'GET', null, firebaseApp.auth().currentUser.uid);
    if (data.error) alert(data.error);
    else {
      console.log(data)
      setDetails(data);
      setDetailsIsLoading(false);
    }
  }, [])

  const handleDragEnd = (result) => {
    const { destination, source, draggableId } = result;

    if (!destination) {return;}
    if (destination.droppableId === source.droppableId && destination.index === source.index) {return;}

    const start = state.columns[source.droppableId];
    const finish = state.columns[destination.droppableId];

    if (start === finish) {
      const newTaskIds = Array.from(start.taskIds);
      newTaskIds.splice(source.index, 1);
      newTaskIds.splice(destination.index, 0, draggableId);

      const newColumn = {
        ...start,
        taskIds: newTaskIds,
      };

      const newState = {
        ...state,
        columns: {
          ...state.columns,
          [newColumn.id]: newColumn,
        },
      };

      setState(newState);
      return;
    }

    // Moving from one list to another
    const startTaskIds = Array.from(start.taskIds);
    startTaskIds.splice(source.index, 1);
    const newStart = {
      ...start,
      taskIds: startTaskIds,
    };

    const finishTaskIds = Array.from(finish.taskIds);
    finishTaskIds.splice(destination.index, 0, draggableId);
    const newFinish = {
      ...finish,
      taskIds: finishTaskIds,
    };

    const newState = {
      ...state,
      columns: {
        ...state.columns,
        [newStart.id]: newStart,
        [newFinish.id]: newFinish,
      },
    };
    setState(newState);
  };

  return (
    <>
      {detailsIsLoading || (
        <div id='project-container'>
        <div id='project-header'>
          <div id='project-name-block'>
            <div style={{fontWeight: 'bold', fontSize: '1.5em'}}>{details.name}</div>
            <div>{details.description}</div>
          </div>
          <div id='project-member-block'></div>
        </div>
        <div id='project-buttons'>
          Hello.
        </div>
        <DragDropContext onDragEnd={handleDragEnd}>
          <div id="task-list-container">
          {state.columnOrder.map(columnId => {
            const column = state.columns[columnId];
            const tasks = column.taskIds.map(taskId => state.tasks[taskId]);

            return <Column key={column.id} column={column} tasks={tasks} />;
          })}
          </div>
        </DragDropContext>
      </div>
      )}
    </>
  )
}

export default Project;
