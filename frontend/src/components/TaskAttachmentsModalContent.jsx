import React, { forwardRef, useState } from "react";
import { makeRequest } from "../helpers";
import config from '../config.json';

const URL = `http://localhost:${config.BACKEND_PORT}`;

const TaskAttachmentsModalContent = forwardRef((props, ref) => {

  const [files, setFiles] = useState(props.files);
  const [rerender, setRerender] = useState(" ");

  const handleUpload = async (event) => {
    event.preventDefault();
    event.stopPropagation();

    const body = new FormData();
    body.append('file', event.target.files[0])

    const response = await fetch(`${URL}/upload_file1`, {
      method: "POST",
      headers: {'Authorization': `${props.uid}`},
      body
    });
    const data1 = await response.json();

    const data2 = await makeRequest("/upload_file2", "POST", {file: data1, destination_name: data1, tid: props.tid}, props.uid);
    console.log(data2)
    const newFiles = files;
    newFiles.push(data2);
    setFiles(newFiles);
    setRerender("  ");
    setRerender(" ");
  }

  return (
    <div id="attachment-modal">
      <label htmlFor="file-upload" id="file-upload-button">Upload File</label>
      <input type="file" id="file-upload" className="hide" onChange={handleUpload} />

      {files.length !== 0 ? files.map((file, idx) => {
        return <a key={idx} href={file.link} target="_blank" download={file.file}>{file.file}</a>
      }) : "No files attached."}
      {rerender}
    </div>
  );
});

export default TaskAttachmentsModalContent;