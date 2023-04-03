import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from 'react-router-dom';
import { makeRequest } from '../helpers';
import { DragDropContext } from 'react-beautiful-dnd';
import Column from "../components/Column";
import './Project.css';
import testData from '../testData';
import ProjectModalContent from "../components/ProjectModalContent";
import { Modal } from "@mui/material";

const ProjectBoardView = ({ firebaseApp }) => {
  const [stateIsLoading, setstateIsLoading] = useState('Loading...');
  const [detailsIsLoading, setDetailsIsLoading] = useState('Loading...');
  const [details, setDetails] = useState();
  const [state, setState] = useState(testData);
  const {pid} = useParams();
  const uid = firebaseApp.auth().currentUser.uid;
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);
  const handleOpen = () => {setOpen(true)};
  const handleClose = () => {setOpen(false)};

  useEffect(async () => {
    const data = await makeRequest(`/projects/view?pid=${pid}`, 'GET', null, uid);
    if (data.error) alert(data.error);
    else {
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

  const handleDelete = () => {
    const res = confirm("Are you sure you want to delete this project?");
    if (res) {
      const data = makeRequest('/projects/delete', 'POST', {pid: pid}, uid);
      if (data.error) alert(data.error);
      else navigate('/projects');
    }
  }

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
          <button onClick={handleOpen}>Details</button>&nbsp;&nbsp;
          <button style={{backgroundColor: 'seagreen'}}>Create Task</button>&nbsp;&nbsp;
          <button style={{backgroundColor: 'firebrick'}} onClick={handleDelete}>Delete Project</button>
        </div>
        <Modal open={open} onClose={handleClose}>
          <ProjectModalContent details={details} uid={uid} handleClose={handleClose} setDetails={setDetails} />
        </Modal>
        <DragDropContext onDragEnd={handleDragEnd}>
          <div id="task-list-container">
          {state.columnOrder.map(columnId => {
            const column = state.columns[columnId];
            const tasks = column.taskIds.map(taskId => state.tasks[taskId]);

            return <Column key={column.id} column={column} tasks={tasks} uid={uid} />;
          })}
          </div>
        </DragDropContext>
      </div>
      )}
    </>
  )
}

export default ProjectBoardView;
