import { Client } from "@gradio/client";
import type {
  SoundQuality,
  SunaErrorCode,
  SunaGenerateInput,
  SunaPreset,
  SunaStatusUpdate,
  SunaTrackResult,
} from "./types";

export const SUNA_SPACE_ID = "johanjomet/suna-ai-studio";
export const SUNA_SPACE_URL =
  "https://huggingface.co/spaces/johanjomet/suna-ai-studio";
export const SUNA_HOST = "https://johanjomet-suna-ai-studio.hf.space";
export const SUNA_INFO_URL = `${SUNA_HOST}/gradio_api/info`;
export const SUNA_API_NAME = "/generate_suna_track";
export const SUNA_PRESET_SELECT_API_NAME = "/on_preset_select";
export const SUNA_MODEL_LABEL = "Suna 48 kHz Master";

export const MIN_PROMPT_LENGTH = 3;
export const MAX_PROMPT_LENGTH = 500;
/** The Space's duration slider runs 24–68 s (step 4); the handler clips 20–68. */
export const MIN_DURATION = 24;
export const MAX_DURATION = 68;
export const DEFAULT_DURATION = 60;
export const DURATION_STEP = 4;
export const MAX_VOCAL_SECONDS = 68;
export const MAX_VOCAL_BYTES = 25 * 1024 * 1024;
export const MIN_VOCAL_MIX = 0.3;
export const MAX_VOCAL_MIX = 1.2;
export const DEFAULT_VOCAL_MIX = 0.88;
export const VOCAL_MIX_STEP = 0.05;
export const GENERATION_TIMEOUT_MS = 9 * 60 * 1000;

/**
 * These values are the exact enum members exposed by the deployed Space at
 * `/gradio_api/info` (2026-10). Do not paraphrase them when calling the API.
 */
