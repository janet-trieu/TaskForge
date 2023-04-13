import React, { forwardRef, useState } from "react";
import { makeRequest } from "../helpers";
import styled from "styled-components";

const CommentCard = styled.div`
  padding: 0.5em;
  background-color: lightgray;
  border-radius: 0.5em;
  margin-top: 0.5em;
`;
const DisplayName = styled.h4`
  margin: 0;
`

const TaskCommentsModalContent = forwardRef((props, ref) => {

  const [comments, setComments] = useState(props.comments);
  const [rerender, setRerender] = useState(" ");

  const handleSubmit = async (event) => {
    event.preventDefault();
    event.stopPropagation();
    const comment = event.target.comment.value;
    event.target.comment.value = "";
    if (!comment) {alert("Comment cannot be empty."); return;}

    const data = await makeRequest('/task/comment', 'POST', {tid: props.tid, comment}, props.uid);
    if (data.error) alert(data.error);
    else {
      let temp = comments;
      temp.unshift(data);
      setComments(temp);
      setRerender("  ");
      setRerender(" ");
    };
  }

  return (
    <div id="task-comment-modal">
      <form id="comment-send" onSubmit={handleSubmit}>
        <input type="text" id="comment" name="comment" placeholder="Write something..." />
        &nbsp;&nbsp;
        <button type="submit">Send Comment</button>
      </form>
      <div>
        {comments.map(comment => {
          return <CommentCard><DisplayName>{comment.display_name}</DisplayName>{comment.comment}</CommentCard>
        })}
      </div>
      {rerender}
    </div>
  );
});

export default TaskCommentsModalContent;