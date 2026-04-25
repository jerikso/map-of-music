import { GENRE_COLORS } from "../utils/genreColors";

export default function Legend() {
  return (
    <div style={{
      position: "fixed",
      bottom: 24,
      right: 24,
      background: "#0f172a",
      border: "1px solid #1e293b",
      borderRadius: 12,
      padding: "12px 16px",
      zIndex: 100,
    }}>
      <p style={{
        color: "#475569",
        fontSize: 11,
        fontFamily: "monospace",
        textTransform: "uppercase",
        letterSpacing: "0.1em",
        margin: "0 0 10px",
      }}>
        Genres
      </p>
      <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
        {Object.entries(GENRE_COLORS).map(([genre, color]) => (
          <div key={genre} style={{ display: "flex", alignItems: "center", gap: 8 }}>
            <div style={{
              width: 10,
              height: 10,
              borderRadius: "50%",
              background: color,
              flexShrink: 0,
            }} />
            <span style={{
              color: "#94a3b8",
              fontSize: 12,
              fontFamily: "monospace",
              textTransform: "capitalize",
            }}>
              {genre}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}