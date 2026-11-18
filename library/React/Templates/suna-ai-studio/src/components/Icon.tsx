import type { SVGProps } from "react";

export type IconName =
  | "play"
  | "pause"
  | "skip-back"
  | "skip-forward"
  | "volume"
  | "volume-off"
  | "download"
  | "arrow-up-right"
  | "arrow-right"
  | "sparkles"
  | "sun"
  | "menu"
  | "close"
  | "plus"
  | "check"
  | "chevron-down"
  | "chevron-up"
  | "music"
  | "clock"
  | "upload"
  | "trash"
  | "pencil"
  | "rotate"
  | "alert"
  | "copy"
  | "stop"
  | "expand"
  | "info"
  | "link"
  | "wave";

interface IconProps extends Omit<SVGProps<SVGSVGElement>, "name"> {
  name: IconName;
  size?: number;
  strokeWidth?: number;
}

export function Icon({
  name,
  size = 20,
  strokeWidth = 1.7,
  className,
  ...props
}: IconProps) {
  const shared = {
    width: size,
    height: size,
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth,
    strokeLinecap: "round" as const,
    strokeLinejoin: "round" as const,
    "aria-hidden": true,
    focusable: false,
    className,
    ...props,
  };

  switch (name) {
    case "play":
      return (
        <svg {...shared} fill="currentColor" stroke="none">
          <path d="M8.4 5.1c0-.8.9-1.3 1.6-.9l9 6.2c.6.4.6 1.3 0 1.7l-9 6.2c-.7.4-1.6-.1-1.6-.9V5.1Z" />
        </svg>
      );
    case "pause":
      return (
        <svg {...shared} fill="currentColor" stroke="none">
          <rect x="6.5" y="5" width="3.6" height="14" rx="1.2" />
          <rect x="13.9" y="5" width="3.6" height="14" rx="1.2" />
        </svg>
      );
    case "skip-back":
      return (
        <svg {...shared}>
          <path d="M6 5v14" />
          <path d="M18 6.7v10.6c0 .8-.9 1.3-1.6.9l-7.2-5.3a1.1 1.1 0 0 1 0-1.8l7.2-5.3c.7-.4 1.6.1 1.6.9Z" />
        </svg>
      );
    case "skip-forward":
      return (
        <svg {...shared}>
          <path d="M18 5v14" />
          <path d="M6 6.7v10.6c0 .8.9 1.3 1.6.9l7.2-5.3a1.1 1.1 0 0 0 0-1.8L7.6 5.8C6.9 5.4 6 5.9 6 6.7Z" />
        </svg>
      );
    case "volume":
      return (
        <svg {...shared}>
          <path d="M11 5.5 6.8 9H4.2A1.2 1.2 0 0 0 3 10.2v3.6A1.2 1.2 0 0 0 4.2 15h2.6L11 18.5V5.5Z" />
          <path d="M15.2 9.2a4 4 0 0 1 0 5.6" />
          <path d="M17.8 6.8a7.5 7.5 0 0 1 0 10.4" />
        </svg>
      );
    case "volume-off":
      return (
        <svg {...shared}>
          <path d="M11 5.5 6.8 9H4.2A1.2 1.2 0 0 0 3 10.2v3.6A1.2 1.2 0 0 0 4.2 15h2.6L11 18.5V5.5Z" />
          <path d="m16 9.5 4 4" />
          <path d="m20 9.5-4 4" />
        </svg>
      );
    case "download":
      return (
        <svg {...shared}>
          <path d="M12 3v11" />
          <path d="m7.5 10 4.5 4.5 4.5-4.5" />
          <path d="M5 18.5h14" />
        </svg>
      );
    case "arrow-up-right":
      return (
        <svg {...shared}>
          <path d="M7 17 17 7" />
          <path d="M8 7h9v9" />
        </svg>
      );
    case "arrow-right":
      return (
        <svg {...shared}>
          <path d="M4 12h16" />
          <path d="m14 6 6 6-6 6" />
        </svg>
      );
    case "sparkles":
      return (
        <svg {...shared}>
          <path d="M12 3.5c.6 4.2 2.8 6.4 7 7-4.2.6-6.4 2.8-7 7-.6-4.2-2.8-6.4-7-7 4.2-.6 6.4-2.8 7-7Z" />
          <path d="M19 15.5c.2 1.4 1 2.2 2.4 2.5-1.4.2-2.2 1-2.5 2.4-.2-1.4-1-2.2-2.4-2.5 1.4-.2 2.2-1 2.5-2.4Z" />
        </svg>
      );
    case "sun":
      return (
        <svg {...shared}>
          <circle cx="12" cy="12" r="4.2" />
          <path d="M12 2.8v2M12 19.2v2M4.5 4.5l1.4 1.4M18.1 18.1l1.4 1.4M2.8 12h2M19.2 12h2M4.5 19.5l1.4-1.4M18.1 5.9l1.4-1.4" />
        </svg>
      );
    case "menu":
      return (
        <svg {...shared}>
          <path d="M4 7h16M4 12h16M4 17h16" />
        </svg>
      );
    case "close":
      return (
        <svg {...shared}>
          <path d="m6 6 12 12M18 6 6 18" />
        </svg>
      );
    case "plus":
      return (
        <svg {...shared}>
          <path d="M12 5v14M5 12h14" />
        </svg>
      );
    case "check":
      return (
        <svg {...shared}>
          <path d="m5 12.5 4.3 4.3L19 7" />
        </svg>
      );
    case "chevron-down":
      return (
        <svg {...shared}>
          <path d="m6 9 6 6 6-6" />
        </svg>
      );
    case "chevron-up":
      return (
        <svg {...shared}>
          <path d="m6 15 6-6 6 6" />
        </svg>
      );
    case "music":
      return (
        <svg {...shared}>
          <path d="M9 18V5.5l10-2v12" />
          <circle cx="6.5" cy="18" r="2.5" />
          <circle cx="16.5" cy="15.5" r="2.5" />
        </svg>
      );
    case "clock":
      return (
        <svg {...shared}>
          <circle cx="12" cy="12" r="8.5" />
          <path d="M12 7.5V12l3 2" />
        </svg>
      );
    case "upload":
      return (
        <svg {...shared}>
          <path d="M12 16V4" />
          <path d="m7.5 8.5 4.5-4.5 4.5 4.5" />
          <path d="M4.5 16.5v2A1.5 1.5 0 0 0 6 20h12a1.5 1.5 0 0 0 1.5-1.5v-2" />
        </svg>
      );
    case "trash":
      return (
        <svg {...shared}>
          <path d="M4.5 7h15" />
          <path d="M9 7V5.2A1.2 1.2 0 0 1 10.2 4h3.6A1.2 1.2 0 0 1 15 5.2V7" />
          <path d="m6.5 7 1 12.1A1.5 1.5 0 0 0 9 20.5h6a1.5 1.5 0 0 0 1.5-1.4l1-12.1" />
        </svg>
      );
    case "pencil":
      return (
        <svg {...shared}>
          <path d="M4 20h4.3L20 8.3a2 2 0 0 0 0-2.8l-1.5-1.5a2 2 0 0 0-2.8 0L4 15.7V20Z" />
          <path d="m14 5.5 4.5 4.5" />
        </svg>
      );
    case "rotate":
      return (
        <svg {...shared}>
          <path d="M20 11a8 8 0 1 0-2.1 6.2" />
          <path d="M20 4.5V11h-6.5" />
        </svg>
      );
    case "alert":
      return (
        <svg {...shared}>
          <path d="M10.3 3.7 2.7 17a1.7 1.7 0 0 0 1.5 2.5h15.6a1.7 1.7 0 0 0 1.5-2.5L13.7 3.7a2 2 0 0 0-3.4 0Z" />
          <path d="M12 9v4.5" />
          <path d="M12 17h.01" />
        </svg>
      );
    case "copy":
      return (
        <svg {...shared}>
          <rect x="8.5" y="8.5" width="11" height="11" rx="2" />
          <path d="M15.5 8.5v-2A2 2 0 0 0 13.5 4.5h-7a2 2 0 0 0-2 2v7a2 2 0 0 0 2 2h2" />
        </svg>
      );
    case "stop":
      return (
        <svg {...shared} fill="currentColor" stroke="none">
          <rect x="6.5" y="6.5" width="11" height="11" rx="2.2" />
        </svg>
      );
    case "expand":
      return (
        <svg {...shared}>
          <path d="M9 4H4v5M15 4h5v5M9 20H4v-5M15 20h5v-5" />
        </svg>
      );
    case "info":
      return (
        <svg {...shared}>
          <circle cx="12" cy="12" r="8.5" />
          <path d="M12 11v5.5" />
          <path d="M12 7.6h.01" />
        </svg>
      );
    case "link":
      return (
        <svg {...shared}>
          <path d="M10 13.5a4 4 0 0 0 5.7 0l2.6-2.6a4 4 0 0 0-5.7-5.7L11 6.8" />
          <path d="M14 10.5a4 4 0 0 0-5.7 0l-2.6 2.6a4 4 0 0 0 5.7 5.7l1.6-1.6" />
        </svg>
      );
    case "wave":
      return (
        <svg {...shared}>
          <path d="M3 12h2.5M19.5 12H21" />
          <path d="M7 8v8M10 5v14M13 7v10M16 9v6" />
        </svg>
      );
    default:
      return null;
  }
}
