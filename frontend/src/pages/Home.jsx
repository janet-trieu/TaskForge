import React from "react";

const Home = ({ firebaseApp }) => {
  return (
    <>
      <p>Welcome {firebaseApp.auth().currentUser.displayName}! You are now signed-in! Peepo</p>
      <button onClick={() => {
        firebaseApp.auth().signOut();
      }}>Sign-out</button>
    </>
  )
}

export default Home;
