import { Routes, Route } from 'react-router-dom';
import Home from '../Pages/Home.jsx'
import Test from '../pages/Test.jsx';

const Site = ({ firebaseApp }) => {
  return (
    <>
      <Routes>
        <Route path='/' element={<Home firebaseApp={firebaseApp} />} />
        <Route path='/test' element={<Test />} />
      </Routes>
    </>
  )
}

export default Site;
