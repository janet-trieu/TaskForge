import React from "react";
import './SettingsContainer.css'

const SettingsContainer = ({ title, description, buttons }) => {
  return (
    <>
      <div className="settings-container">
        <h3 className="settings-title">{title}</h3>
        <p className="settings-description">{description}</p>
        <div className="settings-divider"></div>
        <div className="settings-buttons">
          {buttons.map(button =>
            <button key={button.id}>
              <img src={button.icon}></img>
              {button.label}
            </button>)}
        </div>
      </div>
    </>
  )
}

export default SettingsContainer;
