import { useState } from "react";

interface Props {
  max: number;
  onChange: (value: number) => void;
}

export default function PopularitySlider({ max, onChange }: Props) {
  const [value, setValue] = useState(0);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = parseInt(e.target.value);
    setValue(val);
    onChange(val);
  };

  const format = (n: number) =>
    n >= 1_000_000 ? `${(n / 1_000_000).toFixed(1)}M` :
    n >= 1_000 ? `${(n / 1_000).toFixed(0)}K` : `${n}`;

  return (
    <div style={{
      position: "fixed",
      top: 24,
      left: 24,
      background: "#0f172a",
      border: "1px solid #1e293b",
      borderRadius: 12,
      padding: "12px 16px",
      zIndex: 100,
      width: 220,
    }}>
      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8 }}>
        <span style={{ color: "#475569", fontSize: 11, fontFamily: "monospace", textTransform: "uppercase", letterSpacing: "0.1em" }}>
          Min Listeners
        </span>
        <span style={{ color: "#f1f5f9", fontSize: 11, fontFamily: "monospace" }}>
          {format(value)}
        </span>
      </div>
      <input
        type="range"
        min={0}
        max={max}
        step={10000}
        value={value}
        onChange={handleChange}
        style={{ width: "100%", accentColor: "#38bdf8" }}
      />
    </div>
  );
}