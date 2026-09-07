# Gradient Button

A collection of gradient button components with various styles and effects.

## Variants

| Variant | Description |
|---------|-------------|
| [Linear](./linear/) | Two-color horizontal gradient buttons |
| [Shadow](./shadow/) | Gradient buttons with colored shadows |

## Quick Start

```html
<!-- Basic Linear Gradient -->
<button class="px-6 py-2.5 bg-gradient-to-r from-blue-500 to-blue-600 text-white font-medium rounded-lg hover:opacity-90 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">
  Click Me
</button>
```

## Gradient Directions

| Class | Direction |
|-------|-----------|
| `bg-gradient-to-r` | Left → Right |
| `bg-gradient-to-l` | Right → Left |
| `bg-gradient-to-t` | Bottom → Top |
| `bg-gradient-to-b` | Top → Bottom |
| `bg-gradient-to-tr` | Bottom Left → Top Right |
| `bg-gradient-to-tl` | Bottom Right → Top Left |
| `bg-gradient-to-br` | Top Left → Bottom Right |
| `bg-gradient-to-bl` | Top Right → Bottom Left |

## Accessibility

- All buttons include visible focus rings
- Use `disabled` attribute for disabled state
- Minimum touch target: 44×44px
- Ensure sufficient color contrast

## Customization

### Custom Colors

```html
<button class="bg-gradient-to-r from-[#your-color] to-[#your-color]">
```

### Custom Shadow Colors

```html
<button class="shadow-lg shadow-[color]/[opacity]">
```

## Related

- [Glass Button](../Glass%20Button/) - Frosted glass effect
- [Animated Button](../Animated%20Button/) - Hover animations
- [Icon Button](../Icon%20Button/) - Icon + text combinations
