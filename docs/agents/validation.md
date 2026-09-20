# Agent validation

Validation proves the integration works. There are two layers: verifying the installation (file-based, mandatory) and verifying the result in the host project (behavior-based, depends on what the project provides).

## Layer 1 — Installation verification (mandatory)

Covered in detail in [Installation](installation.md). Summary of the contract:

1. Command exited 0.
2. Destination directory `./devsnips/<tech>/<category>/<family>/<variant>/` exists.
3. Expected files exist (registry `files` manifest minus `metadata.json`/`preview.html`).
4. Files match the *requested* resource (check slug/family/variant, not a sibling).
5. No unexpected files.

A failed check anywhere means the installation failed. Never proceed to adaptation on an unverified install, and never report an installation as successful based on a previous, different install.

## Layer 2 — Integration verification

Run everything the host project provides; fall back to manual verification where it does not.

| Project provides | Verify with |
|---|---|
| Build / typecheck | `build`, `tsc --noEmit`, or the project's equivalent — must pass with the resource integrated. |
| Tests | Run the relevant suite. |
| Dev server | Load the page containing the resource; check the console for errors. |
| Nothing (static project) | Open the page directly in a browser and check rendering, console, and interactions manually. |

Then verify the resource's declared behavior against its metadata/README:

- **Interaction model** — e.g. single-open vs multi-open accordion behavior still works; dropdowns open/close on the intended triggers; Escape and outside-click still close overlays.
- **Keyboard and focus** — every interactive control is reachable and operable by keyboard; focus indicators are visible (`focus-visible` rings survive any token swap or reset).
- **Accessibility semantics** — native elements retained (`<button>` stays a button), accessible names present, `aria-*` state wiring intact, status messages still announced.
- **Responsive behavior** — usable at mobile widths, no horizontal overflow, touch targets usable.
- **Reduced motion** — animations respect `prefers-reduced-motion`.
- **Dark mode** — if the resource declares `darkMode: true`, verify the dark treatment under the project's theming.

A practical checklist is shipped with the skill: `agents/skills/devsnips/references/accessibility_responsive_checklist.md`. Use it during adaptation and validation; report only what was actually checked.

## Reporting

After validation, report only the relevant outcome:

- which DevSnips resource(s) were used, and where they were integrated;
- important adaptations made;
- verification performed (which checks, observed results);
- any limitation that remains.

Rules:

- Do not claim DevSnips was used when the implementation was built from scratch.
- Do not report inventory statistics unless read from the current registry in this session.
- Do not claim success for a failed installation, failed build, unresolved import, or unverified integration.

## Anti-patterns

- Reporting installation success without the file checks.
- Verifying the isolated preview instead of the integrated page.
- Treating a build warning introduced by the adaptation as out of scope.
- Skipping accessibility verification because "it was already accessible" — the *adapted* state is what ships.
