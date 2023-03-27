import React, { useState } from "react";
import './SettingsContainer.css'
import { Modal } from "@mui/material";
import SettingsModalSearch from './SettingsModalSearch.jsx'

const SettingsContainer = ({ title, description, buttons }) => {
  const [open, setOpen] = useState(false);
  const [modalTitle, setModalTitle] = useState('');
  const [modalAction, setModalAction] = useState('');
  const [warning, setWarning] = useState('');
  const handleClose = () => { setOpen(false) };
  const handleOpen = (buttonLabel, buttonWarning) => { setOpen(true), setModalTitle(`${buttonLabel} User`), setModalAction(buttonLabel), setWarning(buttonWarning) };

  return (
    <>
      <div className="settings-container">
        <h3 className="settings-title">{title}</h3>
        <p className="settings-description">{description}</p>
        <div className="settings-divider"></div>
        <div className="settings-buttons">
          {buttons.map(button => (
            <button key={button.id} onClick={() => handleOpen(button.action, button.warning)}>
              <img src={button.icon}></img> {button.action} User </button>
          ))}
        </div>
      </div>
      <Modal open={open} onClose={handleClose}>
        <SettingsModalSearch title={`${modalTitle}`} onClose={handleClose} action={`${modalAction}`} warning={`${warning}`} />
      </Modal>
    </>
  )
}

export default SettingsContainer;
