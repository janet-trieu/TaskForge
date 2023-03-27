import React, { useState } from "react";
import './SettingsModal.css'
import './Searchbar.css';

const SettingsModalSearch = ({ title, onClose, action, warning }) => {
    const handleConfirm = (action, warning) => {
        const msg = `Are you sure you want to ${action.toLowerCase()} FULLNAME UID? ${warning}`
    
        if (window.confirm(msg)) {
            // if action == admin, admin user
            // if action == ban, remove user
            onClose()
        } else {
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
                        <input id="searchbar" placeholder="Enter UID" />
                    </div>
                    <div className="settings-modal-footer">
                        <button className="button-cancel" onClick={onClose}>Cancel</button>
                        <button className="button-confirm" onClick={() => handleConfirm(action, warning)}>{action}</button>
                    </div>
                </div>
            </div>
        </>
    )
}

export default SettingsModalSearch;