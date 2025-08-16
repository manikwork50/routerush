import React from 'react';
import { Map, GoogleApiWrapper, DirectionsRenderer } from 'google-maps-react';

function MapView({ google, directions }) {
  return (
    <div style={{ width: "100%", height: "60vh" }}>
      <Map
        google={google}
        zoom={5}
        initialCenter={{ lat: 22.9734, lng: 78.6569 }}
        style={{ width:'100%', height:'100%' }}
        disableDefaultUI={true}
      >
        {directions && <DirectionsRenderer directions={directions}/>}
      </Map>
    </div>
  );
}

export default GoogleApiWrapper({
  apiKey: 'YOUR_GOOGLE_MAPS_API_KEY',
  libraries: ['places']
})(MapView);

