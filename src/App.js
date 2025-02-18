import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [donations, setDonations] = useState({
    fallenPatriots: 0,
    youtube: 0,
    total: 0,
    lastUpdated: null
  });

  const fetchDonations = async () => {
    try {
      const response = await fetch('data/donations.json');
      const data = await response.json();
      setDonations(data);
    } catch (error) {
      console.error('Error fetching donations:', error);
    }
  };

  useEffect(() => {
    fetchDonations();
    const interval = setInterval(fetchDonations, 60 * 1000); // Check for updates every minute
    return () => clearInterval(interval);
  }, []);

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  const formatLastUpdated = (dateString) => {
    if (!dateString) return 'Never';
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Donation Tracker</h1>
        <div className="donation-container">
          <div className="donation-item">
            <h2>Fallen Patriots</h2>
            <p>{formatCurrency(donations.fallenPatriots)}</p>
          </div>
          <div className="donation-item">
            <h2>YouTube</h2>
            <p>{formatCurrency(donations.youtube)}</p>
          </div>
          <div className="donation-item total">
            <h2>Total Donations</h2>
            <p>{formatCurrency(donations.total)}</p>
          </div>
        </div>
        <p className="last-updated">
          Last updated: {formatLastUpdated(donations.lastUpdated)}
        </p>
        <p className="update-note">
          (Updates every minute)
        </p>
      </header>
    </div>
  );
}

export default App;