export const SUNA_PRESETS: readonly SunaPreset[] = [
  {
    id: "indila-chanson",
    label: "Indila Chanson",
    shortLabel: "Chanson",
    description: "French chanson, weeping flute and violin, operatic lift.",
    apiValue: "🎻 Indila Style (French Chanson & Soaring Chorus)",
    palette: "rose",
    lyrics:
      "[Intro]\nOoh-ooh, aah-aah\nDans la nuit, I hear you calling\n\n[Verse 1]\nSoft rain falls on empty streets\nMy heart beats in quiet shadows\nEvery tear becomes a melody\nWaiting for the light to rise\n\n[Pre-Chorus]\nHold me close and take my hand\nLet the storm begin to play\n\n[Chorus]\nI dance with the wind and rain tonight, oh-oh-oh\nSoaring high above the pain, aah-aah\nJe danse, je vole into the sky\nOur love will never fade away, oh-oh\n\n[Outro]\nSoftly fades the last embrace\nOoh-ooh, aah",
  },
  {
    id: "matushka-folk",
    label: "Matushka Folk-Pop",
    shortLabel: "Folk-Pop",
    description: "Slavic folk-pop dance, balalaika, four-on-the-floor kick.",
    apiValue: "🌸 Matushka Style (Slavic Folk-Pop Dance)",
    palette: "sun",
    lyrics:
      "[Intro]\nAah-aah-aah, ooh-la-la\nGolden fields beneath the sky\n\n[Verse 1]\nMorning sun upon the river\nSilver birch trees in the breeze\nBarefoot dancing through the meadow\nSinging songs of wild and free\n\n[Pre-Chorus]\nSpinning faster round and round\nHear the joyful rhythm pound\n\n[Chorus]\nMatushka, oh mother earth, aah-aah-aah\nShining bright like morning dew, oh-oh\nSing with me across the land, la-la-la\nEvery heart is beating true, aah-aah\n\n[Outro]\nMatushka, oh shining land\nAah-aah-aah",
  },
  {
    id: "sia-power-ballad",
    label: "Power Ballad",
    shortLabel: "Ballad",
    description: "Sia-style power ballad, piano chords, stadium drums.",
    apiValue: "💎 Sia Style (Unstoppable Power Ballad)",
    palette: "lilac",
    lyrics:
      "[Intro]\nOoh-ooh, yeah-eah\nI put my armor on tonight\n\n[Verse 1]\nI hide my tears behind a smile\nI walk alone another mile\nNo one sees the weight I bear\nBreathing in the midnight air\n\n[Pre-Chorus]\nWatch me rise above the ground\nNothing gonna hold me down\n\n[Chorus]\nI am unstoppable tonight, oh-oh-oh\nFlying higher than the sky, yeah-eah\nI am invincible and bright, aah-aah\nWatch me shine into the light, oh-oh\n\n[Outro]\nShining through the darkest night\nOoh-ooh",
  },
  {
    id: "arena-rock",
    label: "Arena Rock",
    shortLabel: "Arena Rock",
    description: "Believer-style stadium rock, raspy anthem chorus.",
    apiValue: "🎸 Imagine Dragons Style (Believer Arena Rock)",
    palette: "night",
    lyrics:
      "[Intro]\nOh-oh-oh, yeah-eah\nFeel the thunder in the dark\n\n[Verse 1]\nFirst things first, I hear the sound\nFeet are planted on the ground\nEvery scar became a flame\nCalling out my only name\n\n[Pre-Chorus]\nFeel the lightning in my veins\nBreaking every single chain\n\n[Chorus]\nYou made me a believer, oh-oh-oh\nWalking through the blazing fire, yeah-eah\nRising higher than the storm, aah-aah\nWe are giants born tonight, oh-oh\n\n[Outro]\nRising through the blazing fire\nOh-oh",
  },
  {
    id: "afro-latin",
    label: "Afro-Latin Pop",
    shortLabel: "Afro-Latin",
    description: "Dembow percussion, nylon guitar, warm log-drum sub-bass.",
    apiValue: "💃 Shakira & Burna Boy Style (Afro-Latin Dembow)",
    palette: "sand",
    lyrics:
      "[Intro]\nOya-oya, baila-la\nFeel the rhythm in your soul\n\n[Verse 1]\nGolden moon above the sea\nMove your body close to me\nEvery drum begins to play\nChase the lonely night away\n\n[Pre-Chorus]\nSubelo, turn up the heat\nEverybody on their feet\n\n[Chorus]\nDai-dai-dai, baila conmigo, oh-oh-oh\nShining underneath the stars, aah-aah\nDai-dai-dai, feel the fuego, yeah-eah\nMusic takes us where we are, oh-oh\n\n[Outro]\nBaila conmigo in the light\nOya-oya",
  },
  {
    id: "slap-house",
    label: "Slap House",
    shortLabel: "Slap House",
    description: "Headlights-style slap house, melancholic piano, metallic bass.",
    apiValue: "🎧 Alok Style (Headlights Slap House)",
    palette: "sage",
    lyrics:
      "[Intro]\nOoh-ooh, aah-aah\nShining headlights in the rain\n\n[Verse 1]\nDriving through the neon glow\nWhere the midnight rivers flow\nEvery memory of you\nPaints the sky in electric blue\n\n[Pre-Chorus]\nHold me til the morning comes\nHear the beating of the drums\n\n[Chorus]\nFollow the headlights home tonight, oh-oh-oh\nDancing through the silver rain, aah-aah\nNever let the music fade, yeah-eah\nTake away the lonely pain, oh-oh\n\n[Outro]\nFollow the headlights home\nOoh-ooh",
  },
];

/**
 * Exact members of the Space's "Synthesis Engine" radio. Turbo is the default.
 */
export const SUNA_QUALITY_MODES: readonly {
  id: SoundQuality;
  label: string;
  shortLabel: string;
  description: string;
  apiValue: string;
}[] = [
  {
    id: "turbo",
    label: "Turbo",
    shortLabel: "Turbo",
    description: "8 denoising steps · fastest render.",
    apiValue: "⚡ Turbo (8 Steps · ~15s on A100)",
  },
  {
    id: "fidelity",
    label: "High-Fidelity",
    shortLabel: "Fidelity",
    description: "16 denoising steps · the Space's flagship engine.",
    apiValue: "💎 High-Fidelity SFT (16 Steps · ~28s on A100)",
  },
];

export function getPreset(id: string): SunaPreset {
  return SUNA_PRESETS.find((preset) => preset.id === id) ?? SUNA_PRESETS[0];
}

export function getQualityMode(id: SoundQuality) {
  return (
    SUNA_QUALITY_MODES.find((mode) => mode.id === id) ?? SUNA_QUALITY_MODES[0]
  );
}

