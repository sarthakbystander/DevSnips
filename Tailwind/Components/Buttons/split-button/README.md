# Split Button

Button components with dropdown or icon triggers for additional actions.

## Variants

| Variant | Description |
|---------|-------------|
| [Icon](./icon/) | Split buttons with icon |
| [Dropdown](./dropdown/) | Split buttons with dropdown trigger |

## Quick Start

```html
<div class="inline-flex rounded-md shadow-sm" role="group">
  <button class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-l-lg hover:bg-blue-700 focus:z-10 focus:ring-2 focus:ring-blue-500">
    Action
  </button>
  <button class="px-2 py-2 text-sm font-medium text-white bg-blue-600 border-l border-blue-700 rounded-r-lg hover:bg-blue-700 focus:z-10 focus:ring-2 focus:ring-blue-500">
    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
    </svg>
  </button>
</div>
```

## Related

- [Basic Button](../Basic%20Button/) - Core button styles
- [Icon Button](../Icon%20Button/) - Icon-only buttons
