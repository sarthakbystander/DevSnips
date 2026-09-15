# Floating Action Button

Floating action buttons (FAB) for primary actions.

## Variants

| Variant | Description |
|---------|-------------|
| [Standard](./standard/) | Standard circular FABs |
| [Extended](./extended/) | FAB with icon and text |
| [Group](./group/) | Grouped FABs for multiple actions |

## Quick Start

```html
<!-- Standard FAB -->
<button class="p-4 bg-blue-600 text-white rounded-full shadow-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all">
  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
  </svg>
</button>

<!-- Extended FAB -->
<button class="flex items-center gap-2 px-5 py-3 bg-blue-600 text-white font-medium rounded-full shadow-lg hover:bg-blue-700">
  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
  </svg>
  <span>Create</span>
</button>
```

## Related

- [Icon Button](../Icon%20Button/) - Icon-only buttons
- [Animated Button](../Animated%20Button/) - Animated buttons
