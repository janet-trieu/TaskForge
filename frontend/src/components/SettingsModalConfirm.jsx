import React from "react";
import './SettingsModal.css'

const SettingsModalConfirm = ({ title, onClose, action, warning }) => {
    return (
        <>
            <div className="settings-modal">
                <div className="settings-modal-content">
                    <div className="settings-modal-header">
                        <h3 className="settings-modal-title">{title}</h3>
                    </div>
                    <div className="settings-modal-body">
                        Are you sure you want to {action.toLowerCase()} <h2>FULLNAME UID?</h2>
                    </div>
                    <div className="settings-modal-warning">{warning}</div>
                    <div className="settings-modal-footer">
                        <button className="button-cancel" onClick={onClose}>Cancel</button>
                        <button className="button-confirm" onClick={onClose}>{action}</button>
                    </div>
                </div>
            </div>
        </>
    )
}

export default SettingsModalConfirm;