export function focusComposer() {
  const prompt = document.getElementById("prompt");
  if (!prompt) return;
  const reduced = window.matchMedia(
    "(prefers-reduced-motion: reduce)",
  ).matches;
  prompt.scrollIntoView({
    behavior: reduced ? "auto" : "smooth",
    block: "center",
  });
  window.setTimeout(() => prompt.focus(), reduced ? 0 : 280);
}
