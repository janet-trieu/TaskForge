import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { makeRequest } from '../helpers';

const ProjectTaskView = ({firebaseApp}) => {
  const [isLoading, setIsLoading] = useState('Loading...');
  const [data, setData] = useState();
  const {pid} = useParams();

  useEffect(async () => {
    const data = await makeRequest(`/projects/view?pid=${pid}`, 'GET', null, firebaseApp.auth().currentUser.uid);
  }, [])

  return (
    <>
    </>
  )
}

export default ProjectTaskView;