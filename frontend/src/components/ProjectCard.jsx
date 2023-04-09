import React, { useState } from "react";
import { makeRequest } from '../helpers';
import './ProjectCard.css';
import { useNavigate } from "react-router-dom";
import unpin from '../assets/project unpin.png'
import pin from '../assets/project pin.png'

const ProjectCard = ({ name, description, status, picture, pid, isPinned, uid }) => {
  const navigate = useNavigate();
  const [pinned, setPinned] = useState(isPinned);

  let statusClass = null;
  if (status === "Not Started") statusClass = 'not-started';
  else if (status === "Completed") statusClass = 'completed';
  else statusClass = 'ongoing';

  const togglePin = async (event) => {
    event.stopPropagation();
    const data = await makeRequest('/projects/pin', 'POST', { pid: pid, is_pinned: !pinned }, uid);
    if (data.error) alert(alert.error);
    else setPinned(!pinned)
  }

  return (
    <div className="project-card" onClick={() => navigate(`/projects/${pid}`)}>
      <img src={picture} style={{ borderRadius: '100px' }} />
      <br />
      <div style={{ fontWeight: 'bold', fontSize: '1.2em' }}>{name}</div>
      <div>{description}</div>
      <div className={statusClass}>{status}</div>
      {!pinned ? (
        <button onClick={togglePin} style={{ backgroundColor: "transparent" }}>
          <img src={unpin} />
        </button>
      ) : (
        <button onClick={togglePin} style={{ backgroundColor: "transparent" }} >
          <img src={pin} />
        </button>
      )}
    </div>
  )
}

export default ProjectCard;