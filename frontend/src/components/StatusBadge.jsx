// A small, reusable piece of UI. Any component that needs to show
// a safe/warning/danger status imports this instead of repeating
// the color logic everywhere.

const STATUS_COLORS = {
  safe: "#2E7D32",
  warning: "#EF6C00",
  danger: "#B71C1C",
};

const STATUS_LABELS = {
  safe: "Safe",
  warning: "Warning",
  danger: "Danger",
};

function StatusBadge({ status }) {
  if (!status) return <span style={{ color: "#999" }}>—</span>;

  const color = STATUS_COLORS[status] || "#999";
  const label = STATUS_LABELS[status] || status;

  return (
    <span
      style={{
        backgroundColor: color,
        color: "white",
        padding: "2px 10px",
        borderRadius: "12px",
        fontSize: "0.8rem",
        fontWeight: 600,
      }}
    >
      {label}
    </span>
  );
}

export default StatusBadge;
