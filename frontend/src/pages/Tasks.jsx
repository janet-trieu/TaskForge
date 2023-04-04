import React, { useState, useEffect } from "react";
import TasksCard from "../components/TasksCard";
import TasksSearchbar from "../components/TasksSearchbar";
import { makeRequest } from '../helpers';

const Tasks = ({ firebaseApp }) => {
  const [tasks, setTasks] = useState();
  const [isLoading, setIsLoading] = useState('Loading...');
  const [showCompleted, setShowCompleted] = useState(false);

  useEffect(async () => {
    const data = await makeRequest('/tasklist/show', 'GET', null, firebaseApp.auth().currentUser.uid);
    if (data.error) alert(data.error);
    else {
      setTasks(data);
      setIsLoading(false);
    }
  }, [showCompleted])

  return (
    <>
      <TasksSearchbar setTasks={setTasks} setIsLoading={setIsLoading} uid={firebaseApp.auth().currentUser.uid} showCompleted={showCompleted} setShowCompleted={setShowCompleted} />
      <div id='tasks-container'>
        {isLoading || (
          tasks.map((details, idx) => {
            if (showCompleted || details.status !== "Completed") {
              return <TasksCard name={details.name} description={details.description} status={details.status} picture={details.picture} pid={details.pid} key={idx} />
            }
          })
        )}
      </div>
    </>
  )
}

export default Tasks;
