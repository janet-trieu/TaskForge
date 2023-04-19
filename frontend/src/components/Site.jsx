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
import Achievements from '../pages/Achievements.jsx';
import Reputation from '../pages/Reputation.jsx';
import SND from '../pages/SND.jsx';

const Site = ({ firebaseApp }) => {
  return (
    <div id='site-container'>
      <Sidebar firebaseApp={firebaseApp} />
      <div className='vertical-line' />
      <div id='right-container'>
        <Header firebaseApp={firebaseApp} />
        <Routes>
          <Route path='/' element={<Home firebaseApp={firebaseApp} />} />
          <Route path='/projects' element={<Projects firebaseApp={firebaseApp} />} />
          <Route path='/projects/create' element={<CreateProject firebaseApp={firebaseApp}/>} />
          <Route path='/projects/:pid' element={<ProjectBoardView firebaseApp={firebaseApp}/>} />
          <Route path='/projects/:pid/board' element={<ProjectBoardView firebaseApp={firebaseApp}/>} />
          <Route path='/projects/:pid/task' element={<ProjectTaskView firebaseApp={firebaseApp}/>} />
          <Route path='/tasks' element={<Tasks firebaseApp={firebaseApp} />} />
          <Route path='/tasks/:uid' element={<Tasks firebaseApp={firebaseApp} />} />
          <Route path='/profile' element={<Profile firebaseApp={firebaseApp} />} />
          <Route path='/profile/:uid' element={<Profile firebaseApp={firebaseApp} />} />
          <Route path='/connections' element={<Connections firebaseApp={firebaseApp} />} />
          <Route path='/settings' element={<Settings firebaseApp={firebaseApp} />} />
          <Route path='/achievements' element={<Achievements firebaseApp={firebaseApp} />} />
          <Route path='/achievements/:uid' element={<Achievements firebaseApp={firebaseApp} />} />
          <Route path='/reputation' element={<Reputation firebaseApp={firebaseApp} />} />
          <Route path='/reputation/:uid' element={<Reputation firebaseApp={firebaseApp} />} />
          <Route path='/snd' element={<SND firebaseApp={firebaseApp} />} />
          <Route path='/snd/:uid' element={<SND firebaseApp={firebaseApp} />} />
        </Routes>
      </div>
    </div>
  )
}

export default Site;
