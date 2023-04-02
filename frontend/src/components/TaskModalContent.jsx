import React, { forwardRef, useState, useEffect } from "react";
import { makeRequest } from "../helpers";
import CircularProgress from '@mui/material/CircularProgress';

const TaskModalContent = forwardRef((props, ref) => {

  const [isLoading, setIsLoading] = useState(<div className="task-modal"><CircularProgress /></div>);
  const [data, setData] = useState();

  useEffect(async () => {
    const data = await makeRequest(`/task/details?tid=${props.tid}`, 'GET', null, props.uid);
    if (data.error) alert(data.error);
    else {
      setData(data);
      setIsLoading(false);
    }
  }, []);

  return ( isLoading ||
    <div className="task-modal">
      <div id="task-left-section">
        <h2>Task Name</h2>
        <h3>Description</h3>
        <textarea placeholder="Add a description..."></textarea>
        <h3>Attachments</h3>
        <h3>Comments</h3>
      </div>
      <div id="task-right-section">
        <div>
          <h3>Due Date</h3>
          <h3>Assignee(s)</h3>
          <h3>Priority</h3>
          <h3>Workload</h3>
          <h3>Epic</h3>
          <h3>Created</h3>
          <h3>Updated</h3>
        </div>
        <div>
          <h3 style={{fontWeight: "normal"}}>Due Date</h3>
          <h3 style={{fontWeight: "normal"}}>Assignees</h3>
          <h3 style={{fontWeight: "normal"}}>Priority</h3>
          <h3 style={{fontWeight: "normal"}}>Workload</h3>
          <h3 style={{fontWeight: "normal"}}>Epic</h3>
          <h3 style={{fontWeight: "normal"}}>Created</h3>
          <h3 style={{fontWeight: "normal"}}>Updated</h3>
        </div>
      </div>
    </div>
  );
});

export default TaskModalContent;