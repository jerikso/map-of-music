import { parseMockData } from "../mocks/mapData"

export function useMapData() {
  return { data: parseMockData(), loading: false, error: null }
}