# Icon Button

Icon-only buttons and icon+text combinations for toolbars and navigation.

## Variants

| Variant | Description |
|---------|-------------|
| [Basic](./basic/) | Basic icon button styles |
| [Rounded](./rounded/) | Fully rounded circular icon buttons |
| [Dark](./dark/) | Dark themed icon buttons |

## Quick Start

```html
<!-- Basic Icon Button -->
<button class="p-2.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500" aria-label="Home">
  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
  </svg>
</button>
```

## Accessibility

- Always include `aria-label` for icon-only buttons
- Minimum touch target: 44×44px

## Related

- [Animated Button](../Animated%20Button/) - Animated icon buttons
- [Split Button](../Split%20Button/) - Button with dropdown
