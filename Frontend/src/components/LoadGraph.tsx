import { useEffect, useRef } from "react";
import { useSigma } from "@react-sigma/core";
import Graph from "graphology";
import type { Artist, Similarity } from "../types";
import { getGenreColor } from "../utils/genreColors";

interface Props {
  artists: Artist[];
  similarities: Similarity[];
  selectedArtist: Artist | null;
  onSelectArtist: (artist: Artist) => void;
}

export default function LoadGraph({ artists, similarities, selectedArtist, onSelectArtist }: Props) {
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

  // runs once — register events and settings
  useEffect(() => {
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
    });
  }, [sigma]);

  // rebuild graph when artists or similarities change
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

    similarities.forEach((sim) => {
      const source = String(sim.artist1Id);
      const target = String(sim.artist2Id);
      if (
        graph.hasNode(source) &&
        graph.hasNode(target) &&
        !graph.hasEdge(source, target)
      ) {
        graph.addEdge(source, target, {
          size: sim.score * 2,
          color: "#38bdf8",
          hidden: true,
        });
      }
    });

    sigma.setGraph(graph);

    // restore edges for selected artist
    const selectedId = selectedArtistRef.current
      ? String(selectedArtistRef.current.id)
      : null;

    if (selectedId) {
      graph.edges().forEach(edge => {
        const [source, target] = graph.extremities(edge);
        const isConnected = source === selectedId || target === selectedId;
        graph.setEdgeAttribute(edge, "hidden", !isConnected);
      });
    }
  }, [sigma, artists, similarities]);

  // update edges and node reducer when selected artist changes
  useEffect(() => {
    selectedArtistRef.current = selectedArtist;
    const graph = sigma.getGraph();
    const selectedId = selectedArtist ? String(selectedArtist.id) : null;

    graph.edges().forEach(edge => {
      const [source, target] = graph.extremities(edge);
      const isConnected = selectedId !== null && (source === selectedId || target === selectedId);
      graph.setEdgeAttribute(edge, "hidden", !isConnected);
    });

    sigma.setSetting("nodeReducer", (node: string, data: Record<string, unknown>) => {
      const isHovered = node === hoveredNode.current;
      const isSelected = node === String(selectedArtistRef.current?.id);
      if (isHovered || isSelected) {
        return { ...data, highlighted: true, hoverColor: "#000000" };
      }
      return data;
    });

    sigma.refresh();
  }, [selectedArtist]);

  // pan to selected artist
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