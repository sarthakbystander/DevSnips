# Command Button

Keyboard-first trigger that opens a command palette and binds the Cmd/Ctrl-K shortcut.

## Usage

```jsx
<CommandButton onOpen={openPalette} />  // binds Cmd/Ctrl-K globally
```

## Props

`placeholder` · `shortcut` (default '⌘K') · `onOpen` · `variant` (outline|secondary) · `size` · `bindShortcut` (default true)

## Variants

outline (default) · secondary.

## Sizes

**md (default)**.

## States

default · hover · focus-visible.

## Accessibility

Renders a wide button with a search icon, placeholder, and a visible `kbd` shortcut. When `bindShortcut` is true, the global Cmd/Ctrl-K shortcut opens the palette. Focus ring present. The palette itself should trap focus and be labelled.

## Behavior

Opens a command palette. Surfaces the ⌘K shortcut visually and binds it globally so keyboard-first users can open it from anywhere.

## Design Tokens

Iconography (search), Typography (`body-md` placeholder, mono `kbd`), Sizing, Color, Motion.

## Notes

This is the trigger; pair it with a full palette component (dialog + filter + list). Show the platform-correct shortcut (⌘ on mac, Ctrl elsewhere).
