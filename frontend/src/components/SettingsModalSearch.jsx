import React, { useState, forwardRef } from "react";
import './SettingsModal.css'
import './Searchbar.css';
import { makeRequest } from "../helpers";

const SettingsModalSearch = forwardRef(({ firebaseApp, title, onClose, action, warning }, ref) => {
  const handleConfirm = async (action, warning, event) => {
    event.preventDefault();
    if (!event.target.searchbar.value) {
      alert("Please enter an email.");
      return;
    }
    
    const emailRegex = /^\S+@\S+\.\S+$/;
    const inputValue = event.target.searchbar.value.trim();
    if (!emailRegex.test(inputValue)) {
      alert("Please enter a valid email address.");
      return;
    }

    const msg = `Are you sure you want to continue? ${warning}`

    if (window.confirm(msg)) {
      let route = null;
      switch (action.toLowerCase()) {
        case 'admin user':
          route = "give_admin";
          break;
        case 'ban user':
          route = "ban_user";
          break;
        case 'unban user':
          route = "unban_user";
          break;
        case 'remove user':
          route = "remove_user";
          break;
        case 'restore user':
          route = "readd_user";
          break;
      }
      const data = makeRequest(`/admin/${route}`, 'POST', {uid_user: event.target.searchbar.value}, firebaseApp.auth().currentUser.uid);
      if (data.error) alert(data.error);
    }
    onClose();
  }

  return (
    <>
      <div className="settings-modal">
        <form className="settings-modal-content" onSubmit={(event) => handleConfirm(action, warning, event)}>
          <div className="settings-modal-header">
            <h3 className="settings-modal-title">{title}</h3>
          </div>
          <div className="settings-modal-body">
            <input id="searchbar" placeholder="Enter user's email" />
          </div>
          <div className="settings-modal-footer">
            <button className="button-cancel" onClick={onClose}>Cancel</button>
            <button className="button-confirm" type="submit" >{action}</button>
          </div>
        </form>
      </div>
    </>
  )
});

export default SettingsModalSearch;