import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
  type ReactNode,
} from "react";
import {
  checkSunaAvailability,
  downloadTrackAudio,
  generateSunaTrack,
  getPreset,
  readAudioDuration,
  SunaError,
} from "../lib/suna";
import { clamp, makeId, titleFromPrompt } from "../lib/format";
import type {
  Availability,
  GenerationState,
  SunaGenerateInput,
  Track,
} from "../lib/types";

type Tone = "info" | "success" | "error";

interface Notice {
  id: number;
  message: string;
  tone: Tone;
}

interface StudioContextValue {
  tracks: Track[];
  currentTrack: Track | null;
  isPlaying: boolean;
  currentTime: number;
  duration: number;
  volume: number;
  muted: boolean;
  generation: GenerationState;
  isGenerating: boolean;
  availability: Availability;
  notice: Notice | null;
  downloadingId: string | null;
  playTrack: (track: Track) => void;
  togglePlay: () => void;
  selectTrack: (track: Track) => void;
  seek: (time: number) => void;
  setVolume: (volume: number) => void;
  toggleMute: () => void;
  playNext: () => void;
  playPrevious: () => void;
  removeTrack: (id: string) => void;
  clearTracks: () => void;
  renameTrack: (id: string, title: string) => void;
  generate: (input: SunaGenerateInput) => void;
  cancelGeneration: () => void;
  retryGeneration: () => void;
  dismissGeneration: () => void;
  downloadTrack: (track: Track) => void;
  notify: (message: string, tone?: Tone) => void;
  dismissNotice: () => void;
}

const StudioContext = createContext<StudioContextValue | null>(null);

const VOLUME_STORAGE_KEY = "suna-studio:volume";

function readStoredVolume(): number {
  try {
    const raw = window.localStorage.getItem(VOLUME_STORAGE_KEY);
    const parsed = raw === null ? Number.NaN : Number(raw);
    return Number.isFinite(parsed) ? clamp(parsed, 0, 1) : 0.8;
  } catch {
    return 0.8;
  }
}

function isAbortError(error: unknown): boolean {
  return (
    error instanceof SunaError && error.code === "cancelled"
  );
}

function generationErrorState(error: unknown): GenerationState["error"] {
  if (error instanceof SunaError) {
    const titles: Record<string, string> = {
      network: "Connection lost",
      space: "Suna is unavailable",
      validation: "Settings need a tweak",
      timeout: "This is taking longer than usual",
      empty: "No audio came back",
      download: "Download unavailable",
      unknown: "That didn't render",
      cancelled: "Generation cancelled",
    };
    return {
      code: error.code,
      title: titles[error.code] ?? "That didn't render",
      message: error.message,
      detail: error.detail,
    };
  }

  return {
    code: "unknown",
    title: "That didn't render",
    message: "Something unexpected happened. Try again in a moment.",
    detail: error instanceof Error ? error.message : String(error),
  };
}

const ACTIVE_STAGES = new Set([
  "connecting",
  "submitting",
  "working",
  "queued",
  "rendering",
]);

