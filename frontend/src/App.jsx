import './App.css';
import Auth from './Pages/Auth.jsx';
import Site from './Components/Site.jsx';
import firebase from 'firebase/compat/app';
import { useState, useEffect } from 'react';

const firebaseConfig = {"apiKey": "AIzaSyCODWXHzh67zRV-xq9ZFAZ4sVaqKwUq9cY",
"authDomain": "taskforge-9aea9.firebaseapp.com",
"databaseURL": "https://taskforge-9aea9-default-rtdb.firebaseio.com",
"projectId": "taskforge-9aea9",
"storageBucket": "taskforge-9aea9.appspot.com",
"messagingSenderId": "221747524877",
"appId": "1:221747524877:web:8785cfe8e0847bd257ec44",
"measurementId": "G-5N1VTMSWEC"
}
const firebaseApp = firebase.initializeApp(firebaseConfig)

const App = () => {
  const [isSignedIn, setIsSignedIn] = useState(false)
  const [isLoading, setIsLoading] = useState("Loading...")

  useEffect(() => {
    const unregisterAuthObserver = firebase.auth().onAuthStateChanged(user => {
      setIsSignedIn(!!user);
      setIsLoading(false);
    });
    return () => unregisterAuthObserver();
  }, []);

  return (
    isLoading || (
      isSignedIn 
      ? <Site firebaseApp={firebaseApp} />
      : <Auth />
    )
  )
}

export default App;
