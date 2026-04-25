import { SigmaContainer, ControlsContainer, ZoomControl } from "@react-sigma/core";
import { GraphSearch } from "@react-sigma/graph-search";
import "@react-sigma/core/lib/style.css";
import "@react-sigma/graph-search/lib/style.css";
import LoadGraph from "./LoadGraph";
import type { Artist } from "../types";

interface Props {
  artists: Artist[];
  selectedArtist: Artist | null;
  onSelectArtist: (artist: Artist) => void;
}

export default function MapCanvas({ artists, selectedArtist, onSelectArtist }: Props) {
  return (
    <SigmaContainer
      style={{ width: "100vw", height: "100vh", background: "#070b14" }}
      settings={{
        labelColor: { color: "#ffffff" },
        labelRenderedSizeThreshold: 6,
        renderEdgeLabels: false,
        stagePadding: 0,
      }}
    >
      <LoadGraph
        artists={artists}
        selectedArtist={selectedArtist}
        onSelectArtist={onSelectArtist}
      />
      <div style={{
          position: "absolute",
          top: 24,
          right: 24,
          zIndex: 100,
        }}>
          <GraphSearch
            type="nodes"
            onChange={(value) => {
              if (value?.type === "nodes") {
                const artist = artists.find((a) => a.id === parseInt(value.id));
                if (artist) onSelectArtist(artist);
              }
            }}
          />
        </div>  
    </SigmaContainer>
  );
}