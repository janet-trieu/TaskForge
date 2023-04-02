import { Routes, Route } from 'react-router-dom';
import Connections from '../pages/Connections.jsx';
import CreateProject from '../pages/CreateProject.jsx';
import Home from '../pages/Home.jsx'
import Profile from '../pages/Profile.jsx';
import Projects from '../pages/Projects.jsx';
import Settings from '../pages/Settings.jsx';
import Tasks from '../pages/Tasks.jsx';
import Header from './Header.jsx';
import Sidebar from './Sidebar.jsx';
import ProjectBoardView from '../pages/ProjectBoardView.jsx';
import ProjectTaskView from '../pages/ProjectTaskView.jsx';

const Site = ({ firebaseApp }) => {
  return (
    <div id='site-container'>
      <Sidebar firebaseApp={firebaseApp} />
      <div className='vertical-line' />
      <div id='right-container'>
        <Header />
        <Routes>
          <Route path='/' element={<Home firebaseApp={firebaseApp} />} />
          <Route path='/projects' element={<Projects firebaseApp={firebaseApp} />} />
          <Route path='/projects/create' element={<CreateProject firebaseApp={firebaseApp}/>} />
          <Route path='/projects/:pid' element={<ProjectBoardView firebaseApp={firebaseApp}/>} />
          <Route path='/projects/:pid/board' element={<ProjectBoardView firebaseApp={firebaseApp}/>} />
          <Route path='/projects/:pid/task' element={<ProjectTaskView firebaseApp={firebaseApp}/>} />
          <Route path='/tasks' element={<Tasks firebaseApp={firebaseApp} />} />
          <Route path='/profile' element={<Profile firebaseApp={firebaseApp} />} />
          <Route path='/profile/:uid' element={<Profile firebaseApp={firebaseApp} />} />
          <Route path='/connections' element={<Connections firebaseApp={firebaseApp} />} />
          <Route path='/settings' element={<Settings firebaseApp={firebaseApp} />} />
        </Routes>
      </div>
    </div>
  )
}

export default Site;
