import { useState } from "react";
import type { CSSProperties } from "react";
import { Composer } from "./components/Composer";
import { GenerationPanel } from "./components/GenerationPanel";
import { Icon } from "./components/Icon";
import { MobileDrawer } from "./components/MobileDrawer";
import { NowPlaying } from "./components/NowPlaying";
import { PlayerBar } from "./components/PlayerBar";
import { Rail } from "./components/Sidebar";
import { SunaMark } from "./components/SunaMark";
import { TopBar } from "./components/TopBar";
import { TrackCard } from "./components/TrackCard";
import { focusComposer } from "./lib/focus";
import { pluralise } from "./lib/format";
import {
  SUNA_MODEL_LABEL,
  SUNA_SPACE_URL,
  SUNA_SPACE_ID,
} from "./lib/suna";
import type { Track } from "./lib/types";
import { useStudio } from "./studio/StudioProvider";

const DEVSNIPS_URL = "https://github.com/sarthakbystander/DevSnips";
const SUNA_SITE_URL = "https://suna.jjcoders.com";

function Hero() {
  return (
    <section className="relative pt-12 text-center sm:pt-16">
      <p className="font-mono text-[9px] uppercase tracking-[0.32em] text-accent-deep/90">
        {SUNA_MODEL_LABEL} · Live Space
      </p>

      <h1 className="mx-auto mt-4 max-w-[760px] text-balance font-display text-[52px] leading-[0.98] tracking-[0.01em] text-ink sm:text-[72px] lg:text-[84px]">
        Start with a{" "}
        <em className="text-accent-deep not-italic font-light">feeling.</em>
      </h1>
      <p className="mx-auto mt-4 max-w-[520px] text-[12.5px] leading-6 text-muted sm:text-[13.5px]">
        Describe the track in your head. Suna AI renders it on its public
        Space as a real stereo master — then it is yours to play, shape, and
        keep.
      </p>

      <div className="mt-5 flex flex-wrap items-center justify-center gap-x-4 gap-y-2 text-[9.5px] text-faint">
        <span className="inline-flex items-center gap-1.5">
          <Icon name="wave" size={12} className="text-accent" />
          Real Suna render
        </span>
        <span className="inline-flex items-center gap-1.5">
          <Icon name="link" size={11} />
          Public Space · no account
        </span>
        <span className="inline-flex items-center gap-1.5">
          <Icon name="clock" size={11} />
          Session-only
        </span>
      </div>
    </section>
  );
}

function EmptySession() {
  return (
    <div className="mt-4 overflow-hidden rounded-[26px] border border-dashed border-line-strong bg-surface/35 p-6 sm:p-8">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center">
        <div className="grid h-16 w-16 shrink-0 place-items-center rounded-2xl bg-accent-soft/70 text-accent">
          <SunaMark size={38} cut="#0D1322" />
        </div>
        <div className="text-left">
          <h3 className="font-display text-[25px] leading-tight text-ink">
            The room is quiet.
          </h3>
          <p className="mt-1 max-w-[430px] text-[11.5px] leading-5 text-muted">
            Describe a track above and Suna will render it here, with its real
            duration, format, and telemetry. Nothing is stored after you leave
            this tab.
          </p>
        </div>
      </div>
      <div className="mt-5 flex flex-wrap gap-1.5">
        {["24–68s songs", "6 artist presets", "Editable lyrics", "MP3 + WAV masters"].map(
          (item) => (
            <span
              key={item}
              className="rounded-full border border-line bg-surface/70 px-2.5 py-1 text-[9px] text-muted"
            >
              {item}
            </span>
          ),
        )}
      </div>
    </div>
  );
}

