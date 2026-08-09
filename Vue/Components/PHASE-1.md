# Vue Phase 1 — Foundation

Phase 1 establishes the core DevSnips Vue 3 UI language across **40 production-oriented components**.

## Design language

- Minimal visual system with restrained borders, soft surfaces, and compact typography.
- Mobile-first and adaptive rather than simply scaled-down desktop layouts.
- Touch targets are designed around comfortable interaction on small screens.
- Visible keyboard focus states and semantic HTML are used throughout.
- Components support light and dark surfaces through Tailwind utility classes.
- APIs use Vue 3 `<script setup>`, props, emits, and controlled `v-model` patterns where state belongs to the consumer.
- Avoid unnecessary runtime dependencies.

## Phase 1 families

### Buttons & Actions
Button, Icon Button, Button Group, Loading Button, Link Button, Split Button, Close Button, Copy Button, Download Button, Floating Action Button.

### Forms & Inputs
Input, Textarea, Search Input, Number Input, Password Input, OTP Input, Checkbox, Radio Group, Switch, Slider.

### Selection
Select, Multi Select, Combobox, Autocomplete, Date Picker, Time Picker, Date Range Picker, Segmented Control, Tags Input, Color Picker.

### Navigation
Navbar, Sidebar, Mobile Navigation, Breadcrumbs, Tabs, Pagination, Stepper, Menu, Dropdown Menu, Command Menu.

## Responsive rule

Every component must have an intentional small-screen behavior. Navigation collapses or becomes scrollable, multi-column controls stack, dense controls remain touch-friendly, and overlays use viewport-aware sizing.
