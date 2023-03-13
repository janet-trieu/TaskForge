import { Routes, Route } from 'react-router-dom';
import Home from '../Pages/Home.jsx'
import Header from './Header.jsx';
import Sidebar from './Sidebar.jsx';

const Site = ({ firebaseApp }) => {
  return (
    <div id='site-container'>
      <Sidebar firebaseApp={firebaseApp}/>
      <div className='vertical-line' />
      <div id='right-container'>
        <Header />
        <Routes>
          <Route path='/' element={<Home firebaseApp={firebaseApp} />} />
        </Routes>
      </div>
    </div>
  )
}

export default Site;
