import React from "react";
import './ProjectCard.css';
import { useNavigate } from "react-router-dom";

const ProjectCard = ({ name, description, status, picture, pid }) => {
  const navigate = useNavigate();
  let statusClass = null;
  if (status === "Not Started") statusClass = 'not-started';
  else if (status === "Completed") statusClass = 'completed';
  else statusClass = 'ongoing';
  return (
    <div className="project-card" onClick={() => navigate(`/projects/${pid}`)}>
      <img src={picture} style={{borderRadius: '100px'}} />
      <br />
      <div style={{fontWeight: 'bold', fontSize: '1.2em'}}>{name}</div>
      <div>{description}</div>
      <div className={statusClass}>{status}</div>
    </div>
  )
}

export default ProjectCard;