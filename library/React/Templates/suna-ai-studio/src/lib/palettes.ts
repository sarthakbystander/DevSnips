import type { PresetPalette } from "./types";

export interface ArtPalette {
  from: string;
  to: string;
  deep: string;
  paper: string;
  label: string;
}

export const ART_PALETTES: Record<PresetPalette, ArtPalette> = {
  sun: {
    from: "#F8DCA0",
    to: "#E58A56",
    deep: "#8A3B22",
    paper: "#FFF4E2",
    label: "#3A2116",
  },
  lilac: {
    from: "#E3DBFA",
    to: "#9C86D8",
    deep: "#4E3C82",
    paper: "#FFFAF2",
    label: "#271F3D",
  },
  rose: {
    from: "#F7D7DE",
    to: "#D98BA5",
    deep: "#863C56",
    paper: "#FFF6F1",
    label: "#3D1F2A",
  },
  night: {
    from: "#3A3050",
    to: "#16121F",
    deep: "#0C0913",
    paper: "#E0B96C",
    label: "#F5F1FF",
  },
  sage: {
    from: "#DDEBE2",
    to: "#95B7A5",
    deep: "#4F6E5F",
    paper: "#FFF9EA",
    label: "#24312B",
  },
  sand: {
    from: "#F1DFC2",
    to: "#C9A06A",
    deep: "#79542F",
    paper: "#FFF4DE",
    label: "#382517",
  },
};

export function paletteGradient(palette: PresetPalette): string {
  const value = ART_PALETTES[palette];
  return `linear-gradient(135deg, ${value.from} 0%, ${value.to} 100%)`;
}
