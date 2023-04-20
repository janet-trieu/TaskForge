import React, { forwardRef } from "react";
import './SettingsModal.css';

const SettingsModalConfirm = forwardRef(({ firebaseApp, title, onClose, action, warning }, ref) => {
  const handleConfirm = async (action) => {
    switch (action) {
      case 'Reset Password':
        const email = firebaseApp.auth().currentUser.email;
        const data = await firebaseApp.auth().sendPasswordResetEmail(email);
        alert("Email sent!");
        onClose();
    }
  }

  return (
    <>
      <div className="settings-modal">
        <div className="settings-modal-content">
          <div className="settings-modal-header">
            <h3 className="settings-modal-title">{title}</h3>
          </div>
          <div className="settings-modal-body">
            Are you sure you want to <h2>{action.toUpperCase()}?</h2>
          </div>
          <div className="settings-modal-warning">{warning}</div>
          <div className="settings-modal-footer">
            <button className="button-cancel" onClick={onClose}>Cancel</button>
            <button className="button-confirm" onClick={() => handleConfirm(action)}>{action}</button>
          </div>
        </div>
      </div>
    </>
  )
});

export default SettingsModalConfirm;