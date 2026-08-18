import { useState, useEffect } from "react";
import { getLatestReadings, getReadingsHistory, getAlerts, getClassification } from "./api";
import ReadingsTable from "./components/ReadingsTable";
import TrendChart from "./components/TrendChart";

const POLL_INTERVAL_MS = 5000; // how often the dashboard refreshes

function App() {
  const [latestReadings, setLatestReadings] = useState([]);
  const [history, setHistory] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [classification, setClassification] = useState(null);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    try {
      const latest = await getLatestReadings();
      setLatestReadings(latest);

      const historyData = await getReadingsHistory("node-01", 50);
      setHistory(historyData);

      const alertData = await getAlerts(10);
      setAlerts(alertData);

      try {
        const classResult = await getClassification("node-01");
        setClassification(classResult);
      } catch {
        setClassification(null); // no readings yet for this node, fine to ignore
      }

      setError(null);
    } catch (err) {
      setError("Could not reach the backend. Is it running?");
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, POLL_INTERVAL_MS);
    return () => clearInterval(interval);
  }, []);

  const classificationColor =
    classification?.usability_class === "Potable" ? "#E8F5E9" :
    classification?.usability_class === "Treatment Recommended" ? "#FFF3E0" :
    "#FFEBEE";

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

      {classification && (
        <div style={{
          background: classificationColor,
          padding: "16px",
          borderRadius: "8px",
          marginTop: "16px",
          marginBottom: "16px"
        }}>
          <h3 style={{ margin: "0 0 8px 0" }}>Water Usability: {classification.usability_class}</h3>
          <p style={{ margin: 0, color: "#444" }}>{classification.guidance}</p>
        </div>
      )}

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