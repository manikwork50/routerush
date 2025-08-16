const { useEffect, useMemo, useRef, useState } = React;

function useIntersection() {
  const ref = useRef(null);
  const [visible, setVisible] = useState(false);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const io = new IntersectionObserver(([e]) => {
      if (e.isIntersecting) {
        setVisible(true);
        io.unobserve(el);
      }
    }, { threshold: 0.08 });
    io.observe(el);
    return () => io.disconnect();
  }, []);
  return [ref, visible];
}

function Controls({ q, setQ, sort, setSort }) {
  return (
    <div className="controls" role="region" aria-label="Filters">
      <input
        className="search"
        placeholder="Search state (e.g., Kerala, Rajasthan)…"
        value={q}
        onChange={e=>setQ(e.target.value)}
        aria-label="Search"
      />
      <select
        value={sort}
        onChange={e=>setSort(e.target.value)}
        className="select"
        aria-label="Sort"
      >
        <option value="popularity">Sort: Popularity</option>
        <option value="az">Sort: A → Z</option>
      </select>
    </div>
  );
}

function Card({ item }) {
  const [ref, show] = useIntersection();
  return (
    <a ref={ref} className={`card ${show ? 'show' : ''}`} href={`${item.slug}.html`} title={`Open ${item.name}`}>
      <span className="thumb">
        <img loading="lazy" src={item.image} alt={`${item.name} cover`} />
      </span>
      <div className="content">
        <h3 className="title">{item.name}</h3>
        <div className="meta">Capital: {item.capital} • Language: {item.lang}</div>
        {item.badge && <span className="badge">{item.badge}</span>}
      </div>
    </a>
  );
}

function Grid({ data }) {
  return (
    <div className="grid" aria-live="polite">
      {data.map(item => <Card key={item.slug} item={item} />)}
    </div>
  );
}

function App() {
  const [raw, setRaw] = useState([]);
  const [q, setQ] = useState('');
  const [sort, setSort] = useState('popularity');

  // Load data
  useEffect(() => {
    fetch('/api/states')
      .then(r => r.json())
      .then(setRaw)
      .catch(console.error);
  }, []);

  // Listen to chip events (hero chips)
  useEffect(() => {
    function onChip(e){ setQ(e.detail || ''); }
    window.addEventListener('wm-chip', onChip);
    return () => window.removeEventListener('wm-chip', onChip);
  }, []);

  const data = useMemo(() => {
    const s = q.trim().toLowerCase();
    let filtered = !s ? raw : raw.filter(x =>
      x.name.toLowerCase().includes(s) ||
      (x.badge || '').toLowerCase().includes(s) ||
      (x.capital || '').toLowerCase().includes(s)
    );

    if (sort === 'az') {
      filtered = [...filtered].sort((a,b)=> a.name.localeCompare(b.name));
    } else {
      filtered = [...filtered].sort((a,b)=> (b.popularity || 0) - (a.popularity || 0));
    }
    return filtered;
  }, [raw, q, sort]);

  return (
    <>
      <Controls q={q} setQ={setQ} sort={sort} setSort={setSort} />
      <Grid data={data} />
    </>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
