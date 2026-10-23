import type { CSSProperties } from "react";

interface SliderProps {
  value: number;
  max: number;
  min?: number;
  step?: number;
  onChange: (value: number) => void;
  label: string;
  valueText?: string;
  disabled?: boolean;
  dark?: boolean;
  className?: string;
}

export function Slider({
  value,
  max,
  min = 0,
  step = 0.01,
  onChange,
  label,
  valueText,
  disabled = false,
  dark = false,
  className = "",
}: SliderProps) {
  const safeMax = max > min ? max : min + 1;
  const progress = Math.min(
    100,
    Math.max(0, ((value - min) / (safeMax - min)) * 100),
  );

  return (
    <input
      type="range"
      min={min}
      max={safeMax}
      step={step}
      value={Number.isFinite(value) ? value : min}
      onChange={(event) => onChange(Number(event.target.value))}
      aria-label={label}
      aria-valuetext={valueText}
      disabled={disabled}
      className={`ds-range ${dark ? "on-dark" : ""} ${className}`}
      style={{ "--range-progress": `${progress}%` } as CSSProperties}
    />
  );
}
