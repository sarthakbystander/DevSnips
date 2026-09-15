# Neumorphism Button

Soft UI buttons with neumorphism (soft UI) shadow effects.

## Variants

| Variant | Description |
|---------|-------------|
| [Soft](./soft/) | Convex neumorphism with outer shadows |
| [Bordered](./bordered/) | Bordered neumorphism with gradient backgrounds |

## Quick Start

```html
<style>
  .neu-button {
    background: #e0e5ec;
    box-shadow: 8px 8px 16px #b8bec5, -8px -8px 16px #ffffff;
  }
  .neu-button:hover {
    box-shadow: 4px 4px 8px #b8bec5, -4px -4px 8px #ffffff;
  }
</style>

<button class="px-8 py-3 neu-button text-gray-600 font-semibold rounded-xl">
  Neumorphism
</button>
```

## Browser Support

Works in all modern browsers.

## Related

- [Glass Button](../Glass%20Button/) - Glass morphism style
- [Basic Button](../Basic%20Button/) - Core button styles
