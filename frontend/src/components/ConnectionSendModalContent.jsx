import React, { forwardRef, useState, useEffect } from "react";
import { makeRequest } from "../helpers";

const ConnectionSendModalContent = forwardRef((props, ref) => {

  const handleSubmit = async (event) => {
    event.preventDefault();
    console.log(event.target.connectionInvite.value);
    //const data = await makeRequest('/notification/connection/request', 'POST', {email: event.target.connectionInvite.value});
    props.handleClose();
  }

  return (
    <form id="connection-send-modal" onSubmit={handleSubmit}>
      <label htmlFor="connectionInvite"><h3 style={{margin: '0'}}>Requestee Email</h3></label>
      <input id="connectionInvite" name="connectionInvite" type="text" placeholder="e.g. user@email.com" />
      <br />
      <br />
      <button type="submit">Send Request</button>
    </form>
  );
});

export default ConnectionSendModalContent;