import React, { useState, useEffect } from "react";
import TasksCard from "../components/TasksCard";
import TasksSearchbar from "../components/TasksSearchbar";
import { makeRequest } from '../helpers';
import { useLocation } from "react-router-dom";

const Tasks = ({ firebaseApp }) => {
  const [tasks, setTasks] = useState();
  const [isLoading, setIsLoading] = useState('Loading...');
  const [showCompleted, setShowCompleted] = useState(false);
  const location = useLocation();
  const uid = location.pathname.split("/").length === 3 ? location.pathname.split("/")[2] : firebaseApp.auth().currentUser.uid;

  useEffect(async () => {
    const data = await makeRequest('/tasklist/show', 'GET', null, uid);
    if (data.error) alert(data.error);
    else {
      setTasks(data);
      setIsLoading(false);
    }
  }, [])

  return (
    <>
      <TasksSearchbar setTasks={setTasks} setIsLoading={setIsLoading} uid={uid} showCompleted={showCompleted} setShowCompleted={setShowCompleted} />
      <div id='tasks-container'>
        {isLoading || (
          tasks.map((details, idx) => {
            if (showCompleted || details.status !== "Completed") {
              return <TasksCard title={details.title} description={details.description} status={details.status} pid={details.pid} key={idx} />
            }
          })
        )}
      </div>
    </>
  )
}

export default Tasks;
