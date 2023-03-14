import { Routes, Route } from 'react-router-dom';
import Connections from '../pages/Connections.jsx';
import CreateProject from '../pages/CreateProject.jsx';
import Home from '../Pages/Home.jsx'
import Profile from '../pages/Profile.jsx';
import Projects from '../pages/Projects.jsx';
import Settings from '../pages/Settings.jsx';
import Tasks from '../pages/Tasks.jsx';
import Header from './Header.jsx';
import Sidebar from './Sidebar.jsx';

const Site = ({ firebaseApp }) => {
  return (
    <div id='site-container'>
      <Sidebar firebaseApp={firebaseApp} />
      <div className='vertical-line' />
      <div id='right-container'>
        <Header />
        <Routes>
          <Route path='/' element={<Home firebaseApp={firebaseApp} />} />
          <Route path='/projects' element={<Projects />} />
          <Route path='/projects/create' element={<CreateProject firebaseApp={firebaseApp}/>} />
          <Route path='/tasks' element={<Tasks />} />
          <Route path='/profile' element={<Profile />} />
          <Route path='/connections' element={<Connections />} />
          <Route path='/settings' element={<Settings />} />
        </Routes>
      </div>
    </div>
  )
}

export default Site;
