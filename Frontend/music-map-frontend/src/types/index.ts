export interface Artist {
  id: number;
  name: string;
  x: number;
  y: number;
}

export interface Similarity {
  artist1Id: number;
  artist2Id: number;
  score: number;
}

export interface MapData {
  artists: Artist[];
  similarities: Similarity[];
}