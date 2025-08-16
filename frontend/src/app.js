import React, { useState, useEffect } from 'react';
import axios from 'axios';
import RouteControls from './components/RouteControls';
import PopularRoutes from './components/PopularRoutes';
import DetailsModal from './components/DetailsModal';
// import MapView from './components/MapView'; // Uncomment if using google-maps-react

function App() {
  const [popularRoutes, setPopularRoutes] = useState([]);
  const [routeDetails, setRouteDetails] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);

  useEffect(() => {
    axios.get('http://localhost:5000/api/popular-routes')
      .then(resp => setPopularRoutes(resp.data));
  }, []);

  const handleSubmit = async ({ from, to, mode }) => {
    // Call Directions API here, set details
    setRouteDetails(`<strong>From:</strong> ${from}<br/><strong>To:</strong> ${to}<br/><em>Sample route details here</em>`);
    setModalOpen(true);
    // Analytics (saves to backend)
    axios.post('http://localhost:5000/api/track-search', { from, to, mode });
  };

  const handleShare = ({ from, to, mode }) => {
    let modeStr = mode === "DRIVING" ? "Road" : mode === "TRANSIT" ? "Train" : "Flight";
    let url = `https://wa.me/?text=${encodeURIComponent(`Check out my route on WanderMap: ${from} → ${to} via ${modeStr}`)}`;
    window.open(url, "_blank");
  };

  const handleRouteSelect = (r) => {
    handleSubmit(r);
  };

  return (
    <div>
      <nav>...nav links here...</nav>
      <RouteControls onSubmit={handleSubmit} onShare={handleShare} values={{}} />
      {/* <MapView directions={null}/> Enable and handle directions fetch */}
      <PopularRoutes routes={popularRoutes} onRouteSelect={handleRouteSelect} />
      <DetailsModal isOpen={modalOpen} details={routeDetails} onClose={() => setModalOpen(false)} />
      {/* AdSense/affiliate widgets */}
      <div className="bottom-ad">{/* Place ads here */}</div>
    </div>
  );
}

export default App;
