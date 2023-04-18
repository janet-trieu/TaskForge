import React, { forwardRef, useState } from "react";
import { makeRequest } from "../helpers";
import { Modal } from "@mui/material";
import TaskSubtasksCreateModalContent from "./TaskSubtasksCreateModalContent";

const TaskSubtasksModalContent = forwardRef((props, ref) => {

  const [isLoading, setIsLoading] = useState("Loading...");
  const [openCreate, setOpenCreate] = useState(false);
  const handleOpenCreate = () => { setOpenCreate(true) };
  const handleCloseCreate = () => { setOpenCreate(false) };

  return (
    <div id="task-subtasks-modal">
      {/* Create subtask option */}
      <button type="button" onClick={handleOpenCreate}>Create Subtask</button>
      <Modal open={openCreate} onClose={handleCloseCreate}>
        <TaskSubtasksCreateModalContent uid={props.uid} tid={props.tid} handleClose={handleCloseCreate} />
      </Modal>
      {/* View subtasks */}
    </div>
  );
});

export default TaskSubtasksModalContent;