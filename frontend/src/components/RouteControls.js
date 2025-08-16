import React, { useState } from 'react';

export default function RouteControls({ onSubmit, onShare, values }) {
  const [from, setFrom] = useState(values.from || '');
  const [to, setTo] = useState(values.to || '');
  const [mode, setMode] = useState(values.mode || 'DRIVING');

  function handleSubmit(e) {
    e.preventDefault();
    onSubmit({ from, to, mode });
  }

  return (
    <form className="controls" onSubmit={handleSubmit} style={{gap:10}}>
      <input value={from} onChange={e => setFrom(e.target.value)} placeholder="From location" />
      <input value={to} onChange={e => setTo(e.target.value)} placeholder="To location" />
      <select value={mode} onChange={e => setMode(e.target.value)}>
        <option value="DRIVING">By Road</option>
        <option value="TRANSIT">By Train</option>
        <option value="FLIGHT">By Air</option>
      </select>
      <button type="submit">Show Route</button>
      <button type="button" style={{background:'#25D366'}} onClick={() => onShare({ from, to, mode })}>Share</button>
    </form>
  );
}

