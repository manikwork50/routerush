import React from 'react';

export default function PopularRoutes({ routes, onRouteSelect }) {
  return (
    <section className="popular-routes">
      {routes.map((r, i) => (
        <article className="route-card" key={i} onClick={() => onRouteSelect(r)}>
          <h4>{r.from} → {r.to}</h4>
          <p>{r.desc}</p>
          <small>Mode: {r.mode === 'DRIVING' ? "🚗" : r.mode === 'TRANSIT' ? "🚆" : "✈️" }</small>
        </article>
      ))}
    </section>
  );
}

