import { useId } from "react";
import { ART_PALETTES } from "../lib/palettes";
import type { PresetPalette } from "../lib/types";

function hashSeed(seed: string): number {
  let hash = 2166136261;
  for (let index = 0; index < seed.length; index += 1) {
    hash ^= seed.charCodeAt(index);
    hash = Math.imul(hash, 16777619);
  }
  return Math.abs(hash);
}

interface TrackArtworkProps {
  seed: string;
  palette: PresetPalette;
  className?: string;
  showLabel?: boolean;
  playing?: boolean;
}

/**
 * Deterministic, original cover art. It is decorative, never a waveform or a
 * representation of the audio signal.
 */
export function TrackArtwork({
  seed,
  palette,
  className = "",
  showLabel = false,
  playing = false,
}: TrackArtworkProps) {
  const paletteValues = ART_PALETTES[palette];
  const hash = hashSeed(seed);
  const variant = hash % 6;
  const rotation = (hash % 60) - 30;
  const offset = (hash % 9) - 4;
  const gradientId = `art-${useId().replace(/:/g, "")}`;

  return (
    <span
      className={`relative block overflow-hidden isolate ${className}`}
      style={{ backgroundColor: paletteValues.from }}
      aria-hidden="true"
    >
      <svg
        viewBox="0 0 200 200"
        className="absolute inset-0 h-full w-full"
        preserveAspectRatio="xMidYMid slice"
      >
        <defs>
          <linearGradient id={gradientId} x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor={paletteValues.from} />
            <stop offset="100%" stopColor={paletteValues.to} />
          </linearGradient>
        </defs>
        <rect width="200" height="200" fill={`url(#${gradientId})`} />

        {variant === 0 && (
          <g transform={`rotate(${rotation} 100 100)`}>
            <circle cx={105 + offset} cy="94" r="58" fill={paletteValues.paper} />
            <circle
              cx={105 + offset}
              cy="94"
              r="72"
              fill="none"
              stroke={paletteValues.deep}
              strokeOpacity="0.42"
              strokeWidth="1"
            />
            <circle
              cx={105 + offset}
              cy="94"
              r="86"
              fill="none"
              stroke={paletteValues.deep}
              strokeOpacity="0.22"
              strokeWidth="1"
            />
            <path
              d="M-10 156c45-18 76-18 108 0s72 18 112-4"
              fill="none"
              stroke={paletteValues.paper}
              strokeOpacity="0.6"
              strokeWidth="1.5"
            />
            <circle cx="46" cy="46" r="4" fill={paletteValues.deep} opacity="0.6" />
          </g>
        )}

        {variant === 1 && (
          <g transform={`rotate(${rotation} 100 100)`}>
            <ellipse
              cx="100"
              cy="100"
              rx="78"
              ry="38"
              fill="none"
              stroke={paletteValues.paper}
              strokeOpacity="0.72"
              strokeWidth="2"
            />
            <ellipse
              cx="100"
              cy="100"
              rx="58"
              ry="80"
              fill="none"
              stroke={paletteValues.deep}
              strokeOpacity="0.4"
              strokeWidth="1.5"
            />
            <circle cx={100 + offset} cy="100" r="28" fill={paletteValues.paper} />
            <circle cx="100" cy="100" r="8" fill={paletteValues.deep} opacity="0.7" />
            <circle cx="22" cy="100" r="3" fill={paletteValues.paper} opacity="0.8" />
          </g>
        )}

        {variant === 2 && (
          <g>
            <path
              d={`M-20 ${132 + offset}c38-30 72-30 110 0s78 30 130-8v96H-20Z`}
              fill={paletteValues.deep}
              opacity="0.28"
            />
            <path
              d={`M-20 ${156 + offset}c42-26 76-26 112 0s74 24 128-6v70H-20Z`}
              fill={paletteValues.paper}
              opacity="0.82"
            />
            <path
              d={`M-20 ${178 + offset}c48-18 84-18 118 0s70 16 122-4v46H-20Z`}
              fill={paletteValues.deep}
              opacity="0.18"
            />
            <circle cx="148" cy="48" r="19" fill={paletteValues.paper} opacity="0.9" />
            <circle
              cx="148"
              cy="48"
              r="29"
              fill="none"
              stroke={paletteValues.deep}
              strokeOpacity="0.28"
            />
          </g>
        )}

        {variant === 3 && (
          <g transform={`rotate(${rotation} 100 100)`}>
            <circle cx="100" cy="100" r="64" fill={paletteValues.paper} opacity="0.3" />
            <circle
              cx={100 + offset}
              cy="100"
              r="40"
              fill={paletteValues.paper}
              opacity="0.9"
            />
            <circle cx="100" cy="100" r="14" fill={paletteValues.deep} opacity="0.88" />
            {[0, 60, 120, 180, 240, 300].map((angle) => (
              <rect
                key={angle}
                x="99"
                y="16"
                width="2"
                height="18"
                rx="1"
                fill={paletteValues.paper}
                opacity="0.75"
                transform={`rotate(${angle} 100 100)`}
              />
            ))}
          </g>
        )}

        {variant === 4 && (
          <g transform={`rotate(${rotation} 100 100)`}>
            <circle cx="100" cy="100" r="86" fill="none" stroke={paletteValues.paper} strokeOpacity="0.3" />
            <circle cx="100" cy="100" r="66" fill="none" stroke={paletteValues.paper} strokeOpacity="0.45" />
            <circle cx="100" cy="100" r="46" fill="none" stroke={paletteValues.paper} strokeOpacity="0.6" />
            <circle cx={100 + offset} cy="100" r="24" fill={paletteValues.paper} />
            <rect x="98" y="0" width="4" height="200" fill={paletteValues.deep} opacity="0.16" />
            <rect x="0" y="98" width="200" height="4" fill={paletteValues.deep} opacity="0.16" />
          </g>
        )}

        {variant === 5 && (
          <g>
            <path
              d={`M-10 ${70 + offset} 210 ${130 + offset}`}
              stroke={paletteValues.paper}
              strokeOpacity="0.42"
              strokeWidth="1.5"
            />
            <path
              d={`M-10 ${96 + offset} 210 ${156 + offset}`}
              stroke={paletteValues.paper}
              strokeOpacity="0.28"
              strokeWidth="1.5"
            />
            <circle cx={62 + offset} cy="104" r="40" fill={paletteValues.paper} />
            <circle cx={62 + offset} cy="104" r="54" fill="none" stroke={paletteValues.deep} strokeOpacity="0.3" />
            <circle cx="156" cy="58" r="10" fill={paletteValues.paper} opacity="0.85" />
            <circle cx="174" cy="80" r="4" fill={paletteValues.paper} opacity="0.7" />
          </g>
        )}
      </svg>

      <span className="paper-grain pointer-events-none absolute inset-0 block opacity-[0.16] mix-blend-overlay" />
      <span className="pointer-events-none absolute inset-0 block ring-1 ring-inset ring-black/5" />

      {showLabel && (
        <span className="absolute inset-x-3 bottom-3 flex items-end justify-between">
          <span
            className="font-mono text-[8px] uppercase tracking-[0.28em] opacity-70"
            style={{ color: paletteValues.label }}
          >
            Suna Studio
          </span>
          <span
            className="font-mono text-[8px] tracking-[0.18em] opacity-50"
            style={{ color: paletteValues.label }}
          >
            {String(variant + 1).padStart(2, "0")}
          </span>
        </span>
      )}

      {playing && (
        <span className="absolute right-3 top-3 flex h-5 items-end gap-[2px] rounded-full bg-black/25 px-2 py-1 backdrop-blur-sm">
          <span className="h-2 w-[2px] origin-bottom animate-equalize rounded-full bg-white/90" />
          <span className="h-2 w-[2px] origin-bottom animate-equalize rounded-full bg-white/90 [animation-delay:120ms]" />
          <span className="h-2 w-[2px] origin-bottom animate-equalize rounded-full bg-white/90 [animation-delay:240ms]" />
        </span>
      )}
    </span>
  );
}
