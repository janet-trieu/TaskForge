import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from 'react-router-dom';
import { makeRequest } from '../helpers';
import { DragDropContext } from 'react-beautiful-dnd';
import Column from "../components/Column";
import './Project.css';
import testData from '../testData';
import ProjectModalContent from "../components/ProjectModalContent";
import ProjectInviteModalContent from "../components/ProjectInviteModalContent";
import TaskCreateModalContent from "../components/TaskCreateModalContent";
import EpicCreateModalContent from "../components/EpicCreateModalContent";
import { Modal } from "@mui/material";

const ProjectBoardView = ({ firebaseApp }) => {
  const [stateIsLoading, setStateIsLoading] = useState('Loading...');
  const [detailsIsLoading, setDetailsIsLoading] = useState('Loading...');
  const [details, setDetails] = useState();
  const [state, setState] = useState(testData);
  const [isCompleted, setIsCompleted] = useState();
  const {pid} = useParams();
  const uid = firebaseApp.auth().currentUser.uid;
  const navigate = useNavigate();
  const [openDetails, setOpenDetails] = useState(false);
  const handleOpenDetails = () => {setOpenDetails(true)};
  const handleCloseDetails = () => {setOpenDetails(false)};
  const [openInvite, setOpenInvite] = useState(false);
  const handleOpenInvite = () => {setOpenInvite(true)};
  const handleCloseInvite = () => {setOpenInvite(false)};
  const [openCreateTask, setOpenCreateTask] = useState(false);
  const handleOpenCreateTask = () => {setOpenCreateTask(true)};
  const handleCloseCreateTask = () => {setOpenCreateTask(false)};
  const [openCreateEpic, setOpenCreateEpic] = useState(false);
  const handleOpenCreateEpic = () => {setOpenCreateEpic(true)};
  const handleCloseCreateEpic = () => {setOpenCreateEpic(false)};

  useEffect(async () => {
    const data = await makeRequest(`/projects/view?pid=${pid}`, 'GET', null, uid);
    if (data.error) alert(data.error);
    else {
      setDetails(data);
      setDetailsIsLoading(false);
      if (data.status === 'Completed') {
        setIsCompleted(true);
      } else {
        setIsCompleted(false);
      }
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

  const handleDelete = async () => {
    const res = confirm("Are you sure you want to delete this project?");
    if (res) {
      const data = await makeRequest('/projects/delete', 'POST', {pid: pid}, uid);
      if (data.error) alert(data.error);
      else navigate('/projects');
    }
  }

  const handleLeave = async () => {
    const res = confirm("Are you sure you want to request to leave this project?");
    if (res) {
      const data = await makeRequest('/projects/leave', 'POST', {pid: Number(pid), msg: "The user is requesting to leave the project"}, uid);
      if (data.error) alert(data.error);
      else alert('Request to leave project has been sent!');
    }
  }

  const handleRevive = async() => {
    const data = await makeRequest("/projects/revive", "POST", {pid: Number(pid), new_status: "In Progress"}, uid);
    if (data.error) alert(data.error);
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
          <button className={isCompleted ? "" : "hide"} onClick={handleRevive}>Revive Project</button>
          <button className={!isCompleted ? "" : "hide"} onClick={handleOpenDetails}>Details</button>&nbsp;&nbsp;
          <button className={!isCompleted ? "" : "hide"} style={{backgroundColor: 'cornflowerblue'}} onClick={handleOpenInvite}>Invite Members</button>&nbsp;&nbsp;
          <button className={!isCompleted ? "" : "hide"} style={{backgroundColor: 'seagreen'}} onClick={handleOpenCreateTask}>Create Task</button>&nbsp;&nbsp;
          <button className={!isCompleted ? "" : "hide"} style={{backgroundColor: 'seagreen'}} onClick={handleOpenCreateEpic}>Create Epic</button>&nbsp;&nbsp;
          <button className={!isCompleted ? "" : "hide"} style={{backgroundColor: 'firebrick'}} onClick={handleDelete}>Delete Project</button>&nbsp;&nbsp;
          <button className={!isCompleted ? "" : "hide"} style={{backgroundColor: 'gray'}} onClick={handleLeave}>Request to Leave</button>
        </div>
        <Modal open={openDetails} onClose={handleCloseDetails}>
          <ProjectModalContent details={details} uid={uid} handleClose={handleCloseDetails} setDetails={setDetails} />
        </Modal>
        <Modal open={openInvite} onClose={handleCloseInvite}>
          <ProjectInviteModalContent uid={uid} pid={pid} handleClose={handleCloseInvite} />
        </Modal>
        <Modal open={openCreateTask} onClose={handleCloseCreateTask}>
          <TaskCreateModalContent uid={uid} pid={pid} epics={details.epics} handleClose={handleCloseCreateTask} />
        </Modal>
        <Modal open={openCreateEpic} onClose={handleCloseCreateEpic}>
          <EpicCreateModalContent uid={uid} pid={pid} handleClose={handleCloseCreateEpic} />
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
