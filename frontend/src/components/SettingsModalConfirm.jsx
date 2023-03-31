import React from "react";
import { makeRequest } from "../helpers";
import './SettingsModal.css'

const SettingsModalConfirm = ({ firebaseApp, title, onClose, action, warning }) => {
    const handleConfirm = (action) => {
        console.log(action)
        switch (action) {
            case 'Reset Password':
                const uid = firebaseApp.auth().currentUser.uid;
                const data = makeRequest("/authentication/reset_password", "POST", null, uid)
                if (data.error) {
                    alert(data.error)
                } else {
                    alert('Email has been sent.')
                    onClose()
                }
            default:
                onClose()
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
}

export default SettingsModalConfirm;