function SessionFeed({ tracks }: { tracks: Track[] }) {
  const [featured, ...earlier] = tracks;

  return (
    <section id="session" aria-labelledby="session-heading" className="mt-14 scroll-mt-20 sm:mt-16">
      <div className="flex items-end justify-between gap-4">
        <div>
          <p className="text-[9px] font-semibold uppercase tracking-[0.22em] text-faint">
            This session
          </p>
          <h2
            id="session-heading"
            className="mt-1.5 font-display text-[30px] leading-none tracking-[0.01em] text-ink"
          >
            Rendered{" "}
            <em className="text-accent-deep not-italic">yours.</em>
          </h2>
        </div>
        <span className="pb-1 text-[9px] text-faint">
          {tracks.length > 0
            ? `${pluralise(tracks.length, "render")} · newest first`
            : "Nothing rendered yet"}
        </span>
      </div>

      {tracks.length === 0 ? (
        <EmptySession />
      ) : (
        <div>
          {featured && (
            <div className="mt-5">
              <TrackCard track={featured} featured />
            </div>
          )}
          {earlier.length > 0 && (
            <div className="mt-5">
              <p className="px-0.5 pb-2 text-[8.5px] font-semibold uppercase tracking-[0.18em] text-faint">
                Earlier in this session
              </p>
              <div className="no-scrollbar flex gap-2.5 overflow-x-auto pb-1.5">
                {earlier.map((track) => (
                  <TrackCard key={track.id} track={track} />
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </section>
  );
}

function Footer() {
  return (
    <footer className="mt-14 border-t border-line/70 pb-10 pt-5 sm:mt-16">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div className="max-w-[450px]">
          <p className="text-[9.5px] leading-4 text-faint">
            Suna Studio is an open DevSnips template, built for Suna AI. Audio
            is generated on the public{" "}
            <a
              href={SUNA_SPACE_URL}
              target="_blank"
              rel="noreferrer"
              className="underline decoration-line-strong underline-offset-2 transition hover:text-muted"
            >
              Hugging Face Space
            </a>
            . This app does not store audio or prompts; tracks live in this tab
            until you close it.
          </p>
          <p className="mt-2 font-mono text-[8px] uppercase tracking-[0.14em] text-faint/80">
            Session media is served by {SUNA_SPACE_ID}
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-x-4 gap-y-2">
          <a
            href={SUNA_SITE_URL}
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-1 text-[9px] font-medium text-muted transition hover:text-ink"
          >
            Suna AI
            <Icon name="arrow-up-right" size={10} />
          </a>
          <a
            href={SUNA_SPACE_URL}
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-1 text-[9px] font-medium text-muted transition hover:text-ink"
          >
            The Space
            <Icon name="arrow-up-right" size={10} />
          </a>
          <a
            href={DEVSNIPS_URL}
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-1 text-[9px] font-medium text-muted transition hover:text-ink"
          >
            DevSnips
            <Icon name="arrow-up-right" size={10} />
          </a>
        </div>
      </div>
    </footer>
  );
}

function NoticeToast() {
  const { notice, dismissNotice } = useStudio();
  if (!notice) return null;

  const tone =
    notice.tone === "success"
      ? "border-sage/40 bg-sage-soft text-ink"
      : notice.tone === "error"
        ? "border-accent/35 bg-accent-soft text-accent-deep"
        : "border-line bg-surface text-ink-2";

  return (
    <div className="pointer-events-none fixed inset-x-0 bottom-[calc(76px+env(safe-area-inset-bottom)+0.75rem)] z-[60] flex justify-center px-4 lg:bottom-[100px]">
      <div
        role="status"
        aria-live="polite"
        className={`pointer-events-auto flex max-w-[92vw] items-center gap-2 rounded-full border px-3.5 py-2 text-[10.5px] font-medium shadow-lift backdrop-blur animate-fade-up ${tone}`}
      >
        <Icon
          name={
            notice.tone === "success"
              ? "check"
              : notice.tone === "error"
                ? "alert"
                : "info"
          }
          size={13}
          className="shrink-0"
        />
        <span className="min-w-0">{notice.message}</span>
        <button
          type="button"
          onClick={dismissNotice}
          aria-label="Dismiss notification"
          className="ml-1 grid h-5 w-5 shrink-0 place-items-center rounded-full opacity-55 transition hover:bg-white/10 hover:opacity-100"
        >
          <Icon name="close" size={11} />
        </button>
      </div>
    </div>
  );
}

const OCEAN_RAYS = [
  { el: "span", left: "4%", rot: "6deg", width: "13rem", duration: "26s", delay: "0s", opacity: "0.6" },
  { el: "span", left: "22%", rot: "9deg", width: "17rem", duration: "31s", delay: "1.5s", opacity: "0.5" },
  { el: "span", left: "58%", rot: "-5deg", width: "24rem", duration: "36s", delay: "0.5s", opacity: "0.7" },
  { el: "span", left: "78%", rot: "-9deg", width: "14rem", duration: "29s", delay: "3s", opacity: "0.45" },
  { el: "i", left: "40%", rot: "3deg", width: "9rem", duration: "39s", delay: "2s", opacity: "0.5" },
];

function BackdropScene() {
  return (
    <div className="ocean-scene pointer-events-none fixed inset-0 z-0" aria-hidden="true">
      <div className="ocean-rays" style={{ opacity: 0.6 }}>
        {OCEAN_RAYS.map((ray, index) => (
          <span
            key={index}
            style={
              {
                left: ray.left,
                width: ray.width,
                "--ray-rot": ray.rot,
                "--ray-op": ray.opacity,
                animationDuration: ray.duration,
                animationDelay: ray.delay,
              } as CSSProperties
            }
          />
        ))}
      </div>
      <div className="ocean-crests" />
      <div className="ocean-caustic ocean-caustic-a" />
      <div className="ocean-caustic ocean-caustic-b" />
      <div className="ocean-particles ocean-particles-a" />
      <div className="ocean-particles ocean-particles-b" />
      <div className="ocean-vignette" />
      <div className="paper-grain absolute inset-0 opacity-[0.035]" />
    </div>
  );
}

export default function App() {
  const { tracks } = useStudio();
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <div className="relative min-h-dvh bg-paper text-ink">
      <BackdropScene />

      <a
        href="#main"
        className="fixed left-4 top-4 z-[100] -translate-y-24 rounded-full bg-cream px-4 py-2 text-[11px] font-medium text-night transition focus:translate-y-0"
      >
        Skip to content
      </a>

      <div className="relative z-10 mx-auto flex min-h-dvh w-full max-w-[1600px]">
        <Rail />

        <div className="flex min-w-0 flex-1 flex-col">
          <TopBar onOpenMenu={() => setMenuOpen(true)} />

          <main
            id="main"
            tabIndex={-1}
            className="flex-1 pb-[calc(82px+env(safe-area-inset-bottom))] focus:outline-none lg:pb-[104px]"
          >
            <div className="mx-auto w-full max-w-[860px] px-4 sm:px-6 lg:px-8">
              <Hero />
              <div className="mt-8 sm:mt-10">
                <Composer />
                <GenerationPanel />
              </div>
              <SessionFeed tracks={tracks} />
              <Footer />
            </div>
          </main>
        </div>

        <aside className="sticky top-0 hidden h-[calc(100dvh-84px)] w-[308px] shrink-0 border-l border-line/60 min-[1360px]:block">
          <div className="h-full overflow-y-auto px-5 py-6">
            <NowPlaying />
          </div>
        </aside>
      </div>

      <MobileDrawer
        open={menuOpen}
        onClose={() => setMenuOpen(false)}
        onNewTrack={focusComposer}
      />
      <PlayerBar />
      <NoticeToast />
    </div>
  );
}
