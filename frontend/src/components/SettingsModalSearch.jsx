import React, { useState } from "react";
import './SettingsModal.css'
import './Searchbar.css';
import { Modal } from "@mui/material";
import SettingsModalConfirm from "./SettingsModalConfirm";

const SettingsModalSearch = ({ title, onClose, action, warning }) => {
    const [open, setOpen] = useState(false);
    const handleClose = () => { setOpen(false) };
    const handleOpen  = () => { setOpen(true) };

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
                        <button className="button-confirm" onClick={handleOpen}>{action}</button>
                    </div>
                </div>
            </div>
            <Modal open={open} onClose={handleClose}>
                <SettingsModalConfirm title={title} onClose={handleClose} action={action} warning={warning} />
            </Modal>
        </>
    )
}

export default SettingsModalSearch;