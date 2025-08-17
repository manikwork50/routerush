import React from 'react';
import React, { useState } from 'react';

function MapPage() {
  const [from, setFrom] = useState('');
  const [to, setTo] = useState('');
  const [mode, setMode] = useState('DRIVING');

  const handleSubmit = e => {
    e.preventDefault();
    // Here you’ll add route calculation logic (coming soon)
    alert(`Route from: ${from}\nTo: ${to}\nMode: ${mode}`);
  };

  return (
    <div style={{ maxWidth: 700, margin: "0 auto", padding: "40px 10px" }}>
      <h2 style={{ color: "#FF5E00" }}>Plan Your Trip</h2>
      <form onSubmit={handleSubmit} style={{ margin: "20px 0" }}>
        <input placeholder="From location" value={from} onChange={e => setFrom(e.target.value)} required style={{ margin: 4, padding: 8 }} />
        <input placeholder="To location" value={to} onChange={e => setTo(e.target.value)} required style={{ margin: 4, padding: 8 }} />
        <select value={mode} onChange={e => setMode(e.target.value)} style={{ margin: 4, padding: 8 }}>
          <option value="DRIVING">By Road</option>
          <option value="TRANSIT">By Train</option>
          <option value="FLIGHT">By Air</option>
        </select>
        <button type="submit" style={{ margin: 6, padding: "8px 20px", background: "#FF5E00", color: "#fff", border: "none", borderRadius: "5px" }}>Show Route</button>
      </form>
    </div>
  );
}

export default MapPage;


function MapPage() {
  return (
    <div>
      <h2>Plan Your Trip - Interactive Route Mapper</h2>
      <p>Use the controls to find the best routes, fares, and travel modes across India!</p>
    </div>
  );
}

export default MapPage;
import React from 'react';