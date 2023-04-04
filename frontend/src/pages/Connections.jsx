import React, { useState, useEffect } from "react";
import ConnectionsSearchbar from "../components/ConnectionsSearchbar";
import ConnectionCard from '../components/ConnectionCard';
import ConnectionSendModalContent from '../components/ConnectionSendModalContent';
import { makeRequest } from "../helpers";
import './Connections.css'
import { Modal } from '@mui/material';

const Connections = ({ firebaseApp }) => {
  const [isLoading, setIsLoading] = useState('Loading...');
  const [connections, setConnections] = useState();
  const [openConnectionSend, setOpenConnectionSend] = useState(false);
  const handleOpenConnectionSend = () => { setOpenConnectionSend(true) };
  const handleCloseConnectionSend = () => { setOpenConnectionSend(false) };
  const currentUser = firebaseApp.auth().currentUser;

  useEffect(async () => {
    const data = await makeRequest('/connections/get_connected_taskmasters', 'GET', null, currentUser.uid);
    if (data.error) alert(data.error);
    else {
      setConnections(data);
      setIsLoading(false);
    }
  }, []);

  return (
    <>
      <div id="connections-container">
        <div id="connections-header">
          <h3 id="connections-title">{currentUser.displayName}'s Connections</h3>
          <button onClick={handleOpenConnectionSend}>Send Connection Request</button>
          <Modal open={openConnectionSend} onClose={handleCloseConnectionSend}>
            <ConnectionSendModalContent handleClose={handleCloseConnectionSend} uid={currentUser.uid} />
          </Modal>
          <ConnectionsSearchbar />
        </div>
        {isLoading || (
          <div id="connections-card-container">
            {connections.map(connection => {
              return <ConnectionCard key={connection.uid} firebaseApp={firebaseApp} photo={connection.photo_url} displayName={connection.display_name} role={connection.role} />
            })}
          </div>
        )}
      </div>
    </>
  )
}

export default Connections;