export class SunaError extends Error {
  readonly code: SunaErrorCode;
  readonly detail?: string;

  constructor(code: SunaErrorCode, message: string, detail?: string) {
    super(message);
    this.name = "SunaError";
    this.code = code;
    this.detail = detail;
  }
}

let clientPromise: Promise<Client> | null = null;

/** Minimal shape of the Gradio queue events this adapter consumes. */
interface GradioStreamEvent {
  type?: string;
  stage?: string;
  message?: string;
  position?: number;
  eta?: number;
  data?: unknown;
}

type SunaStreamJob = ReturnType<Client["submit"]>;
type SunaStreamStep = Awaited<ReturnType<SunaStreamJob["next"]>>;

function getClient(): Promise<Client> {
  if (!clientPromise) {
    clientPromise = Client.connect(SUNA_SPACE_ID).catch((error: unknown) => {
      clientPromise = null;
      throw error;
    });
  }
  return clientPromise;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}

function toAbsoluteUrl(url: string): string {
  if (/^https?:\/\//i.test(url)) return url;
  return `${SUNA_HOST}${url.startsWith("/") ? "" : "/"}${url}`;
}

function abortReason(signals: {
  external: AbortSignal | undefined;
  timeout: AbortSignal;
}): SunaError {
  if (signals.timeout.aborted) {
    return new SunaError(
      "timeout",
      "Suna took too long to finish this track. The Space may be busy — try again in a moment.",
    );
  }
  return new SunaError("cancelled", "Generation cancelled.");
}

function mergeSignals(
  external: AbortSignal | undefined,
  timeoutSignal: AbortSignal,
): AbortSignal {
  if (!external) return timeoutSignal;

  const controller = new AbortController();
  const abort = () => controller.abort();

  if (external.aborted || timeoutSignal.aborted) {
    controller.abort();
    return controller.signal;
  }

  external.addEventListener("abort", abort, { once: true });
  timeoutSignal.addEventListener("abort", abort, { once: true });
  controller.signal.addEventListener(
    "abort",
    () => {
      external.removeEventListener("abort", abort);
      timeoutSignal.removeEventListener("abort", abort);
    },
    { once: true },
  );

  return controller.signal;
}

function normalizeError(
  error: unknown,
  signals: { external: AbortSignal | undefined; timeout: AbortSignal },
): SunaError {
  if (error instanceof SunaError) return error;
  if (signals.timeout.aborted || signals.external?.aborted) {
    return abortReason(signals);
  }

  const raw = error instanceof Error ? error.message : String(error);
  const message = raw.toLowerCase();

  if (
    message.includes("could not resolve app config") ||
    message.includes("space status") ||
    message.includes("no api information") ||
    message.includes("not authorized")
  ) {
    return new SunaError(
      "space",
      "Suna's Space isn't available right now. It may be waking up or at capacity. Try again in a moment.",
      raw,
    );
  }

  if (
    message.includes("failed to fetch") ||
    message.includes("networkerror") ||
    message.includes("network error") ||
    message.includes("load failed") ||
    message.includes("connection")
  ) {
    return new SunaError(
      "network",
      "We couldn't reach Suna's Space. Check your connection and try again.",
      raw,
    );
  }

  if (
    message.includes("validation") ||
    message.includes("422") ||
    message.includes("invalid")
  ) {
    return new SunaError(
      "validation",
      "Suna couldn't use those settings. Adjust the prompt, style, or length and try again.",
      raw,
    );
  }

  return new SunaError(
    "unknown",
    "The track didn't finish rendering. This is usually temporary — try again.",
    raw,
  );
}

export interface GenerateOptions {
  signal?: AbortSignal;
  onStatus?: (status: SunaStatusUpdate) => void;
}

/**
 * Calls the deployed Suna Space through its documented Gradio API.
 *
 * Verified contract (2026-10, `/gradio_api/info` + the Space's source):
 *   POST /gradio_api/call/v2/generate_suna_track
 *   params: user_prompt, artist_preset, custom_lyrics, duration_sec,
 *           speed_mode, uploaded_vocal, vocal_mix
 *   returns: [mp3 FileData, wav FileData, telemetry string, lyrics string]
 *   On render error: [null, null, "⚠️ Generation error: …", lyrics]
 */
export async function generateSunaTrack(
  input: SunaGenerateInput,
  options: GenerateOptions = {},
): Promise<SunaTrackResult> {
  const timeoutController = new AbortController();
  const timeout = window.setTimeout(
    () => timeoutController.abort(),
    GENERATION_TIMEOUT_MS,
  );
  const signals = {
    external: options.signal,
    timeout: timeoutController.signal,
  };
  const signal = mergeSignals(options.signal, timeoutController.signal);
  let resetClient = false;

  try {
    options.onStatus?.({ stage: "connecting" });
    const client = await getClient();

    if (signal.aborted) throw abortReason(signals);

    options.onStatus?.({ stage: "submitting" });

    const preset = getPreset(input.presetId);
    const quality = getQualityMode(input.quality);
    const lyrics = input.lyrics.trim();
    const job = client.submit(SUNA_API_NAME, {
      user_prompt: input.prompt.trim(),
      artist_preset: preset.apiValue,
      custom_lyrics: lyrics,
      duration_sec: input.durationSec,
      speed_mode: quality.apiValue,
      uploaded_vocal: input.vocalFile ?? null,
      vocal_mix: input.vocalMixLevel,
    });

    const cancelJob = () => {
      void job.cancel();
    };
    signal.addEventListener("abort", cancelJob, { once: true });

    let payload: unknown;
    let wavPayload: unknown;
    let telemetry = "";
    let sungLyrics = "";
    let sawData = false;
    let sawAnyEvent = false;

    /**
     * Pull the next queue event without hanging forever on an idle stream.
     *
     * Observed 2026-10: when the Space's anonymous ZeroGPU quota is spent (or
     * the queue drops the request), the SSE stream closes the job without ever
     * yielding an event. A plain `for await` would sit on a promise that never
     * settles, so cancellation UI would freeze — race every `next()` against
     * the abort signal instead.
     */
    const nextEvent = (): Promise<SunaStreamStep> => {
      const pending = job.next();
      // A cancel can settle the loser-of-the-race promise as a rejection
      // later on; swallow it so nothing surfaces as an unhandled rejection.
      void pending.catch(() => {});
      const interruption = new Promise<never>((_, reject) => {
        const onAbort = () => reject(abortReason(signals));
        if (signal.aborted) {
          onAbort();
          return;
        }
        signal.addEventListener("abort", onAbort, { once: true });
        void pending.then(
          () => signal.removeEventListener("abort", onAbort),
          () => signal.removeEventListener("abort", onAbort),
        );
      });
      return Promise.race([pending, interruption]);
    };

    try {
      options.onStatus?.({ stage: "working" });

      for (;;) {
        const step = await nextEvent();
        if (step.done) break;
        sawAnyEvent = true;
        const event = step.value as GradioStreamEvent;

        if (signal.aborted) throw abortReason(signals);

        if (event.type === "status") {
          if (event.stage === "pending") {
            options.onStatus?.({
              stage: "queued",
              position:
                typeof event.position === "number" ? event.position : undefined,
              eta: typeof event.eta === "number" ? event.eta : undefined,
            });
          } else if (event.stage === "generating" || event.stage === "streaming") {
            options.onStatus?.({ stage: "rendering" });
          } else if (event.stage === "error") {
            const message =
              typeof event.message === "string" && event.message.trim()
                ? event.message
                : "Suna reported an error.";
            throw new SunaError("space", message);
          }
        } else if (event.type === "data") {
          sawData = true;
          const data = event.data;
          if (Array.isArray(data)) {
            payload = data[0] ?? null;
            wavPayload = data[1] ?? null;
            if (typeof data[2] === "string") telemetry = data[2];
            if (typeof data[3] === "string") sungLyrics = data[3];
          }
        }
      }
    } finally {
      signal.removeEventListener("abort", cancelJob);
      // Close the stream politely whenever we leave the loop for any reason.
      // Fire-and-forget: never let cleanup delay an in-flight cancellation.
      void job
        .return()
        .catch(() => {
          /* the stream may already be gone (cancel, quota) — that is fine */
        });
    }

    if (signal.aborted) throw abortReason(signals);

    /**
     * Observed 2026-10: when the public Space's anonymous ZeroGPU quota is
     * spent (or the queue drops the request), the job stream closes with no
     * events at all. Say so honestly instead of blaming the prompt.
     */
    if (!sawAnyEvent) {
      throw new SunaError(
        "space",
        "Suna's Space closed the request without starting a render. Its free anonymous GPU quota is likely spent for your connection right now, or the queue backed off — wait a bit and try again.",
      );
    }

    // The Space returns [null, null, "⚠️ Generation error: …", lyrics] when
    // its handler threw. Prefer the Space's own error text.
    if (!isRecord(payload) || typeof payload.url !== "string") {
      if (telemetry.trim().startsWith("⚠️")) {
        throw new SunaError("space", telemetry.trim());
      }
      throw new SunaError(
        "empty",
        sawData
          ? "Suna finished without returning an audio file. Try a different prompt."
          : "Suna's queue closed before returning audio. The public Space may be at capacity — try again shortly.",
      );
    }

    const fileName =
      typeof payload.orig_name === "string" && payload.orig_name
        ? payload.orig_name
        : "suna-track.mp3";
    const mimeType =
      typeof payload.mime_type === "string" && payload.mime_type
        ? payload.mime_type
        : "audio/mpeg";

    return {
      audioUrl: toAbsoluteUrl(payload.url),
      wavUrl:
        isRecord(wavPayload) && typeof wavPayload.url === "string"
          ? toAbsoluteUrl(wavPayload.url)
          : undefined,
      wavName:
        isRecord(wavPayload) && typeof wavPayload.orig_name === "string"
          ? wavPayload.orig_name
          : undefined,
      telemetry,
      lyrics: sungLyrics || undefined,
      mimeType,
      fileName,
      requestedDuration: input.durationSec,
    };
  } catch (error) {
    const normalized = normalizeError(error, signals);
    if (normalized.code === "network" || normalized.code === "space") {
      resetClient = true;
    }
    throw normalized;
  } finally {
    window.clearTimeout(timeout);
    if (resetClient) clientPromise = null;
  }
}

/** Reads the real duration from the returned audio file. */
export function readAudioDuration(url: string): Promise<number | undefined> {
  return new Promise((resolve) => {
    const audio = new Audio();
    audio.preload = "metadata";

    const finish = (value?: number) => {
      audio.removeAttribute("src");
      audio.load();
      resolve(value);
    };

    audio.addEventListener(
      "loadedmetadata",
      () => {
        finish(
          Number.isFinite(audio.duration) && audio.duration > 0
            ? audio.duration
            : undefined,
        );
      },
      { once: true },
    );
    audio.addEventListener("error", () => finish(undefined), { once: true });
    audio.src = url;
  });
}

/** A lightweight, honest availability probe for the public endpoint. */
export async function checkSunaAvailability(
  signal?: AbortSignal,
): Promise<"online" | "offline" | "unknown"> {
  try {
    const response = await fetch(SUNA_INFO_URL, {
      signal,
      cache: "no-store",
    });
    if (!response.ok) return "offline";
    const info: unknown = await response.json();
    if (
      isRecord(info) &&
      isRecord(info.named_endpoints) &&
      SUNA_API_NAME in info.named_endpoints
    ) {
      return "online";
    }
    return "unknown";
  } catch {
    return typeof navigator !== "undefined" && navigator.onLine === false
      ? "offline"
      : "unknown";
  }
}

function slugify(value: string): string {
  return (
    value
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-+|-+$/g, "")
      .slice(0, 60) || "suna-track"
  );
}

/** Fetches the generated MP3 and saves it locally. */
export async function downloadTrackAudio(
  url: string,
  title: string,
  fileName?: string,
): Promise<void> {
  let response: Response;
  try {
    response = await fetch(url);
  } catch (error) {
    throw new SunaError(
      "download",
      "The download was blocked. Open the track in a new tab instead.",
      error instanceof Error ? error.message : undefined,
    );
  }

  if (!response.ok) {
    throw new SunaError(
      "download",
      "The track file is no longer available. Regenerate it to download again.",
      `HTTP ${response.status}`,
    );
  }

  const blob = await response.blob();
  const extension = fileName?.split(".").pop()?.toLowerCase() ?? "mp3";
  const objectUrl = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = objectUrl;
  link.download = `${slugify(title)}.${extension}`;
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.setTimeout(() => URL.revokeObjectURL(objectUrl), 10_000);
}
