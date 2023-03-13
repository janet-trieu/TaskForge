import { Routes, Route } from 'react-router-dom';
import Home from '../Pages/Home.jsx'
import Test from '../pages/Test.jsx';
import Sidebar from './Sidebar.jsx';

const Site = ({ firebaseApp }) => {
  return (
    <div id='site-container'>
      <Sidebar firebaseApp={firebaseApp}/>
      <div className='vertical-line' />
      <Routes>
        <Route path='/' element={<Home firebaseApp={firebaseApp} />} />
        <Route path='/test' element={<Test />} />
      </Routes>
    </div>
  )
}

export default Site;
