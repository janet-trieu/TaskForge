import React, { useState } from "react";
import './SettingsContainer.css'
import { Modal } from "@mui/material";
import SettingsModalSearch from './SettingsModalSearch.jsx'
import SettingsModalConfirm from './SettingsModalConfirm.jsx'

const SettingsContainer = ({ firebaseApp, title, description, buttons }) => {
  const [open, setOpen] = useState(false);
  const [modalTitle, setModalTitle] = useState('');
  const [modalAction, setModalAction] = useState('');
  const [warning, setWarning] = useState('');
  const [modalType, setModalType] = useState('');
  const handleClose = () => { setOpen(false) };
  const handleOpen = (buttonLabel, buttonWarning, buttonType) => { setOpen(true), setModalTitle(`${buttonLabel}`), setModalAction(buttonLabel), setWarning(buttonWarning), setModalType(buttonType) };

  const renderModal = () => {
    switch (modalType) {
      case 'uid search':
        return <Modal open={open} onClose={handleClose}>
          <SettingsModalSearch title={`${modalTitle}`} onClose={handleClose} action={`${modalAction}`} warning={`${warning}`} />
        </Modal>
      case 'confirm':
        return <Modal open={open} onClose={handleClose}>
        <SettingsModalConfirm firebaseApp={firebaseApp} title={`${modalTitle}`} onClose={handleClose} action={`${modalAction}`} warning={`${warning}`} />
      </Modal>
      default:
        return null;
    }
  };

  return (
    <>
      <div className="settings-container">
        <h3 className="settings-title">{title}</h3>
        <p className="settings-description">{description}</p>
        <div className="settings-divider"></div>
        <div className="settings-buttons">
          {buttons.map(button => (
            <button key={button.id} onClick={() => handleOpen(button.action, button.warning, button.type)}>
              <img src={button.icon}></img> {button.action} </button>
          ))}
        </div>
      </div>
      {renderModal()}
    </>
  )
}

export default SettingsContainer;
