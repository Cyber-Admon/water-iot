import StatusBadge from "./StatusBadge";

// Receives readings as a prop — it doesn't fetch data itself.
// This separation matters: this component only cares about *displaying*
// data, not *how* the data was obtained. App.jsx handles fetching.

function ReadingsTable({ readings }) {
  if (!readings || readings.length === 0) {
    return <p>No readings yet. Waiting for data from a node...</p>;
  }

  return (
    <table style={{ width: "100%", borderCollapse: "collapse" }}>
      <thead>
        <tr style={{ borderBottom: "2px solid #ddd", textAlign: "left" }}>
          <th style={{ padding: "8px" }}>Node</th>
          <th style={{ padding: "8px" }}>Turbidity (NTU)</th>
          <th style={{ padding: "8px" }}>pH</th>
          <th style={{ padding: "8px" }}>TDS (ppm)</th>
          <th style={{ padding: "8px" }}>Temp (°C)</th>
          <th style={{ padding: "8px" }}>Received</th>
        </tr>
      </thead>
      <tbody>
        {readings.map((r) => (
          <tr key={r.id} style={{ borderBottom: "1px solid #eee" }}>
            <td style={{ padding: "8px" }}>{r.node_id}</td>
            <td style={{ padding: "8px" }}>
              {r.turbidity_ntu} <StatusBadge status={r.turbidity_status} />
            </td>
            <td style={{ padding: "8px" }}>
              {r.ph} <StatusBadge status={r.ph_status} />
            </td>
            <td style={{ padding: "8px" }}>
              {r.tds_ppm} <StatusBadge status={r.tds_status} />
            </td>
            <td style={{ padding: "8px" }}>{r.temperature_c}</td>
            <td style={{ padding: "8px" }}>
              {new Date(r.received_at).toLocaleTimeString()}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default ReadingsTable;
