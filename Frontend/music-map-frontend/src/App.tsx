import { useState } from "react";
import MapCanvas from "./components/MapCanvas";
import { parseMockData } from "./mocks/mapData";
import type { Artist } from "./types";

const { artists } = parseMockData();

export default function App() {
  const [selected, setSelected] = useState<Artist | null>(null);

  return (
    <div style={{ width: "100vw", height: "100vh" }}>
      <MapCanvas
        artists={artists}
        selectedArtist={selected}
        onSelectArtist={setSelected}
      />
      {selected && (
        <div style={{
          position: "fixed", bottom: 24, left: 24,
          background: "#1e293b", color: "white",
          padding: "12px 20px", borderRadius: 8,
        }}>
          {selected.name}
        </div>
      )}
    </div>
  );
}