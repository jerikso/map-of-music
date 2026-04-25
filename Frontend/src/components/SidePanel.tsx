import { useState } from "react";
import { getColorForGenre } from "../utils/genreColors";

interface Props {
  max: number;
  activeGenres: Set<string>;
  availableGenres: string[];
  onListenersChange: (value: number) => void;
  onToggleGenre: (genre: string) => void;
  onRemoveGenre: (genre: string) => void;
}

export default function SidePanel({
  max,
  activeGenres,
  availableGenres,
  onListenersChange,
  onToggleGenre,
  onRemoveGenre,
}: Props) {
  const [sliderValue, setSliderValue] = useState(0);
  const [search, setSearch] = useState("");

  const format = (n: number) =>
    n >= 1_000_000 ? `${(n / 1_000_000).toFixed(1)}M` :
    n >= 1_000 ? `${(n / 1_000).toFixed(0)}K` : `${n}`;

  const handleSlider = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = parseInt(e.target.value);
    setSliderValue(val);
    onListenersChange(val);
  };

  const searchResults = search.trim()
    ? availableGenres.filter(g =>
        g.toLowerCase().includes(search.toLowerCase()) &&
        !activeGenres.has(g)
      )
    : [];

  return (
    <div style={{
      position: "fixed",
      top: 24,
      left: 24,
      background: "#0f172a",
      border: "1px solid #1e293b",
      borderRadius: 12,
      padding: "16px",
      zIndex: 100,
      width: 240,
      display: "flex",
      flexDirection: "column",
      gap: 16,
      maxHeight: "calc(100vh - 48px)",
      overflow: "visible",
    }}>

      {/* Popularity slider */}
      <div>
        <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8 }}>
          <span style={{ color: "#475569", fontSize: 11, fontFamily: "monospace", textTransform: "uppercase", letterSpacing: "0.1em" }}>
            Min Listeners
          </span>
          <span style={{ color: "#f1f5f9", fontSize: 11, fontFamily: "monospace" }}>
            {format(sliderValue)}
          </span>
        </div>
        <input
          type="range"
          min={0}
          max={max}
          step={10000}
          value={sliderValue}
          onChange={handleSlider}
          style={{ width: "100%", accentColor: "#38bdf8" }}
        />
      </div>

      <div style={{ borderTop: "1px solid #1e293b" }} />

      {/* Genre search */}
      <div>
        <p style={{ margin: "0 0 8px", color: "#475569", fontSize: 11, fontFamily: "monospace", textTransform: "uppercase", letterSpacing: "0.1em" }}>
          Genres
        </p>

        {/* Search input */}
        <div style={{ position: "relative" }}>
          <input
            value={search}
            onChange={e => setSearch(e.target.value)}
            placeholder="Add genre..."
            style={{
              width: "100%",
              background: "#1e293b",
              border: "1px solid #334155",
              borderRadius: 8,
              padding: "6px 10px",
              color: "#f1f5f9",
              fontSize: 12,
              fontFamily: "monospace",
              outline: "none",
              boxSizing: "border-box",
            }}
          />

          {searchResults.length > 0 && (
            <div style={{
              position: "absolute",
              left: 0,
              right: 0,
              width: "100%",
              background: "#1e293b",
              border: "1px solid #334155",
              borderRadius: 8,
              marginTop: 4,
              zIndex: 200,
            }}>
              {searchResults.map(genre => (
                <button
                  key={genre}
                  onClick={() => {
                    onToggleGenre(genre);
                    setSearch("");
                  }}
                  style={{
                    width: "100%",
                    display: "flex",
                    alignItems: "center",
                    gap: 8,
                    background: "transparent",
                    border: "none",
                    borderBottom: "1px solid #334155",
                    padding: "7px 10px",
                    cursor: "pointer",
                    textAlign: "left",
                  }}
                  onMouseEnter={e => e.currentTarget.style.background = "#334155"}
                  onMouseLeave={e => e.currentTarget.style.background = "transparent"}
                >
                  <div style={{
                    width: 8, height: 8, borderRadius: "50%",
                    background: getColorForGenre(genre), flexShrink: 0,
                  }} />
                  <span style={{ color: "#94a3b8", fontSize: 12, fontFamily: "monospace", textTransform: "capitalize" }}>
                    {genre}
                  </span>
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Active genres */}
        <div style={{ display: "flex", flexDirection: "column", gap: 4, marginTop: 8 }}>
          {activeGenres.size === 0 && (
            <p style={{ color: "#334155", fontSize: 11, fontFamily: "monospace", margin: 0 }}>
              No genres selected — showing all
            </p>
          )}
          {Array.from(activeGenres).map(genre => {
            const color = getColorForGenre(genre);
            return (
              <div
                key={genre}
                style={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  background: `${color}22`,
                  border: `1px solid ${color}44`,
                  borderRadius: 6,
                  padding: "4px 8px",
                }}
              >
                <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                  <div style={{ width: 8, height: 8, borderRadius: "50%", background: color, flexShrink: 0 }} />
                  <span style={{ color: "#94a3b8", fontSize: 12, fontFamily: "monospace", textTransform: "capitalize" }}>
                    {genre}
                  </span>
                </div>
                <button
                  onClick={() => onRemoveGenre(genre)}
                  style={{
                    background: "none",
                    border: "none",
                    color: "#475569",
                    cursor: "pointer",
                    fontSize: 14,
                    padding: 0,
                    lineHeight: 1,
                  }}
                >
                  ✕
                </button>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}