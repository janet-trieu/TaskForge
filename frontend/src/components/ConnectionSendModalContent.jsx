import React, { forwardRef, useState, useEffect } from "react";
import { makeRequest } from "../helpers";

const ConnectionSendModalContent = forwardRef((props, ref) => {
  const [buttonText, setButtonText] = useState("Send Request");
  const handleSubmit = async (event) => {
    event.preventDefault();

    if (buttonText === "...") return;
    setButtonText("...");

    const data = await makeRequest('/notification/connection/request', 'POST', {user_email: event.target.connectionInvite.value}, props.uid);
    setButtonText("Send Request");
    if (data.error) alert(data.error);
    else props.handleClose();
  }

  return (
    <form id="connection-send-modal" onSubmit={handleSubmit}>
      <label htmlFor="connectionInvite"><h3 style={{margin: '0'}}>Requestee Email</h3></label>
      <input id="connectionInvite" name="connectionInvite" type="text" placeholder="e.g. user@email.com" />
      <br />
      <br />
      <button type="submit">{buttonText}</button>
    </form>
  );
});

export default ConnectionSendModalContent;