import React, { useEffect, useState } from "react";
import './AvailabilityModal.css'
import './Searchbar.css';
import { makeRequest } from "../helpers";

const AvailabilityModal = ({ firebaseApp, handleClose }) => {
  const [ava, setAva] = useState();

  const handleConfirm = async (event) => {
    event.preventDefault();
    if (event.target.searchbar.value) {
      const uid = firebaseApp.auth().currentUser.uid;
      const availability = Number(event.target.searchbar.value);

      if (![0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5].includes(availability)) {
        alert('Enter valid availability. Accepted values range from 0 to 5 with optional 0.5 intervals. e.g. 2.5');
        return;
      }

      const data = makeRequest('/workload/update_user_availability', 'POST', { availability: availability }, uid);
      if (data.error) alert(data.error);
    }
    handleClose();
  }

  useEffect(async () => {
    const uid = firebaseApp.auth().currentUser.uid;
    const data = await makeRequest('/workload/get_availability', 'GET', null, uid);
    if (data.error) alert(data.error);
    else {
      setAva(data);
    }
  }, []);

  return (
    <>
      <div className="availability-modal">
        <form className="availability-modal-content" onSubmit={(event) => handleConfirm(event)}>
          <div className="availability-modal-header">
            <h3 className="availability-modal-title">Availability</h3>
          </div>
          <div className="availability-modal-body">
            <div className="description">You are currently available to work for {ava} day(s).</div>
            <br />
            <br />
            <input id="searchbar" placeholder="Enter value between 0-5, optionally in 0.5 intervals (e.g. 2.5)" />
          </div>
          <div className="availability-modal-footer">
            <button className="button-cancel" onClick={handleClose}>Cancel</button>
            <button className="button-confirm" type="submit" >Save</button>
          </div>
        </form>
      </div>
    </>
  )
}

export default AvailabilityModal;