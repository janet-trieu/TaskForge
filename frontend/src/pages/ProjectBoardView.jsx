import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from 'react-router-dom';
import { makeRequest } from '../helpers';
import Column from "../components/Column";
import './Project.css';
import ProjectModalContent from "../components/ProjectModalContent";
import ProjectInviteModalContent from "../components/ProjectInviteModalContent";
import TaskCreateModalContent from "../components/TaskCreateModalContent";
import EpicCreateModalContent from "../components/EpicCreateModalContent";
import ProjectRemoveModalContent from "../components/ProjectRemoveModalContent";
import { Modal } from "@mui/material";

const ProjectBoardView = ({ firebaseApp }) => {
  const [detailsIsLoading, setDetailsIsLoading] = useState('Loading...');
  const [details, setDetails] = useState();
  const [tasksIsLoading, setTasksIsLoading] = useState('Loading...');
  const [tasks, setTasks] = useState();
  const [isCompleted, setIsCompleted] = useState();
  const [isPM, setIsPM] = useState(false);
  const { pid } = useParams();
  const uid = firebaseApp.auth().currentUser.uid;
  const navigate = useNavigate();
  const [openDetails, setOpenDetails] = useState(false);
  const handleOpenDetails = () => { setOpenDetails(true) };
  const handleCloseDetails = () => { setOpenDetails(false) };
  const [openInvite, setOpenInvite] = useState(false);
  const handleOpenInvite = () => { setOpenInvite(true) };
  const handleCloseInvite = () => { setOpenInvite(false) };
  const [openCreateTask, setOpenCreateTask] = useState(false);
  const handleOpenCreateTask = () => { setOpenCreateTask(true) };
  const handleCloseCreateTask = () => { setOpenCreateTask(false) };
  const [openCreateEpic, setOpenCreateEpic] = useState(false);
  const handleOpenCreateEpic = () => { setOpenCreateEpic(true) };
  const handleCloseCreateEpic = () => { setOpenCreateEpic(false) };
  const [openRemove, setOpenRemove] = useState(false);
  const handleOpenRemove = () => { setOpenRemove(true) };
  const handleCloseRemove = () => { setOpenRemove(false) };

  useEffect(async () => {
    const data = await makeRequest(`/projects/view?pid=${pid}`, 'GET', null, uid);
    if (data.error) alert(data.error);
    else {
      setDetails(data);
      setDetailsIsLoading(false);
      setIsCompleted(data.status === 'Completed');
      setIsPM(data.uid === uid);
    }
    
    const data1 = await makeRequest(`/taskboard/show?pid=${pid}&hidden=true`, 'GET', null, uid);
    if (data1.error) alert(data1.error);
    else {
      setTasks(data1);
      setTasksIsLoading(false);
    }
  }, [])

  const handleDelete = async () => {
    const res = confirm("Are you sure you want to delete this project?");
    if (res) {
      const data = await makeRequest('/projects/delete', 'POST', { pid: pid }, uid);
      if (data.error) alert(data.error);
      else navigate('/projects');
    }
  }

  const handleLeave = async () => {
    const res = confirm("Are you sure you want to request to leave this project?");
    if (res) {
      const data = await makeRequest('/projects/leave', 'POST', { pid: Number(pid), msg: "The user is requesting to leave the project" }, uid);
      if (data.error) alert(data.error);
      else alert('Request to leave project has been sent!');
    }
  }

  const handleRevive = async () => {
    const res = confirm("Are you sure you want to request to leave this project?");
    if (res) {
      const data = await makeRequest("/projects/revive", "POST", { pid: Number(pid), new_status: "In Progress" }, uid);
      if (data.error) alert(data.error);
      else alert('Project has been revived!');
    }
  }

  return (
    <>
      {detailsIsLoading || (
        <div id='project-container'>
          <div id='project-header'>
            <div id='project-name-block'>
              <div style={{ fontWeight: 'bold', fontSize: '1.5em' }}>{details.name}</div>
              <div>{details.description}</div>
            </div>
            <div id='project-member-block'></div>
          </div>
          <div id='project-buttons'>
            <button className={isCompleted && isPM ? "" : "hide"} onClick={handleRevive}>Revive Project</button>&nbsp;&nbsp;
            <button className={!isCompleted ? "" : "hide"} onClick={handleOpenDetails}>Details</button>&nbsp;&nbsp;
            <button className={!isCompleted ? "" : "hide"} style={{ backgroundColor: 'cornflowerblue' }} onClick={handleOpenInvite}>Invite Members</button>&nbsp;&nbsp;
            <button className={!isCompleted ? "" : "hide"} style={{ backgroundColor: 'seagreen' }} onClick={handleOpenCreateTask}>Create Task</button>&nbsp;&nbsp;
            <button className={!isCompleted ? "" : "hide"} style={{ backgroundColor: 'seagreen' }} onClick={handleOpenCreateEpic}>Create Epic</button>&nbsp;&nbsp;
            <button className={!isCompleted && isPM ? "" : "hide"} style={{ backgroundColor: 'firebrick' }} onClick={handleDelete}>Delete Project</button>&nbsp;&nbsp;
            <button className={!isCompleted && isPM ? "" : "hide"} style={{ backgroundColor: 'firebrick' }} onClick={handleOpenRemove}>Remove Member</button>
            <button className={!isCompleted && !isPM ? "" : "hide"} style={{ backgroundColor: 'gray' }} onClick={handleLeave}>Request to Leave</button>&nbsp;&nbsp;
          </div>
          <Modal open={openDetails} onClose={handleCloseDetails}>
            <ProjectModalContent details={details} uid={uid} handleClose={handleCloseDetails} setDetails={setDetails} />
          </Modal>
          <Modal open={openInvite} onClose={handleCloseInvite}>
            <ProjectInviteModalContent uid={uid} pid={pid} handleClose={handleCloseInvite} />
          </Modal>
          <Modal open={openCreateTask} onClose={handleCloseCreateTask}>
            <TaskCreateModalContent uid={uid} pid={pid} epics={details.epics} handleClose={handleCloseCreateTask} tasks={tasks} setTasks={setTasks} />
          </Modal>
          <Modal open={openCreateEpic} onClose={handleCloseCreateEpic}>
            <EpicCreateModalContent uid={uid} pid={pid} handleClose={handleCloseCreateEpic} />
          </Modal>
          <Modal open={openRemove} onClose={handleCloseRemove}>
            <ProjectRemoveModalContent uid={uid} pid={pid} handleClose={handleCloseRemove} />
          </Modal>
          {tasksIsLoading || (
            <div id="task-list-container">
              <Column title={"NOT STARTED"} tasks={tasks["Not Started"]} uid={uid} epics={details.epics} setTasks={setTasks} />
              <Column title={"IN PROGRESS"} tasks={tasks["In Progress"]} uid={uid} epics={details.epics} setTasks={setTasks} />
              <Column title={"IN REVIEW/TESTING"} tasks={tasks["In Review/Testing"]} uid={uid} epics={details.epics} setTasks={setTasks} />
              <Column title={"BLOCKED"} tasks={tasks["Blocked"]} uid={uid} epics={details.epics} setTasks={setTasks} />
              <Column title={"COMPLETED"} tasks={tasks["Completed"]} uid={uid} epics={details.epics} setTasks={setTasks} />
            </div>
          )}
        </div>
      )}
    </>
  )
}

export default ProjectBoardView;
