import React from "react";

const Home = ({ firebaseApp }) => {
  return (
    <>
      Welcome {firebaseApp.auth().currentUser.displayName}! You are now signed-in!
    </>
  )
}

export default Home;
