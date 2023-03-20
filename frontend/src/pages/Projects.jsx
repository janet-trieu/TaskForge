import React from "react";
import ProjectCard from "../components/ProjectCard";
import Searchbar from "../components/Searchbar";

const Projects = () => {
  
  return (
    <>
      <Searchbar />
      <div id='projects-container'>
        <ProjectCard />
        <ProjectCard />
        <ProjectCard />
        <ProjectCard />
        <ProjectCard />
        <ProjectCard />
        <ProjectCard />
        <ProjectCard />
        <ProjectCard />
      </div>
    </>
  )
}

export default Projects;
