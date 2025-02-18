import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [donations, setDonations] = useState(null);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);

  useEffect(() => {
    const fetchDonations = async () => {
      try {
        const response = await fetch('https://raw.githubusercontent.com/eacopela/donation-tracker/main/data/donations.json');
        const data = await response.json();
        setDonations(data);
        setLastUpdated(new Date(data.lastUpdated).toLocaleString());
      } catch (err) {
        setError('Error fetching donation data');
        console.error('Error:', err);
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
      <h1>Donation Tracker</h1>
      <p>{error}</p>
    </div>;
  }

  if (!donations) {
    return <div className="App loading">
      <h1>Donation Tracker</h1>
      <p>Loading donation data...</p>
    </div>;
  }

  return (
    <div className="App">
      <h1>Donation Tracker</h1>
      
      <div className="donations">
        <div className="donation-card">
          <h2>Fallen Patriots</h2>
          <p className="amount">${donations.fallenPatriots.toLocaleString()}</p>
        </div>

        <div className="donation-card">
          <h2>YouTube</h2>
          <p className="amount">${donations.youtube.toLocaleString()}</p>
        </div>

        <div className="donation-card total">
          <h2>Total</h2>
          <p className="amount">${donations.total.toLocaleString()}</p>
        </div>
      </div>

      <p className="last-updated">Last updated: {lastUpdated}</p>
    </div>
  );
}

export default App;
