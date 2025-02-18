import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [donations, setDonations] = useState(null);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);

  useEffect(() => {
    const fetchDonations = async () => {
      try {
        // In development, fetch from public folder, in production from GitHub
        const url = process.env.NODE_ENV === 'development' 
          ? '/donation-tracker/donations.json'
          : 'https://raw.githubusercontent.com/eacopela/donation-tracker/main/data/donations.json';
        
        console.log('Fetching from:', url); // Debug log
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setDonations(data);
        
        // Convert to Eastern Time
        const date = new Date(data.lastUpdated);
        const options = {
          timeZone: 'America/New_York',
          year: 'numeric',
          month: 'numeric',
          day: 'numeric',
          hour: 'numeric',
          minute: 'numeric',
          second: 'numeric',
          hour12: true
        };
        setLastUpdated(date.toLocaleString('en-US', options) + ' ET');
      } catch (err) {
        console.error('Error:', err);
        setError('Error fetching donation data');
      }
    };

    // Fetch immediately
    fetchDonations();

    // Then fetch every minute
    const interval = setInterval(fetchDonations, 60000);

    // Cleanup interval on unmount
    return () => clearInterval(interval);
  }, []);

  if (error) {
    return <div className="App error">
      <p>{error}</p>
    </div>;
  }

  if (!donations) {
    return <div className="App loading">
      <p>Loading...</p>
    </div>;
  }

  return (
    <div className="App">
      <div className="total">
        <span className="dollar">$</span>
        <span className="amount">{donations.total.toLocaleString()}</span>
      </div>
      <div className="last-updated">
        Last updated: {lastUpdated}
      </div>
    </div>
  );
}

export default App;
