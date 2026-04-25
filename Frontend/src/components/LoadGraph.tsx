import { useEffect, useRef } from "react";
import { useSigma } from "@react-sigma/core";
import Graph from "graphology";
import type { Artist } from "../types";
import { getGenreColor } from "../utils/genreColors";

interface Props {
  artists: Artist[];
  selectedArtist: Artist | null;
  onSelectArtist: (artist: Artist) => void;
}

export default function LoadGraph({ artists, selectedArtist, onSelectArtist }: Props) {
  const sigma = useSigma();
  const hoveredNode = useRef<string | null>(null);
  const onSelectArtistRef = useRef(onSelectArtist);
  const artistsRef = useRef(artists);
  const selectedArtistRef = useRef<Artist | null>(null);

  // keep refs up to date without triggering effects
  useEffect(() => {
    onSelectArtistRef.current = onSelectArtist;
    artistsRef.current = artists;
  });

  useEffect(() => {
    selectedArtistRef.current = selectedArtist;
    sigma.refresh();
  }, [selectedArtist]);

  // runs once — register events and settings
  useEffect(() => {
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
      const artist = artistsRef.current.find((a) => a.id === parseInt(node));
      if (artist) onSelectArtistRef.current(artist);

      const nodePosition = sigma.getNodeDisplayData(node);
      if (nodePosition) {
        sigma.getCamera().animate(
          { x: nodePosition.x, y: nodePosition.y, ratio: 0.2 },
          { duration: 500 }
        );
      }
    });
  }, [sigma]);

  // runs when artists change — rebuild graph
  useEffect(() => {
    const graph = new Graph();

    artists.forEach((artist) => {
      const size = artist.listeners
        ? Math.pow(artist.listeners, 0.40) / 75
        : 3;

      graph.addNode(String(artist.id), {
        x: artist.x,
        y: -artist.y,
        size,
        label: artist.name,
        color: getGenreColor(artist.genres),
      });
    });

    sigma.setGraph(graph);
  }, [sigma, artists]);

  // runs when selected artist changes — pan to node
  useEffect(() => {
    if (!selectedArtist) return;
    const nodePosition = sigma.getNodeDisplayData(String(selectedArtist.id));
    if (nodePosition) {
      sigma.getCamera().animate(
        { x: nodePosition.x, y: nodePosition.y, ratio: 0.2 },
        { duration: 500 }
      );
    }
    sigma.setSetting("nodeReducer", (node: string, data: Record<string, unknown>) => {
      const isHovered = node === hoveredNode.current;
      const isSelected = node === String(selectedArtistRef.current?.id);

      if (isHovered || isSelected) {
        return {
          ...data,
          highlighted: true,
          hoverColor: "#000000",
        };
      }
      return data;
    });

  }, [selectedArtist]);

  return null;
}