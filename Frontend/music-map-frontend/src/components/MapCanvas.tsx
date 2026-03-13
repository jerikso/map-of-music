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
  const hoveredNode = useRef<string | null>(null);

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

    // Sigma settings
    const sigmaSettings = {
      renderEdgeLabels: false,
      stagePadding: 0,
      labelColor: { attribute: "hoverColor", color: "#fff" },
      labelRenderedSizeThreshold: 0,
      nodeReducer: (node, data) => {
        if (node === hoveredNode.current) {
              return {
                ...data,
                hoverColor: "#000000",
              };
        }
        return data;
      },
    };

    const sigma = new Sigma(graph, containerRef.current, sigmaSettings);

    sigma.on("clickNode", ({ node }) => {
      const artist = artists.find((a) => a.id === parseInt(node));
      if (artist) onSelectArtist(artist);
    });

    sigma.on("enterNode", ({ node }) => {
      hoveredNode.current = node;
      sigma.refresh();
    });

    sigma.on("leaveNode", () => {
      hoveredNode.current = null;
      sigma.refresh();
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