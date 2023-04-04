import React from "react";
import './TasksCard.css';
import { useNavigate } from "react-router-dom";

const TasksCard = (props) => {
  const navigate = useNavigate();
  let statusClass = null;
  if (props.status === "Not Started") statusClass = 'not-started';
  else if (props.status === "Completed") statusClass = 'completed';
  else statusClass = 'ongoing';
  return (
    <div className="tasks-card" onClick={() => navigate(`/projects/${props.pid}`)}>
      <div style={{fontWeight: 'bold', fontSize: '1.2em'}}>{props.title}</div>
      <div>{props.description}</div>
      <div className={statusClass}>{props.status}</div>
    </div>
  )
}

export default TasksCard;