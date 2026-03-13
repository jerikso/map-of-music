import { useEffect, useRef } from "react";
import { useSigma } from "@react-sigma/core";
import Graph from "graphology";
import type { Artist } from "../types";

interface Props {
  artists: Artist[];
  selectedArtist: Artist | null;
  onSelectArtist: (artist: Artist) => void;
}

export default function LoadGraph({ artists, selectedArtist, onSelectArtist }: Props) {
  const sigma = useSigma();
  const hoveredNode = useRef<string | null>(null);


  useEffect(() => {
    const graph = new Graph();

    artists.forEach((artist) => {
      graph.addNode(String(artist.id), {
        x: artist.x,
        y: -artist.y,
        size: 5,
        label: artist.name,
        color: "#38bdf8",
      });
    });

    sigma.setGraph(graph);

    sigma.setSetting("nodeReducer", (node: string, data: Record<string, unknown>) => {
      if (node === hoveredNode.current) {
        return { ...data, hoverColor: "#000000" };
      }
      return data;
    });

    sigma.setSetting("labelColor", { attribute: "hoverColor", color: "#ffffff" });

    sigma.on("enterNode", ({ node }) => {
      hoveredNode.current = node;
      sigma.refresh();
    });

    sigma.on("leaveNode", () => {
      hoveredNode.current = null;
      sigma.refresh();
    });

    sigma.on("clickNode", ({ node }) => {
    const artist = artists.find((a) => a.id === parseInt(node));
    if (artist) onSelectArtist(artist);

    const nodePosition = sigma.getNodeDisplayData(node);
    if (nodePosition) {
        sigma.getCamera().animate(
        { x: nodePosition.x, y: nodePosition.y, ratio: 0.2 },
        { duration: 500 }
        );
    }
    });
  }, [sigma, artists]);

  // second useEffect — pans to selected artist
  useEffect(() => {
    if (!selectedArtist) return;
    const nodePosition = sigma.getNodeDisplayData(String(selectedArtist.id));
    if (nodePosition) {
      sigma.getCamera().animate(
        { x: nodePosition.x, y: nodePosition.y, ratio: 0.2 },
        { duration: 500 }
      );
    }
  }, [selectedArtist]);

  return null;
}