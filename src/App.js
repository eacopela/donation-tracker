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
