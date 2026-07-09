import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

// Takes an array of historical readings and plots turbidity, pH, and TDS
// over time on the same chart. Recharts wants data in ascending time order,
// but our API returns newest-first, so we reverse it here.

function TrendChart({ readings }) {
  if (!readings || readings.length === 0) {
    return <p>No historical data yet.</p>;
  }

  const chartData = [...readings]
    .reverse()
    .map((r) => ({
      time: new Date(r.received_at).toLocaleTimeString(),
      Turbidity: r.turbidity_ntu,
      pH: r.ph,
      TDS: r.tds_ppm,
    }));

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="time" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="Turbidity" stroke="#2E7D32" dot={false} />
        <Line type="monotone" dataKey="pH" stroke="#1565C0" dot={false} />
        <Line type="monotone" dataKey="TDS" stroke="#B71C1C" dot={false} />
      </LineChart>
    </ResponsiveContainer>
  );
}

export default TrendChart;