export function StudioProvider({ children }: { children: ReactNode }) {
  const [tracks, setTracks] = useState<Track[]>([]);
  const [currentId, setCurrentId] = useState<string | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [volume, setVolumeState] = useState(readStoredVolume);
  const [muted, setMuted] = useState(false);
  const [generation, setGeneration] = useState<GenerationState>({
    stage: "idle",
  });
  const [availability, setAvailability] = useState<Availability>("checking");
  const [notice, setNotice] = useState<Notice | null>(null);
  const [downloadingId, setDownloadingId] = useState<string | null>(null);

  const audioRef = useRef<HTMLAudioElement>(null);
  const currentIdRef = useRef<string | null>(null);
  const loadedUrlRef = useRef<string | null>(null);
  const abortRef = useRef<AbortController | null>(null);
  const lastRequestRef = useRef<SunaGenerateInput | null>(null);
  const noticeTimerRef = useRef<number | null>(null);
  const tracksRef = useRef<Track[]>(tracks);

  useEffect(() => {
    tracksRef.current = tracks;
  }, [tracks]);

  const currentTrack = useMemo(
    () => tracks.find((track) => track.id === currentId) ?? null,
    [tracks, currentId],
  );

  const notify = useCallback((message: string, tone: Tone = "info") => {
    if (noticeTimerRef.current !== null) {
      window.clearTimeout(noticeTimerRef.current);
    }
    const next = { id: Date.now(), message, tone };
    setNotice(next);
    noticeTimerRef.current = window.setTimeout(() => {
      setNotice((current) => (current?.id === next.id ? null : current));
    }, 5200);
  }, []);

  const dismissNotice = useCallback(() => {
    if (noticeTimerRef.current !== null) {
      window.clearTimeout(noticeTimerRef.current);
      noticeTimerRef.current = null;
    }
    setNotice(null);
  }, []);

  useEffect(() => {
    return () => {
      if (noticeTimerRef.current !== null) {
        window.clearTimeout(noticeTimerRef.current);
      }
    };
  }, []);

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;
    audio.volume = volume;
    audio.muted = muted;
    try {
      window.localStorage.setItem(VOLUME_STORAGE_KEY, String(volume));
    } catch {
      // Storage is a convenience, not a requirement.
    }
  }, [volume, muted]);

  const forgetAudio = useCallback(() => {
    loadedUrlRef.current = null;
    const audio = audioRef.current;
    if (!audio) return;
    audio.pause();
    audio.removeAttribute("src");
    audio.load();
  }, []);

  const loadAudio = useCallback((url: string) => {
    const audio = audioRef.current;
    if (!audio) return;
    if (loadedUrlRef.current === url) return;
    loadedUrlRef.current = url;
    audio.src = url;
    audio.load();
  }, []);

  useEffect(() => {
    if (!currentTrack) {
      currentIdRef.current = null;
      forgetAudio();
      setCurrentTime(0);
      setDuration(0);
      setIsPlaying(false);
      return;
    }

    if (currentIdRef.current === currentTrack.id) {
      // The src may still be missing (e.g. the request resolved before the
      // effect ran), so make sure it is loaded either way.
      loadAudio(currentTrack.audioUrl);
      return;
    }

    currentIdRef.current = currentTrack.id;
    loadAudio(currentTrack.audioUrl);
    setCurrentTime(0);
    setDuration(currentTrack.duration ?? 0);
    setIsPlaying(false);
  }, [currentTrack, forgetAudio, loadAudio]);

  useEffect(() => {
    const controller = new AbortController();
    let active = true;
    const timer = window.setTimeout(() => controller.abort(), 9000);
    void checkSunaAvailability(controller.signal).then((result) => {
      // StrictMode runs this effect twice. Ignore the aborted first probe so it
      // cannot overwrite the live result with "unknown".
      if (active) setAvailability(result);
    });
    return () => {
      active = false;
      window.clearTimeout(timer);
      controller.abort();
    };
  }, []);

  const selectTrack = useCallback((track: Track) => {
    setCurrentId(track.id);
    setCurrentTime(0);
    setDuration(track.duration ?? 0);
  }, []);

  const playTrack = useCallback(
    (track: Track) => {
      const audio = audioRef.current;
      if (!audio) return;

      if (currentIdRef.current !== track.id) {
        currentIdRef.current = track.id;
        setCurrentId(track.id);
        setCurrentTime(0);
        setDuration(track.duration ?? 0);
      }
      loadAudio(track.audioUrl);

      void audio
        .play()
        .then(() => setIsPlaying(true))
        .catch(() => {
          setIsPlaying(false);
          notify(
            "Your browser blocked playback. Press play once more to start.",
            "error",
          );
        });
    },
    [notify],
  );

  const togglePlay = useCallback(() => {
    const audio = audioRef.current;
    if (!audio) return;

    if (!currentIdRef.current) {
      const first = tracksRef.current[0];
      if (first) playTrack(first);
      return;
    }

    if (audio.paused) {
      void audio
        .play()
        .then(() => setIsPlaying(true))
        .catch(() => {
          setIsPlaying(false);
          notify("Playback couldn't start. Try again.", "error");
        });
    } else {
      audio.pause();
    }
  }, [notify, playTrack]);

  const seek = useCallback((time: number) => {
    const audio = audioRef.current;
    if (!audio) return;
    const max = Number.isFinite(audio.duration) ? audio.duration : duration;
    const next = clamp(time, 0, max || 0);
    audio.currentTime = next;
    setCurrentTime(next);
  }, [duration]);

  const setVolume = useCallback((next: number) => {
    const value = clamp(next, 0, 1);
    setVolumeState(value);
    if (value > 0) setMuted(false);
  }, []);

  const toggleMute = useCallback(() => {
    setMuted((current) => !current);
  }, []);

  const playNext = useCallback(() => {
    const list = tracksRef.current;
    if (!currentIdRef.current || list.length < 2) return;
    const index = list.findIndex((track) => track.id === currentIdRef.current);
    if (index < 0) return;
    const next = list[index + 1];
    if (next) playTrack(next);
  }, [playTrack]);

  const playPrevious = useCallback(() => {
    const list = tracksRef.current;
    if (!currentIdRef.current || list.length < 2) return;
    const index = list.findIndex((track) => track.id === currentIdRef.current);
    if (index < 0) return;

    const audio = audioRef.current;
    if (audio && audio.currentTime > 3) {
      seek(0);
      return;
    }

    const previous = list[index - 1];
    if (previous) playTrack(previous);
  }, [playTrack, seek]);

  const removeTrack = useCallback(
    (id: string) => {
      const previous = tracksRef.current;
      const next = previous.filter((track) => track.id !== id);

      if (currentIdRef.current === id) {
        forgetAudio();
        currentIdRef.current = null;
        setCurrentId(next[0]?.id ?? null);
        setCurrentTime(0);
        setDuration(next[0]?.duration ?? 0);
        setIsPlaying(false);
      }

      setTracks(next);
      notify("Removed from this session.", "info");
    },
    [forgetAudio, notify],
  );

  const clearTracks = useCallback(() => {
    forgetAudio();
    currentIdRef.current = null;
    setTracks([]);
    setCurrentId(null);
    setCurrentTime(0);
    setDuration(0);
    setIsPlaying(false);
    notify("Session cleared. Your downloads are untouched.", "info");
  }, [forgetAudio, notify]);

  const renameTrack = useCallback((id: string, title: string) => {
    const next = title.trim().slice(0, 80);
    if (!next) return;
    setTracks((previous) =>
      previous.map((track) =>
        track.id === id ? { ...track, title: next } : track,
      ),
    );
  }, []);

  const generate = useCallback(
    (input: SunaGenerateInput) => {
      if (abortRef.current) return;

      lastRequestRef.current = input;
      const controller = new AbortController();
      abortRef.current = controller;
      const startedAt = Date.now();

      setGeneration({
        stage: "connecting",
        prompt: input.prompt,
        presetId: input.presetId,
        startedAt,
      });

      void (async () => {
        try {
          const result = await generateSunaTrack(input, {
            signal: controller.signal,
            onStatus: (status) => {
              if (controller.signal.aborted) return;
              setGeneration((previous) => ({
                ...previous,
                stage: status.stage,
                position: status.position ?? previous.position,
              }));
            },
          });

          if (controller.signal.aborted) return;

          const actualDuration = await readAudioDuration(result.audioUrl);
          const preset = getPreset(input.presetId);
          const track: Track = {
            id: makeId(),
            title: titleFromPrompt(input.prompt),
            prompt: input.prompt.trim(),
            presetId: preset.id,
            presetLabel: preset.label,
            audioUrl: result.audioUrl,
            wavUrl: result.wavUrl,
            wavName: result.wavName,
            telemetry: result.telemetry,
            lyrics: result.lyrics,
            mimeType: result.mimeType,
            fileName: result.fileName,
            requestedDuration: result.requestedDuration,
            duration: actualDuration,
            quality: input.quality,
            vocalName: input.vocalFile?.name,
            createdAt: Date.now(),
          };

          setTracks((previous) => [track, ...previous]);
          currentIdRef.current = track.id;
          setCurrentId(track.id);
          setGeneration({
            stage: "complete",
            prompt: input.prompt,
            presetId: input.presetId,
            startedAt,
          });
          notify("Your track is ready. Press play to listen.", "success");
        } catch (error) {
          if (isAbortError(error)) {
            setGeneration((previous) => ({
              ...previous,
              stage: "cancelled",
            }));
            notify("Generation cancelled.", "info");
          } else {
            setGeneration((previous) => ({
              ...previous,
              stage: "error",
              error: generationErrorState(error),
            }));
          }
        } finally {
          abortRef.current = null;
        }
      })();
    },
    [notify],
  );

  const cancelGeneration = useCallback(() => {
    abortRef.current?.abort();
  }, []);

  const retryGeneration = useCallback(() => {
    const request = lastRequestRef.current;
    if (request && !abortRef.current) {
      generate(request);
    }
  }, [generate]);

  const dismissGeneration = useCallback(() => {
    if (abortRef.current) return;
    setGeneration({ stage: "idle" });
  }, []);

  const downloadTrack = useCallback(
    (track: Track) => {
      if (downloadingId) return;
      setDownloadingId(track.id);
      // Prefer the Space's 48 kHz 16-bit WAV master when it exists; the MP3
      // stays the playback format.
      const url = track.wavUrl ?? track.audioUrl;
      const fileName = track.wavUrl ? track.wavName : track.fileName;
      void downloadTrackAudio(url, track.title, fileName)
        .then(() => {
          notify("Download started.", "success");
        })
        .catch((error: unknown) => {
          notify(
            error instanceof SunaError
              ? error.message
              : "The download couldn't start. Try again.",
            "error",
          );
        })
        .finally(() => {
          setDownloadingId(null);
        });
    },
    [downloadingId, notify],
  );

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    const onTimeUpdate = () => setCurrentTime(audio.currentTime);
    const onLoadedMetadata = () => {
      if (Number.isFinite(audio.duration)) {
        setDuration(audio.duration);
        const id = currentIdRef.current;
        if (id) {
          setTracks((previous) =>
            previous.map((track) =>
              track.id === id && track.duration === undefined
                ? { ...track, duration: audio.duration }
                : track,
            ),
          );
        }
      }
    };
    const onPlay = () => setIsPlaying(true);
    const onPause = () => setIsPlaying(false);
    const onEnded = () => {
      setIsPlaying(false);
      setCurrentTime(0);
    };
    const onError = () => {
      setIsPlaying(false);
      notify(
        "This audio file couldn't be loaded. It may have expired — regenerate the track.",
        "error",
      );
    };

    audio.addEventListener("timeupdate", onTimeUpdate);
    audio.addEventListener("loadedmetadata", onLoadedMetadata);
    audio.addEventListener("play", onPlay);
    audio.addEventListener("pause", onPause);
    audio.addEventListener("ended", onEnded);
    audio.addEventListener("error", onError);

    return () => {
      audio.removeEventListener("timeupdate", onTimeUpdate);
      audio.removeEventListener("loadedmetadata", onLoadedMetadata);
      audio.removeEventListener("play", onPlay);
      audio.removeEventListener("pause", onPause);
      audio.removeEventListener("ended", onEnded);
      audio.removeEventListener("error", onError);
    };
  }, [notify]);

  useEffect(() => {
    if (!("mediaSession" in navigator)) return;
    if (currentTrack) {
      navigator.mediaSession.metadata = new MediaMetadata({
        title: currentTrack.title,
        artist: "Suna AI",
        album: "Suna Studio session",
      });
    } else {
      navigator.mediaSession.metadata = null;
    }
  }, [currentTrack]);

  useEffect(() => {
    if (!("mediaSession" in navigator)) return;

    const onPlay = () => togglePlay();
    const onPause = () => togglePlay();
    const onSeekBack = (details: MediaSessionActionDetails) => {
      seek((audioRef.current?.currentTime ?? 0) - (details.seekOffset ?? 10));
    };
    const onSeekForward = (details: MediaSessionActionDetails) => {
      seek((audioRef.current?.currentTime ?? 0) + (details.seekOffset ?? 10));
    };
    const onSeekTo = (details: MediaSessionActionDetails) => {
      if (typeof details.seekTime === "number") seek(details.seekTime);
    };

    try {
      navigator.mediaSession.setActionHandler("play", onPlay);
      navigator.mediaSession.setActionHandler("pause", onPause);
      navigator.mediaSession.setActionHandler("seekbackward", onSeekBack);
      navigator.mediaSession.setActionHandler("seekforward", onSeekForward);
      navigator.mediaSession.setActionHandler("seekto", onSeekTo);
    } catch {
      // A browser may reject individual media-session actions.
    }

    return () => {
      try {
        navigator.mediaSession.setActionHandler("play", null);
        navigator.mediaSession.setActionHandler("pause", null);
        navigator.mediaSession.setActionHandler("seekbackward", null);
        navigator.mediaSession.setActionHandler("seekforward", null);
        navigator.mediaSession.setActionHandler("seekto", null);
      } catch {
        // Ignore unsupported cleanup.
      }
    };
  }, [seek, togglePlay]);

  useEffect(() => {
    if (!("mediaSession" in navigator)) return;
    navigator.mediaSession.playbackState = isPlaying ? "playing" : "paused";
  }, [isPlaying]);

  useEffect(() => {
    return () => {
      abortRef.current?.abort();
    };
  }, []);

  const value = useMemo<StudioContextValue>(
    () => ({
      tracks,
      currentTrack,
      isPlaying,
      currentTime,
      duration,
      volume,
      muted,
      generation,
      isGenerating: ACTIVE_STAGES.has(generation.stage),
      availability,
      notice,
      downloadingId,
      playTrack,
      togglePlay,
      selectTrack,
      seek,
      setVolume,
      toggleMute,
      playNext,
      playPrevious,
      removeTrack,
      clearTracks,
      renameTrack,
      generate,
      cancelGeneration,
      retryGeneration,
      dismissGeneration,
      downloadTrack,
      notify,
      dismissNotice,
    }),
    [
      tracks,
      currentTrack,
      isPlaying,
      currentTime,
      duration,
      volume,
      muted,
      generation,
      availability,
      notice,
      downloadingId,
      playTrack,
      togglePlay,
      selectTrack,
      seek,
      setVolume,
      toggleMute,
      playNext,
      playPrevious,
      removeTrack,
      clearTracks,
      renameTrack,
      generate,
      cancelGeneration,
      retryGeneration,
      dismissGeneration,
      downloadTrack,
      notify,
      dismissNotice,
    ],
  );

  return (
    <StudioContext.Provider value={value}>
      {children}
      <audio ref={audioRef} preload="metadata" className="hidden" />
    </StudioContext.Provider>
  );
}

export function useStudio(): StudioContextValue {
  const context = useContext(StudioContext);
  if (!context) {
    throw new Error("useStudio must be used inside a StudioProvider.");
  }
  return context;
}
