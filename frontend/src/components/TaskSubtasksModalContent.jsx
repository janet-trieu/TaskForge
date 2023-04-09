import React, { forwardRef, useState } from "react";
import { makeRequest } from "../helpers";
import styled from "styled-components";
import { Modal } from "@mui/material";
import TaskSubtasksCreateModalContent from "./TaskSubtasksCreateModalContent";

const TaskSubtasksModalContent = forwardRef((props, ref) => {

  const handleSubmit = async (event) => {
    event.preventDefault();
    event.stopPropagation();

    // const data = await makeRequest('/task/comment', 'POST', {tid: props.tid, comment}, props.uid);
    if (data.error) alert(data.error);
    else {

    };
  }

  return (
    <div id="task-subtasks-modal">
      {/* Create subtask option */}
      <button>Create Subtask</button>
      <Modal open={openSubtasks} onClose={handleCloseSubtasks}>
        <TaskSubtasksCreateModalContent uid={uid} tid={details.tid} subtasks={details.subtasks} handleClose={handleCloseSubtasks} />
      </Modal>
      {/* View subtasks */}
    </div>
  );
});

export default TaskSubtasksModalContent;