# 3D Button

Buttons with 3D depth effects and push animations.

## Variants

| Variant | Description |
|---------|-------------|
| [Colored](./colored/) | Colored 3D buttons with gradients |

## Quick Start

```html
<style>
  .btn-3d {
    position: relative;
    box-shadow: 0 6px 0 #1d4ed8;
    transition: all 0.1s;
  }
  .btn-3d:active {
    transform: translateY(4px);
    box-shadow: 0 2px 0 #1d4ed8;
  }
</style>

<button class="px-8 py-3 btn-3d bg-blue-600 text-white font-bold rounded-lg hover:bg-blue-700">
  3D Button
</button>

<!-- Or with Tailwind shadow extensions -->
<button class="px-8 py-3 bg-blue-600 text-white font-bold rounded-lg shadow-[0_6px_0_#1d4ed8] hover:shadow-[0_4px_0_#1d4ed8] active:translate-y-[4px] active:shadow-[0_2px_0_#1d4ed8]">
  3D Button
</button>
```

## Related

- [Basic Button](../Basic%20Button/) - Core button styles
- [Animated Button](../Animated%20Button/) - General animations
