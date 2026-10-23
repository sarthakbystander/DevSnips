import {
  useRef,
  useState,
  type DragEvent,
  type FormEvent,
  type KeyboardEvent,
} from "react";
import { Icon } from "./Icon";
import { Slider } from "./Slider";
import { paletteGradient } from "../lib/palettes";
import { formatBytes, formatTime } from "../lib/format";
import {
  DEFAULT_DURATION,
  DEFAULT_VOCAL_MIX,
  DURATION_STEP,
  MAX_DURATION,
  MAX_PROMPT_LENGTH,
  MAX_VOCAL_BYTES,
  MIN_DURATION,
  MIN_VOCAL_MIX,
  SUNA_PRESETS,
  SUNA_QUALITY_MODES,
  getPreset,
  getQualityMode,
  readAudioDuration,
} from "../lib/suna";
import type { SoundQuality, SunaGenerateInput } from "../lib/types";
import { useStudio } from "../studio/StudioProvider";

type Mode = "simple" | "custom";

interface Idea {
  label: string;
  prompt: string;
  presetId: string;
}

const IDEAS: Idea[] = [
  {
    label: "Midnight drive",
    prompt:
      "Midnight drive through neon rain, breathy romantic vocals, warm piano, bouncy metallic bassline",
    presetId: "slap-house",
  },
  {
    label: "Armor up",
    prompt:
      "Rising above a hard week, raw vocals turning tender, big piano, cinematic stadium drums",
    presetId: "sia-power-ballad",
  },
  {
    label: "Stadium sunrise",
    prompt:
      "Stadium sunrise, raspy anthem vocals, thunderous stomping drums, burning scars into flame",
    presetId: "arena-rock",
  },
  {
    label: "Golden meadow",
    prompt:
      "Dancing barefoot in a golden meadow, bright folk vocals, plucky balalaika, joyful dance kick",
    presetId: "matushka-folk",
  },
  {
    label: "Carnival dusk",
    prompt:
      "Carnival dusk by the sea, call-and-response vocals, syncopated dembow, warm log-drum sub-bass",
    presetId: "afro-latin",
  },
  {
    label: "Night lullaby",
    prompt:
      "A quiet night lullaby in French, weeping flute and violin, operatic chorus lift, soft rain",
    presetId: "indila-chanson",
  },
];

function isAudioFile(file: File): boolean {
  return (
    file.type.startsWith("audio/") ||
    /\.(mp3|wav|m4a|ogg|webm|aac|flac)$/i.test(file.name)
  );
}

