export const GENRE_COLORS: Record<string, string> = {
  "alternative rock": "#38bdf8",
  "indie":            "#34d399",
  "pop":              "#f472b6",
  "hip-hop":          "#a78bfa",
  "rap":              "#818cf8",
  "electronic":       "#2dd4bf",
  "metal":            "#f59e0b",
  "rock":             "#fb923c",
  "classical":        "#facc15",
  "jazz":             "#4ade80",
  "folk":             "#a3e635",
};

const DEFAULT_COLOR = "#64748b";

export function getGenreColor(genres: string[] | null | undefined): string {
  if (!genres || genres.length === 0) return DEFAULT_COLOR;

  for (const genre of genres) {
    const lower = genre.toLowerCase();
    for (const [key, color] of Object.entries(GENRE_COLORS)) {
      if (lower.includes(key)) return color;
    }
  }
  return DEFAULT_COLOR;
}