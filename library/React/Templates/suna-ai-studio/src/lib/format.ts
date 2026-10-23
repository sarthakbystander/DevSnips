export function formatTime(seconds: number | undefined): string {
  if (seconds === undefined || !Number.isFinite(seconds) || seconds < 0) {
    return "0:00";
  }
  const whole = Math.floor(seconds);
  const minutes = Math.floor(whole / 60);
  const rest = whole % 60;
  return `${minutes}:${rest.toString().padStart(2, "0")}`;
}

export function formatDurationLabel(seconds: number | undefined): string {
  if (seconds === undefined || !Number.isFinite(seconds) || seconds <= 0) {
    return "—";
  }
  const rounded = Math.round(seconds);
  return `${rounded}s`;
}

export function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${Math.round(bytes / 1024)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export function clamp(value: number, min: number, max: number): number {
  return Math.min(max, Math.max(min, value));
}

/** A human title from the first clause of a prompt. */
export function titleFromPrompt(prompt: string): string {
  const firstClause =
    prompt
      .trim()
      .split(/[,.;\n]/)
      .map((part) => part.trim())
      .find(Boolean) ?? "";
  const cleaned = firstClause.replace(/\s+/g, " ").trim();
  if (!cleaned) return "Untitled sketch";

  const capitalised = cleaned.charAt(0).toUpperCase() + cleaned.slice(1);
  return capitalised.length > 54
    ? `${capitalised.slice(0, 51).trimEnd()}…`
    : capitalised;
}

export function makeId(): string {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) {
    return crypto.randomUUID();
  }
  return `track-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
}

export function pluralise(
  count: number,
  singular: string,
  plural = `${singular}s`,
): string {
  return `${count} ${count === 1 ? singular : plural}`;
}
