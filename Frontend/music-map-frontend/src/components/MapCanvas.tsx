import { useEffect, useRef } from "react";
import Graph from "graphology";
import Sigma from "sigma";
import type { Artist } from "../types";

interface Props {
  artists: Artist[];
  onSelectArtist: (artist: Artist) => void;
}

export default function MapCanvas({ artists, onSelectArtist }: Props) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    const graph = new Graph();

    artists.forEach((artist) => {
      graph.addNode(String(artist.id), {
        x: artist.x,
        y: artist.y,
        size: 5,
        label: artist.name,
        color: "#38bdf8",
      });
    });

    const sigma = new Sigma(graph, containerRef.current, {
        renderEdgeLabels: false,
        stagePadding: 0,
        labelColor: { color: "#ffffff" },
        labelRenderedSizeThreshold: 3,
    });

    sigma.on("clickNode", ({ node }) => {
      const artist = artists.find((a) => a.id === parseInt(node));
      if (artist) onSelectArtist(artist);
    });

    return () => sigma.kill();
  }, [artists]);

  return (
  <div
    ref={containerRef}
    style={{
      width: "100vw",
      height: "100vh",
      background: "#070b14",
      position: "fixed",
      top: 0,
      left: 0,
    }}
  />
);
}