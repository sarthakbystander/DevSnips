# Loading Button

Buttons with loading states, spinners, and progress indicators.

## Variants

| Variant | Description |
|---------|-------------|
| [Spinner](./spinner/) | Loading buttons with spinner animations |
| [Progress](./progress/) | Loading buttons with progress bar |

## Quick Start

```html
<style>
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
  .animate-spin {
    animation: spin 1s linear infinite;
  }
</style>

<button class="px-6 py-2.5 bg-blue-600 text-white rounded-lg flex items-center gap-2 cursor-wait" disabled>
  <svg class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
  </svg>
  Loading
</button>
```

## Related

- [Animated Button](../Animated%20Button/) - General animations
- [Basic Button](../Basic%20Button/) - Core button styles
