# Tabs (Disabled)

Tabs with disabled entries that cannot activate, stay out of the tab order, and are skipped by arrow keys.

## Usage

```tsx
<Tabs defaultValue="activity">
  <TabsList aria-label="Workspace navigation">
    <TabsTrigger value="overview">Overview</TabsTrigger>
    <TabsTrigger value="activity">Activity</TabsTrigger>
    <TabsTrigger value="settings" disabled>Settings</TabsTrigger>
    <TabsTrigger value="billing" disabled>Billing</TabsTrigger>
  </TabsList>
  …
</Tabs>
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
<Tabs defaultValue="activity">
  <TabsList aria-label="Workspace navigation">
    <TabsTrigger value="overview">Overview</TabsTrigger>
    <TabsTrigger value="activity">Activity</TabsTrigger>
    <TabsTrigger value="settings" disabled>Settings</TabsTrigger>
    <TabsTrigger value="billing" disabled>Billing</TabsTrigger>
  </TabsList>
  …
</Tabs>
```

## Props

### `<Tabs>`

| Name | Type | Default | Description |
|---|---|---|---|
| `value` | `string` | — | Selected tab value (controlled). |
| `defaultValue` | `string` | — | Initial selected value (uncontrolled). |
| `onValueChange` | `(value: string) => void` | — | Selection callback. |
| `orientation` | `"horizontal" \| "vertical"` | `"horizontal"` | Arrow-key navigation axis + layout. |
| `className` | `string` | — | Extra classes on the root. |
| `children` | `ReactNode` | — | `TabsList` + `TabsContent` composition. |

### `<TabsList>`

| Name | Type | Default | Description |
|---|---|---|---|
| `aria-label` | `string` | — | Group label for the tablist (recommended). |
| `className` | `string` | — | Extra classes on the tablist. |
| `children` | `ReactNode` | — | `TabsTrigger` elements. |

### `<TabsTrigger>`

| Name | Type | Default | Description |
|---|---|---|---|
| `value` | `string` (required) | — | Value this trigger selects; associates it with its panel. |
| `icon` | `ReactNode` | — | Meaningful leading icon (rendered `aria-hidden`). |
| `badge` | `ReactNode` | — | Small contextual chip after the label. |
| `count` | `number` | — | Numeric chip after the label. |
| `disabled` | `boolean` | `false` | Prevents activation; skipped by key navigation. |
| `className` | `string` | — | Extra classes on the trigger. |
| `children` | `ReactNode` | — | Visible label. |

### `<TabsContent>`

| Name | Type | Default | Description |
|---|---|---|---|
| `value` | `string` (required) | — | Matches the owning `TabsTrigger`. |
| `className` | `string` | — | Extra classes on the panel. |
| `children` | `ReactNode` | — | Panel content. |

## Composition

Tabs is a compound component. Four primitives compose the pattern:

```tsx
<Tabs defaultValue="overview">
  <TabsList aria-label="Project navigation">
    <TabsTrigger value="overview">Overview</TabsTrigger>
    <TabsTrigger value="activity">Activity</TabsTrigger>
  </TabsList>
  <TabsContent value="overview">…</TabsContent>
  <TabsContent value="activity">…</TabsContent>
</Tabs>
```

- `Tabs` — the root provider. Owns the selected value (controlled via `value` + `onValueChange`, uncontrolled via `defaultValue`) and the `orientation` (`"horizontal"` | `"vertical"`).
- `TabsList` — renders `role="tablist"` and owns arrow-key / Home / End navigation with automatic activation.
- `TabsTrigger` — renders a native `<button role="tab">` with roving `tabIndex`, plus the optional `icon` / `badge` / `count` content props.
- `TabsContent` — renders the `role="tabpanel"`. Every panel stays mounted; inactive panels carry the `hidden` attribute, so form and input state inside a panel is preserved.

Mark entries with `disabled` — the trigger renders a native disabled `<button>` and the arrow-key handler filters it out of the navigation set.

## Keyboard Interaction

| Key | Horizontal tabs | Vertical tabs |
|---|---|---|
| `ArrowRight` | Move focus + activate the next tab | — |
| `ArrowLeft` | Move focus + activate the previous tab | — |
| `ArrowDown` | — | Move focus + activate the next tab |
| `ArrowUp` | — | Move focus + activate the previous tab |
| `Home` | Activate the first tab | Activate the first tab |
| `End` | Activate the last tab | Activate the last tab |

Navigation wraps around the ends. Automatic activation is used: focus and selection move together through the tablist. Disabled tabs are skipped by arrow keys and removed from the tab order. Only the selected tab sits in the tab order (roving `tabIndex`).

## Accessibility

The structure follows the W3C Tabs pattern: one `role="tablist"` containing native `<button role="tab">` triggers, with `role="tabpanel"` content regions.

- Trigger → panel association: `aria-controls` points at the panel id; the panel answers with `aria-labelledby` pointing back at the trigger id.
- `aria-selected` mirrors the current selection on every trigger.
- Panels stay focusable (`tabIndex={0}`) so keyboard users can read into scrollable content.

Native `disabled` <button> semantics — screen readers announce the tab as unavailable. Arrow keys filter it out, so there is no dead stop while navigating.

## States

- **Disabled** — `disabled:opacity-50` + `pointer-events-none`; cannot be activated.
- Keyboard navigation skips disabled entries entirely.
- Native `disabled` also removes the tab from the tab order (it never receives focus).

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-surface-active)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. This tabs variant uses the semantic color, radius, spacing, and motion tokens.

## Notes

Pair disabled with a real reason (e.g. an admin-only section). If every sibling is disabled, provide context elsewhere on the page.
