import React, { forwardRef, useState, useEffect } from "react";
import { makeRequest } from "../helpers";

const TaskAssignModalContent = forwardRef((props, ref) => {

  const handleSubmit = async (event) => {
    event.preventDefault();
    event.stopPropagation();
  }

  return (
    <></>
  );
});

export default TaskAssignModalContent;