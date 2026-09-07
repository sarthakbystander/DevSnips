# Glass Button

Glass morphism buttons with backdrop blur effects.

## Variants

| Variant | Description |
|---------|-------------|
| [Soft](./soft/) | Light glass buttons with subtle blur |
| [Icon](./icon/) | Glass icon buttons |

## Quick Start

```html
<style>
  .glass-button {
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.3);
  }
</style>

<button class="px-6 py-2.5 glass-button text-gray-700 font-medium rounded-lg hover:bg-white/90 focus:outline-none focus:ring-2 focus:ring-white/50 transition-all">
  Glass Button
</button>
```

## Browser Support

- `backdrop-filter` requires webkit prefix for Safari
- Fallback: semi-transparent background without blur

## Related

- [Basic Button](../Basic%20Button/) - Core button styles
- [Neumorphism Button](../Neumorphism%20Button/) - Soft UI style
