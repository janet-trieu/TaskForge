import React, { useState, useEffect } from "react";
import ProjectCard from "../components/ProjectCard";
import ProjectSearchbar from "../components/ProjectSearchbar";
import { makeRequest } from '../helpers';

const Projects = ({ firebaseApp }) => {
  const [projects, setProjects] = useState();
  const [isLoading, setIsLoading] = useState('Loading...');
  const [showCompleted, setShowCompleted] = useState(false);

  useEffect(async () => {
    const data = await makeRequest('/projects/search', 'GET', {query: ''}, firebaseApp.auth().currentUser.uid);
    if (data.error) alert(data.error);
    else {
      setProjects(data);
      setIsLoading(false);
      console.log(data)
    }
  }, [showCompleted])

  return (
    <>
      <ProjectSearchbar setProjects={setProjects} setIsLoading={setIsLoading} uid={firebaseApp.auth().currentUser.uid} showCompleted={showCompleted} setShowCompleted={setShowCompleted} />
      <div id='projects-container'>
        {isLoading || (
          projects.map((details, idx) => {
            if (showCompleted || details.status !== "Completed") {
              console.log(details.is_pinned)
              return <ProjectCard name={details.name} description={details.description} status={details.status} picture={details.picture} pid={details.pid} key={idx} isPinned={details.is_pinned} uid={firebaseApp.auth().currentUser.uid}/>
            }
          })
        )}
      </div>
    </>
  )
}

export default Projects;
