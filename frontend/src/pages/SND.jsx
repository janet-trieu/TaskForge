import React, { useState, useEffect } from "react";
import Chart from 'chart.js/auto';
import { makeRequest } from '../helpers';

const SND = ({ firebaseApp }) => {
  const [details, setDetails] = useState();
  const [isLoading, setIsLoading] = useState("Loading...");
  const uid = firebaseApp.auth().currentUser.uid;

  useEffect(async () => {
    let data = null;
    if (location.pathname === '/snd') {
      data = await makeRequest(`/workload/get_supply_demand?uid=${uid}`, 'GET', null, uid);
      if (data.error) alert(data.error);
      else {
        setIsLoading(false);
      }
    } else {
      const requested_uid = location.pathname.split('/')[2];
      data = await makeRequest(`/workload/get_supply_demand?uid=${requested_uid}`, 'GET', null, uid);
      if (data.error) alert(data.error);
      else {
        setIsLoading(false);
      }
    }
    
    const ctx = document.getElementById('sndChart').getContext('2d');
    const chart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Supply / Availability', 'Demand / Task Workload'],
        datasets: [{
          label: 'Supply & Demand',
          data: [data[0].supply, data[0].demand],
          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)'
          ],
          borderColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)'
          ],
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });
  }, []);

  return (
    <canvas id="sndChart"></canvas>
  )
}

export default SND;