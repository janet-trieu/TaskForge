import React, { forwardRef, useState } from "react";
import { makeRequest } from "../helpers";
import styled from "styled-components";

const TaskSubtasksCreateModalContent = forwardRef((props, ref) => {

  const handleSubmit = async (event) => {
    event.preventDefault();
    event.stopPropagation();

    // const data = await makeRequest('/task/comment', 'POST', {tid: props.tid, comment}, props.uid);
    if (data.error) alert(data.error);
    else {

    };
  }

  return (
    <div id="task-subtasks-create-modal">
      Hello.
    </div>
  );
});

export default TaskSubtasksCreateModalContent;