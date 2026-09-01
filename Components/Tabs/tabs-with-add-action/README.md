# Tabs With Add Action

Tabs plus a separate add action rendered outside the tablist with a required accessible label.

## Usage

```tsx
<Tabs defaultValue="projects">
  <div className="flex items-start gap-2">
    <TabsList aria-label="Workspace views">
      <TabsTrigger value="projects">Projects</TabsTrigger>
      <TabsTrigger value="archived">Archived</TabsTrigger>
    </TabsList>
    <TabsAddAction aria-label="Add a project" onClick={addProject} />
  </div>
  <TabsContent value="projects">…</TabsContent>
  <TabsContent value="archived">…</TabsContent>
</Tabs>
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
<Tabs defaultValue="projects">
  <div className="flex items-start gap-2">
    <TabsList aria-label="Workspace views">
      <TabsTrigger value="projects">Projects</TabsTrigger>
      <TabsTrigger value="archived">Archived</TabsTrigger>
    </TabsList>
    <TabsAddAction aria-label="Add a project" onClick={addProject} />
  </div>
  <TabsContent value="projects">…</TabsContent>
  <TabsContent value="archived">…</TabsContent>
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

### `<TabsAddAction>`

| Name | Type | Default | Description |
|---|---|---|---|
| `aria-label` | `string` (required) | — | Accessible name for the action. |
| `onClick` | `(event) => void` | — | Click callback. |
| `disabled` | `boolean` | `false` | Disables the action. |
| `className` | `string` | — | Extra classes on the button. |
| `children` | `ReactNode` | — | Custom icon/content (defaults to the built-in plus icon). |

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

`TabsAddAction` is a plain button rendered next to the tablist inside a flex row — it is not part of the tablist, so Arrow keys never land on it and its `aria-label` is required by the type.

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

The button requires an `aria-label` (enforced by the prop type) because it is icon-only. It is reachable by normal Tab focus without entering the tablist's arrow-key interaction.

## States

- The add action is a real `<button>` outside `role="tablist"` — tab semantics are untouched.
- It shares the trigger's 36px height, radius, border, and focus ring, so the row reads as one system.
- In the demo, clicking it appends a new tab and selects it.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-surface-active)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. This tabs variant uses the semantic color, radius, spacing, and motion tokens.

## Notes

Compose the row with flexbox so the add action sits beside the list, as in the usage example. Disable it with `disabled` like any other control.
