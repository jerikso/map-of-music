import { SigmaContainer } from "@react-sigma/core";
import "@react-sigma/core/lib/style.css";
import "@react-sigma/graph-search/lib/style.css";
import LoadGraph from "./LoadGraph";
import type { Artist } from "../types";
import ArtistSearch from "./ArtistSearch";

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
        labelFont: "Outfit",
        labelWeight: "600",
        labelColor: { attribute: "hoverColor", color: "#ffffff" },
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
      <div className="artist-search-wrapper" style={{
          position: "absolute",
          top: 24,
          right: 24,
          zIndex: 100,
        }}>
          <ArtistSearch artists={artists} onSelectArtist={onSelectArtist} />
        </div>
    </SigmaContainer>
  );
}