export function Composer() {
  const { generate, isGenerating } = useStudio();

  const [mode, setMode] = useState<Mode>("simple");
  const [prompt, setPrompt] = useState("");
  const [presetId, setPresetId] = useState(SUNA_PRESETS[0].id);
  const [lyrics, setLyrics] = useState("");
  const lyricsTouchedRef = useRef(false);
  const [quality, setQuality] = useState<SoundQuality>("turbo");
  const [duration, setDuration] = useState(DEFAULT_DURATION);
  const [vocalFile, setVocalFile] = useState<File | null>(null);
  const [vocalDuration, setVocalDuration] = useState<number | undefined>();
  const [vocalMix, setVocalMix] = useState(DEFAULT_VOCAL_MIX);
  const [error, setError] = useState<string | null>(null);
  const [dragActive, setDragActive] = useState(false);

  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const lyricsRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const vocalZoneRef = useRef<HTMLDivElement>(null);
  const vocalRequestRef = useRef(0);

  const preset = getPreset(presetId);
  const qualityMode = getQualityMode(quality);
  const remainingCharacters = MAX_PROMPT_LENGTH - prompt.length;

  const choosePreset = (id: string) => {
    setPresetId(id);
    setError(null);
    /**
     * The Space's own UI refills the lyrics box whenever the preset changes.
     * Follow that convention until the user has edited the songbook.
     */
    if (!lyricsTouchedRef.current) {
      setLyrics(getPreset(id).lyrics);
    }
  };

  const editLyrics = (value: string) => {
    lyricsTouchedRef.current = true;
    setLyrics(value);
    setError(null);
  };

  const chooseMode = (next: Mode) => {
    setMode(next);
    setError(null);
    if (next === "custom" && !lyricsTouchedRef.current) {
      setLyrics(preset.lyrics);
    }
  };

  const applyIdea = (idea: Idea) => {
    setPrompt(idea.prompt);
    setMode("simple");
    choosePreset(idea.presetId);
    textareaRef.current?.focus();
  };

  const acceptVocal = async (file: File | undefined) => {
    if (!file) return;

    if (!isAudioFile(file)) {
      setError("Choose an audio file — MP3, WAV, M4A, OGG, or WebM.");
      return;
    }
    if (file.size > MAX_VOCAL_BYTES) {
      setError(`That clip is larger than ${formatBytes(MAX_VOCAL_BYTES)}. Try a shorter file.`);
      return;
    }

    const request = vocalRequestRef.current + 1;
    vocalRequestRef.current = request;
    setError(null);
    setVocalFile(file);
    setVocalDuration(undefined);

    const objectUrl = URL.createObjectURL(file);
    const actualDuration = await readAudioDuration(objectUrl);
    URL.revokeObjectURL(objectUrl);

    if (vocalRequestRef.current === request) {
      setVocalDuration(actualDuration);
    }
  };

  const handleFileInput = (file: File | undefined) => {
    void acceptVocal(file);
  };

  const removeVocal = () => {
    vocalRequestRef.current += 1;
    setVocalFile(null);
    setVocalDuration(undefined);
    setError(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  const handleDrop = (event: DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setDragActive(false);
    void acceptVocal(event.dataTransfer.files?.[0]);
  };

  const submit = () => {
    if (isGenerating) return;
    const cleanPrompt = prompt.trim();

    if (cleanPrompt.length < 3) {
      setError(
        `Give Suna a little more to work with — at least 3 characters.`,
      );
      textareaRef.current?.focus();
      return;
    }

    const input: SunaGenerateInput = {
      prompt: cleanPrompt,
      presetId,
      // In Simple mode Suna sings the preset's own songbook (custom_lyrics="").
      lyrics: mode === "custom" ? lyrics : "",
      quality,
      durationSec: duration,
      vocalFile,
      vocalMixLevel: vocalMix,
    };

    setError(null);
    generate(input);
  };

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    submit();
  };

  const handlePromptKeyDown = (
    event: KeyboardEvent<HTMLTextAreaElement>,
  ) => {
    if ((event.metaKey || event.ctrlKey) && event.key === "Enter") {
      event.preventDefault();
      submit();
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="overflow-hidden rounded-[26px] border border-line bg-surface shadow-card"
      aria-labelledby="composer-label"
    >
      <div className="p-4 sm:p-5">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-2.5">
            <span className="grid h-7 w-7 place-items-center rounded-full bg-accent-soft text-accent-deep">
              <Icon name="sparkles" size={15} />
            </span>
            <div>
              <h2
                id="composer-label"
                className="text-[13px] font-semibold tracking-[-0.01em] text-ink"
              >
                New track
              </h2>
              <p className="hidden text-[11px] text-muted sm:block">
                One idea is enough to begin.
              </p>
            </div>
          </div>

          <div
            className="flex rounded-full border border-line bg-surface-2 p-1"
            role="group"
            aria-label="Composer mode"
          >
            {(["simple", "custom"] as Mode[]).map((item) => (
              <button
                key={item}
                type="button"
                onClick={() => chooseMode(item)}
                aria-pressed={mode === item}
                className={`rounded-full px-3.5 py-1.5 text-[11px] font-medium capitalize transition ${
                  mode === item
                    ? "bg-surface text-ink shadow-sm"
                    : "text-muted hover:text-ink"
                }`}
              >
                {item}
              </button>
            ))}
          </div>
        </div>

        <div className="mt-4 rounded-2xl border border-line-strong/70 bg-surface-2/40 transition focus-within:border-ink/30 focus-within:bg-surface">
          <label htmlFor="prompt" className="sr-only">
            Describe the track you want to make
          </label>
          <textarea
            ref={textareaRef}
            id="prompt"
            value={prompt}
            onChange={(event) => {
              setPrompt(event.target.value);
              if (error) setError(null);
            }}
            onKeyDown={handlePromptKeyDown}
            maxLength={MAX_PROMPT_LENGTH}
            rows={3}
            placeholder="Warm collapsing night, headlights in the rain, a voice that refuses to stay down…"
            className="block min-h-[96px] w-full resize-none bg-transparent px-4 pb-2 pt-4 text-[15px] leading-6 text-ink placeholder:text-faint/90 focus:outline-none sm:min-h-[108px] sm:text-base"
            aria-describedby="prompt-hint"
          />
          <div className="flex items-center justify-between gap-3 px-4 pb-3">
            <p
              id="prompt-hint"
              className="text-[10.5px] leading-4 text-muted"
            >
              Mood, story, and style all shape the master.{" "}
              <span className="hidden sm:inline">
                <kbd className="rounded border border-line bg-surface px-1 py-0.5 font-mono text-[9px] text-muted">
                  ⌘/Ctrl
                </kbd>{" "}
                +{" "}
                <kbd className="rounded border border-line bg-surface px-1 py-0.5 font-mono text-[9px] text-muted">
                  ↵
                </kbd>{" "}
                to generate.
              </span>
            </p>
            <span
              className={`font-mono text-[10px] tabular-nums ${
                remainingCharacters < 40 ? "text-accent-deep" : "text-faint"
              }`}
              aria-hidden="true"
            >
              {prompt.length}/{MAX_PROMPT_LENGTH}
            </span>
          </div>
        </div>

        <div className="mt-3 flex flex-wrap items-center gap-2">
          <span className="mr-0.5 text-[10px] uppercase tracking-[0.16em] text-faint">
            Try
          </span>
          {IDEAS.map((idea) => (
            <button
              key={idea.label}
              type="button"
              onClick={() => applyIdea(idea)}
              className="rounded-full border border-line bg-surface px-2.5 py-1 text-[11px] text-muted transition hover:border-line-strong hover:bg-surface-2 hover:text-ink"
            >
              {idea.label}
            </button>
          ))}
        </div>

        {mode === "simple" ? (
          <div className="mt-5">
            <div className="flex items-baseline justify-between gap-3">
              <div>
                <p className="text-[11px] font-semibold uppercase tracking-[0.14em] text-ink">
                  Voice & world
                </p>
                <p className="mt-0.5 text-[11px] text-muted">
                  Suna sings the preset's songbook. Open Custom to edit lyrics.
                </p>
              </div>
              <span className="font-mono text-[10px] text-faint">
                {duration}s
              </span>
            </div>

            <div
              className="mt-3 flex flex-wrap gap-1.5 pb-1"
              role="group"
              aria-label="Sound preset"
            >
              {SUNA_PRESETS.map((item) => {
                const selected = presetId === item.id;
                return (
                  <button
                    key={item.id}
                    type="button"
                    onClick={() => choosePreset(item.id)}
                    aria-pressed={selected}
                    title={item.description}
                    className={`group flex items-center gap-1.5 rounded-full border px-2.5 py-2 text-[11px] font-medium transition ${
                      selected
                        ? "border-accent bg-accent text-white shadow-sm"
                        : "border-line bg-surface text-ink-2 hover:border-line-strong hover:bg-surface-2"
                    }`}
                  >
                    <span
                      className={`h-3 w-3 rounded-full ring-1 ring-inset ring-black/10 ${
                        selected ? "opacity-100" : "opacity-80"
                      }`}
                      style={{ background: paletteGradient(item.palette) }}
                      aria-hidden="true"
                    />
                    {item.shortLabel}
                  </button>
                );
              })}
            </div>
          </div>
        ) : (
          <div className="mt-6 space-y-6">
            <fieldset>
              <legend className="text-[11px] font-semibold uppercase tracking-[0.14em] text-ink">
                Voice & world
              </legend>
              <p className="mt-0.5 text-[11px] text-muted">
                Each artist preset loads its own singing voice, key, and tempo.
                Choose the one closest to your idea.
              </p>

              <div className="mt-3 grid gap-2 sm:grid-cols-2">
                {SUNA_PRESETS.map((item) => {
                  const checked = presetId === item.id;
                  return (
                    <label
                      key={item.id}
                      className={`relative flex cursor-pointer items-start gap-3 rounded-2xl border p-3.5 transition focus-within:ring-2 focus-within:ring-accent/60 focus-within:ring-offset-2 focus-within:ring-offset-surface ${
                        checked
                          ? "border-accent/70 bg-accent-soft/35"
                          : "border-line bg-surface hover:border-line-strong hover:bg-surface-2/60"
                      }`}
                    >
                      <input
                        type="radio"
                        name="suna-preset"
                        value={item.id}
                        checked={checked}
                        onChange={() => choosePreset(item.id)}
                        className="sr-only"
                      />
                      <span
                        className="mt-0.5 h-7 w-7 shrink-0 rounded-full ring-1 ring-inset ring-black/10"
                        style={{ background: paletteGradient(item.palette) }}
                        aria-hidden="true"
                      />
                      <span className="min-w-0">
                        <span className="flex items-center gap-1.5 text-[12.5px] font-semibold text-ink">
                          {item.label}
                        </span>
                        <span className="mt-0.5 block text-[11px] leading-4 text-muted">
                          {item.description}
                        </span>
                      </span>
                      {checked && (
                        <span className="absolute right-2.5 top-2.5 grid h-4 w-4 place-items-center rounded-full bg-accent text-white">
                          <Icon name="check" size={10} strokeWidth={2.4} />
                        </span>
                      )}
                    </label>
                  );
                })}
              </div>
            </fieldset>

            <div>
              <div className="flex items-baseline justify-between gap-3">
                <div>
                  <label
                    htmlFor="lyrics"
                    className="text-[11px] font-semibold uppercase tracking-[0.14em] text-ink"
                  >
                    Lyrics
                  </label>
                  <p className="mt-0.5 text-[11px] text-muted">
                    Suna sings these. Structure tags like{" "}
                    <code className="rounded border border-line bg-surface px-1 font-mono text-[9.5px]">
                      [Verse]
                    </code>{" "}
                    and{" "}
                    <code className="rounded border border-line bg-surface px-1 font-mono text-[9.5px]">
                      [Chorus]
                    </code>{" "}
                    are honored.
                  </p>
                </div>
                {lyricsTouchedRef.current && (
                  <button
                    type="button"
                    onClick={() => {
                      lyricsTouchedRef.current = false;
                      setLyrics(preset.lyrics);
                    }}
                    className="rounded-full border border-line bg-surface px-2.5 py-1 text-[10px] font-medium text-ink-2 transition hover:bg-surface-2"
                  >
                    Use {preset.shortLabel} songbook
                  </button>
                )}
              </div>
              <textarea
                ref={lyricsRef}
                id="lyrics"
                value={lyrics}
                onChange={(event) => editLyrics(event.target.value)}
                rows={6}
                placeholder={`Load a songbook from a preset, or write your own.`}
                className="mt-3 block w-full resize-y rounded-2xl border border-line-strong/70 bg-surface-2/40 px-4 py-3 font-mono text-[11.5px] leading-5 text-ink placeholder:text-faint/90 focus:border-ink/30 focus:bg-surface focus:outline-none"
              />
              <p className="mt-1.5 px-1 text-[10px] leading-4 text-muted">
                Leaving it empty lets the{" "}
                <span className="font-medium text-ink-2">
                  {preset.label}
                </span>{" "}
                songbook sing. Custom lines are trimmed; the Space also cleans
                structure tags for you.
              </p>
            </div>

            <div className="grid gap-3 sm:grid-cols-2">
              <div className="rounded-2xl border border-line bg-surface-2/40 p-4">
                <div className="flex items-baseline justify-between gap-3">
                  <label
                    htmlFor="duration"
                    className="text-[11px] font-semibold uppercase tracking-[0.14em] text-ink"
                  >
                    Length
                  </label>
                  <span className="font-mono text-[11px] tabular-nums text-ink-2">
                    {duration}s
                  </span>
                </div>
                <Slider
                  label="Track length"
                  value={duration}
                  min={MIN_DURATION}
                  max={MAX_DURATION}
                  step={DURATION_STEP}
                  onChange={setDuration}
                  valueText={`${duration} seconds`}
                  className="mt-3"
                />
                <div className="flex justify-between font-mono text-[9px] text-faint">
                  <span>{MIN_DURATION}s</span>
                  <span>{MAX_DURATION}s</span>
                </div>
                <p className="mt-2 text-[10.5px] leading-4 text-muted">
                  {vocalFile
                    ? "With a vocal clip, the master matches the clip's length up to this target."
                    : "60s leaves room for a full chorus climax, like the Space suggests."}
                </p>
              </div>

              <div className="rounded-2xl border border-line bg-surface-2/40 p-4">
                <div className="flex items-baseline justify-between gap-3">
                  <span className="text-[11px] font-semibold uppercase tracking-[0.14em] text-ink">
                    Synthesis engine
                  </span>
                  <span className="font-mono text-[9.5px] text-faint">
                    A100 SIZES
                  </span>
                </div>
                <div
                  className="mt-3 grid gap-1.5"
                  role="radiogroup"
                  aria-label="Synthesis engine"
                >
                  {SUNA_QUALITY_MODES.map((item) => {
                    const checked = quality === item.id;
                    return (
                      <label
                        key={item.id}
                        className={`flex cursor-pointer items-center gap-2.5 rounded-xl border px-3 py-2 transition focus-within:ring-2 focus-within:ring-accent/60 focus-within:ring-offset-2 focus-within:ring-offset-surface ${
                          checked
                            ? "border-accent/70 bg-accent-soft/35"
                            : "border-line bg-surface hover:bg-surface-2/60"
                        }`}
                      >
                        <input
                          type="radio"
                          name="suna-engine"
                          value={item.id}
                          checked={checked}
                          onChange={() => setQuality(item.id)}
                          className="sr-only"
                        />
                        <span className="flex-1">
                          <span className="block text-[12px] font-medium text-ink">
                            {item.label}
                          </span>
                          <span className="block text-[10px] leading-4 text-muted">
                            {item.description}
                          </span>
                        </span>
                        <span
                          aria-hidden="true"
                          className={`h-3.5 w-3.5 rounded-full border transition ${
                            checked
                              ? "border-accent bg-accent shadow-[inset_0_0_0_2px_white]"
                              : "border-line-strong bg-surface"
                          }`}
                        />
                      </label>
                    );
                  })}
                </div>
                <p className="mt-2 text-[10.5px] leading-4 text-muted">
                  Turbo is the Space's default. High-Fidelity takes about twice
                  as long.
                </p>
              </div>
            </div>

            <div>
              <div className="flex items-baseline justify-between gap-3">
                <div>
                  <p className="text-[11px] font-semibold uppercase tracking-[0.14em] text-ink">
                    Sing-to-Masterpiece
                  </p>
                  <p className="mt-0.5 text-[11px] text-muted">
                    Optional. Suna builds the 48 kHz band around your voice.
                  </p>
                </div>
                {vocalFile && (
                  <span className="rounded-full bg-sage-soft px-2 py-0.5 text-[9px] font-semibold uppercase tracking-[0.12em] text-ink-2">
                    Ready
                  </span>
                )}
              </div>

              <div
                ref={vocalZoneRef}
                tabIndex={-1}
                onDragOver={(event) => {
                  event.preventDefault();
                  setDragActive(true);
                }}
                onDragLeave={() => setDragActive(false)}
                onDrop={handleDrop}
                className={`mt-3 rounded-2xl border border-dashed p-3 transition ${
                  dragActive
                    ? "border-accent bg-accent-soft/40"
                    : "border-line-strong bg-surface-2/30"
                }`}
              >
                <input
                  ref={fileInputRef}
                  id="vocal-upload"
                  type="file"
                  accept="audio/*,.mp3,.wav,.m4a,.ogg,.webm,.aac,.flac"
                  className="sr-only"
                  onChange={(event) => {
                    const file = event.target.files?.[0];
                    event.target.value = "";
                    handleFileInput(file);
                  }}
                />

                {!vocalFile ? (
                  <label
                    htmlFor="vocal-upload"
                    className="flex cursor-pointer items-center gap-3 rounded-xl px-1 py-1"
                  >
                    <span className="grid h-10 w-10 shrink-0 place-items-center rounded-full bg-surface text-ink-2 ring-1 ring-line">
                      <Icon name="upload" size={17} />
                    </span>
                    <span className="min-w-0">
                      <span className="block text-[12.5px] font-medium text-ink">
                        Drop a vocal clip, or browse
                      </span>
                      <span className="mt-0.5 block text-[10.5px] leading-4 text-muted">
                        MP3, WAV, M4A, OGG · up to {formatBytes(MAX_VOCAL_BYTES)}{" "}
                        · analyzed for key & tempo
                      </span>
                    </span>
                  </label>
                ) : (
                  <div className="flex items-center gap-3">
                    <span className="grid h-10 w-10 shrink-0 place-items-center rounded-full bg-surface text-accent-deep ring-1 ring-line">
                      <Icon name="music" size={17} />
                    </span>
                    <div className="min-w-0 flex-1">
                      <p className="truncate text-[12.5px] font-medium text-ink">
                        {vocalFile.name}
                      </p>
                      <p className="mt-0.5 font-mono text-[9.5px] text-muted">
                        {formatBytes(vocalFile.size)}
                        {vocalDuration
                          ? ` · ${formatTime(vocalDuration)} clip`
                          : " · reading clip"}
                      </p>
                    </div>
                    <label
                      htmlFor="vocal-upload"
                      className="cursor-pointer rounded-full border border-line bg-surface px-2.5 py-1 text-[10px] font-medium text-ink-2 transition hover:bg-surface-2"
                    >
                      Replace
                    </label>
                    <button
                      type="button"
                      onClick={removeVocal}
                      aria-label="Remove vocal clip"
                      className="grid h-8 w-8 place-items-center rounded-full text-muted transition hover:bg-surface hover:text-ink"
                    >
                      <Icon name="close" size={14} />
                    </button>
                  </div>
                )}

                {vocalFile && (
                  <p className="mt-2 px-1 text-[10px] leading-4 text-muted">
                    The band runs for {Math.min(vocalDuration ?? duration, duration)}s —
                    your clip's length, clipped to the Length slider. Suna
                    detects key & tempo from your voice.
                  </p>
                )}
              </div>

              {vocalFile && (
                <div className="mt-4 rounded-2xl border border-line bg-surface p-4">
                  <div className="flex items-baseline justify-between gap-3">
                    <label
                      htmlFor="vocal-mix"
                      className="text-[11px] font-semibold uppercase tracking-[0.14em] text-ink"
                    >
                      Vocal vs band mix
                    </label>
                    <span className="font-mono text-[11px] tabular-nums text-ink-2">
                      {vocalMix.toFixed(2)}
                    </span>
                  </div>
                  <Slider
                    label="Vocal vs band mix"
                    value={vocalMix}
                    min={MIN_VOCAL_MIX}
                    max={1.2}
                    step={0.05}
                    onChange={setVocalMix}
                    valueText={`${vocalMix.toFixed(2)} of 1.2`}
                    className="mt-3"
                  />
                  <div className="flex justify-between font-mono text-[9px] text-faint">
                    <span>MORE BED</span>
                    <span>MORE VOICE</span>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {error && (
          <div
            role="alert"
            className="mt-4 flex items-start gap-2 rounded-2xl border border-accent/25 bg-accent-soft/55 px-3.5 py-3 text-[11.5px] leading-5 text-accent-deep"
          >
            <Icon name="alert" size={14} className="mt-0.5 shrink-0" />
            <span>{error}</span>
          </div>
        )}
      </div>

      <div className="flex flex-col gap-3 border-t border-line bg-surface-2/65 px-4 py-3.5 sm:flex-row sm:items-center sm:justify-between sm:px-5">
        <div className="flex items-center gap-2 text-[10.5px] text-muted">
          <span className="relative flex h-1.5 w-1.5">
            <span className="absolute inline-flex h-full w-full rounded-full bg-sage opacity-60" />
            <span className="relative inline-flex h-1.5 w-1.5 rounded-full bg-sage" />
          </span>
          <span>
            Live on Suna's public Space. Tracks stay in this tab.
          </span>
        </div>

        <div className="flex items-center justify-between gap-3 sm:justify-end">
          <span className="font-mono text-[9.5px] uppercase tracking-[0.12em] text-faint">
            {duration}s · {preset.shortLabel} · {qualityMode.shortLabel}
          </span>
          <button
            type="submit"
            disabled={isGenerating}
            className="group inline-flex h-11 items-center justify-center gap-2 rounded-full bg-accent px-5 text-[12.5px] font-semibold text-white shadow-sm transition hover:bg-accent-deep disabled:cursor-wait disabled:opacity-65"
          >
            {isGenerating ? (
              <>
                <span className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-white/30 border-t-white" />
                Composing…
              </>
            ) : (
              <>
                <Icon
                  name="sparkles"
                  size={15}
                  className="transition-transform duration-300 group-hover:rotate-12"
                />
                Generate track
                <Icon
                  name="arrow-right"
                  size={14}
                  className="opacity-55 transition-transform group-hover:translate-x-0.5"
                />
              </>
            )}
          </button>
        </div>
      </div>
    </form>
  );
}
