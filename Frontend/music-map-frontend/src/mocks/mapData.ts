import type { Artist, MapData, Similarity } from "../types";
import artists from "./artists.json";
import similarities from "./similarities.json";

export function parseMockData(): MapData {
  return {
    artists: artists as Artist[],
    similarities: similarities as Similarity[]
  };
}