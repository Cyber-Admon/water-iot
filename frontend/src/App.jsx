import { useState, useEffect } from "react";
import { getLatestReadings, getReadingsHistory, getAlerts } from "./api";
import ReadingsTable from "./components/ReadingsTable";
import TrendChart from "./components/TrendChart";

const POLL_INTERVAL_MS = 5000; // how often the dashboard refreshes

function App() {
  const [latestReadings, setLatestReadings] = useState([]);
  const [history, setHistory] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [error, setError] = useState(null);

  // fetchData is defined once, then called immediately and on an interval.
  // This is the standard React pattern for "poll an API every N seconds."
  const fetchData = async () => {
    try {
      const latest = await getLatestReadings();
      setLatestReadings(latest);

      // For now we chart node-01's history. Once you have multiple
      // real nodes deployed, this can become a dropdown selector.
      const historyData = await getReadingsHistory("node-01", 50);
      setHistory(historyData);

      const alertData = await getAlerts(10);
      setAlerts(alertData);

      setError(null);
    } catch (err) {
      setError("Could not reach the backend. Is it running?");
    }
  };

  useEffect(() => {
    fetchData(); // run once immediately on page load
    const interval = setInterval(fetchData, POLL_INTERVAL_MS);
    return () => clearInterval(interval); // cleanup when component unmounts
  }, []);

  return (
    <div style={{ fontFamily: "sans-serif", padding: "24px", maxWidth: "960px", margin: "0 auto" }}>
      <h1>Water Pollution Monitoring Dashboard</h1>
      <p style={{ color: "#666" }}>
        Auto-refreshing every {POLL_INTERVAL_MS / 1000} seconds.
      </p>

      {error && (
        <div style={{ background: "#FFEBEE", color: "#B71C1C", padding: "10px", borderRadius: "6px", marginBottom: "16px" }}>
          {error}
        </div>
      )}

      <h2>Latest Readings</h2>
      <ReadingsTable readings={latestReadings} />

      <h2 style={{ marginTop: "32px" }}>Trend (node-01)</h2>
      <TrendChart readings={history} />

      <h2 style={{ marginTop: "32px" }}>Recent Alerts</h2>
      {alerts.length === 0 ? (
        <p>No alerts yet.</p>
      ) : (
        <ul>
          {alerts.map((a) => (
            <li key={a.id}>
              <strong>{a.severity.toUpperCase()}</strong> — {a.message}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default App;
