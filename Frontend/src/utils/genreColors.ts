const FIXED_COLORS = [
  "#38bdf8", "#34d399", "#f472b6", "#a78bfa", "#818cf8",
  "#2dd4bf", "#f59e0b", "#fb923c", "#facc15", "#4ade80",
  "#f43f5e", "#e879f9", "#67e8f9", "#86efac", "#fda4af",
];

const genreColorCache: Record<string, string> = {};
let colorIndex = 0;

export function getGenreColor(genres: string[] | null | undefined): string {
  if (!genres || genres.length === 0) return "#64748b";
  for (const genre of genres) {
    const lower = genre.toLowerCase();
    if (!genreColorCache[lower]) {
      genreColorCache[lower] = FIXED_COLORS[colorIndex % FIXED_COLORS.length];
      colorIndex++;
    }
    return genreColorCache[lower];
  }
  return "#64748b";
}

export function getColorForGenre(genre: string): string {
  const lower = genre.toLowerCase();
  if (!genreColorCache[lower]) {
    genreColorCache[lower] = FIXED_COLORS[colorIndex % FIXED_COLORS.length];
    colorIndex++;
  }
  return genreColorCache[lower];
}

export function getAllCachedGenres(): Record<string, string> {
  return { ...genreColorCache };
}