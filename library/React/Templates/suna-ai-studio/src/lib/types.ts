export type PresetPalette = "sun" | "lilac" | "sage" | "night" | "rose" | "sand";

export type SoundQuality = "turbo" | "fidelity";

export interface SunaPreset {
  id: string;
  label: string;
  shortLabel: string;
  description: string;
  apiValue: string;
  palette: PresetPalette;
  /** The preset's default songbook, exactly as the Space ships it. */
  lyrics: string;
}

export interface SunaGenerateInput {
  prompt: string;
  presetId: string;
  lyrics: string;
  quality: SoundQuality;
  durationSec: number;
  vocalFile: File | null;
  vocalMixLevel: number;
}

export interface SunaTrackResult {
  audioUrl: string;
  wavUrl?: string;
  mimeType: string;
  fileName: string;
  wavName?: string;
  telemetry: string;
  /** The Space's word-aligned lyric sheet for what was actually sung. */
  lyrics?: string;
  requestedDuration: number;
}

export interface SunaStatusUpdate {
  stage: "connecting" | "submitting" | "working" | "queued" | "rendering";
  position?: number;
  eta?: number;
  message?: string;
}

export type SunaErrorCode =
  | "network"
  | "space"
  | "validation"
  | "timeout"
  | "cancelled"
  | "empty"
  | "download"
  | "unknown";

export interface Track {
  id: string;
  title: string;
  prompt: string;
  presetId: string;
  presetLabel: string;
  audioUrl: string;
  /** 48 kHz 16-bit WAV master link, when the Space returned one. */
  wavUrl?: string;
  wavName?: string;
  telemetry: string;
  lyrics?: string;
  mimeType: string;
  fileName: string;
  requestedDuration: number;
  /** Read from the returned audio file, never inferred. */
  duration?: number;
  quality: SoundQuality;
  vocalName?: string;
  createdAt: number;
}

export type GenerationStage =
  | "idle"
  | "connecting"
  | "submitting"
  | "working"
  | "queued"
  | "rendering"
  | "complete"
  | "error"
  | "cancelled";

export interface GenerationState {
  stage: GenerationStage;
  prompt?: string;
  presetId?: string;
  position?: number;
  startedAt?: number;
  error?: {
    code: SunaErrorCode;
    title: string;
    message: string;
    detail?: string;
  };
}

export type Availability = "checking" | "online" | "unknown" | "offline";
