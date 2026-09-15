# Animated Button

Interactive button animations including loading states, hover effects, and transitions.

## Variants

| Variant | Description |
|---------|-------------|
| [Loading](./loading/) | Loading spinner animations |
| [Arrow](./arrow/) | Arrow slide animations |
| [Icon](./icon/) | Icon animations on hover |
| [Scale](./scale/) | Scale transformations |
| [Shine](./shine/) | Shine sweep effects |

## Quick Start

```html
<!-- Loading Button -->
<style>
  @keyframes spin { to { transform: rotate(360deg); } }
  .animate-spin-fast { animation: spin 1s linear infinite; }
</style>
<button class="px-6 py-2.5 bg-blue-600 text-white rounded-lg flex items-center gap-2" disabled>
  <svg class="w-5 h-5 animate-spin-fast" fill="none" viewBox="0 0 24 24">
    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
  </svg>
  Loading...
</button>
```

## Related

- [Basic Button](../Basic%20Button/) - Core button styles
- [Loading Button](../Loading%20Button/) - Dedicated loading components
