# Input Components

A comprehensive collection of **35 Tailwind CSS input components** for modern web applications.

## 🎯 Overview

This component family covers every input type and style you need for building production-ready forms, from simple text inputs to complex date pickers and color selectors.

## 📦 Components

| # | Component | Description |
|---|-----------|-------------|
| 1 | [Underline](./underline/) | Minimal underline style with focus animation |
| 2 | [Outlined](./outlined/) | Classic bordered style with label |
| 3 | [Filled](./filled/) | Filled background style |
| 4 | [Floating Label](./floating-label/) | Animated floating label input |
| 5 | [Icon Left](./icon-left/) | Left-aligned icon input |
| 9 | [With Prefix](./with-prefix/) | Text prefix (e.g., $) |
| 10 | [With Suffix](./with-suffix/) | Text suffix (e.g., .com) |
| 11 | [Password Toggle](./password-toggle/) | Password with show/hide |
| 12 | [Textarea](./textarea/) | Multi-line text input |
| 13 | [Character Count](./character-count/) | Input with counter |
| 14 | [Validation States](./validation-states/) | Success/error/warning states |
| 15 | [With Helper Text](./with-helper/) | Helper/error messages |
| 16 | [Disabled Readonly](./disabled-readonly/) | Disabled and readonly |
| 19 | [Gradient Border](./gradient-border/) | Gradient border effect |
| 20 | [Glassmorphism](./glassmorphism/) | Frosted glass effect |
| 21 | [Neumorphism](./neumorphism/) | Soft UI shadow style |
| 22 | [Dark Mode](./dark-mode/) | Dark background inputs |
| 25 | [Animated Focus](./animated-focus/) | Smooth focus transitions |
| 26 | [Split Input](./split-input/) | Multi-part inputs (OTP, cards) |
| 27 | [Tag Input](./tag-input/) | Tag/chip functionality |
| 28 | [Number Stepper](./number-stepper/) | Increment/decrement buttons |
| 29 | [Date Picker](./date-picker/) | Date selection components |
| 30 | [File Upload](./file-upload/) | Drag-drop and preview |
| 31 | [Color Picker](./color-picker/) | Color selection swatches |
| 32 | [Range Slider](./range-slider/) | Numeric range selection |
| 33 | [Checkbox Styled](./checkbox-styled/) | Custom checkbox designs |
| 34 | [Toggle Switch](./toggle-switch/) | Boolean toggle controls |
| 35 | [Radio Styled](./radio-styled/) | Custom radio buttons |

## ✨ Features

- **35 Production-Ready Components** - Each variant is fully functional
- **Responsive Design** - Mobile-first approach
- **Dark Mode Support** - Most components work in dark themes
- **Accessibility** - Proper focus states and ARIA attributes
- **Zero JavaScript** - Pure CSS (except where interaction is needed)
- **Copy & Paste** - Clean, semantic code ready for production

## 🎨 Design Variants

| Category | Examples |
|----------|----------|
| **Layout** | Underline, Outlined, Filled, Sharp Corner, Rounded Pill |
| **Visual Style** | Gradient Border, Glassmorphism, Neumorphism, Dark Mode |
| **Corporate** | Corporate, Modern SaaS, Enterprise Forms |
| **Interactive** | Floating Label, Animated Focus, Password Toggle |
| **Complex** | Split Input, Tag Input, Number Stepper, File Upload |
| **Selection** | Color Picker, Range Slider, Checkbox, Toggle, Radio |

## 🚀 Quick Start

```html
<!-- Using the code.html file -->
<input type="text" class="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
```

## 📁 File Structure

```
Input/
├── README.md
├── underline/
│   ├── code.html
│   ├── preview.html
│   └── metadata.json
├── outlined/
│   └── ...
└── ... (33 more components)
```

## 🔧 Customization

All components use standard Tailwind CSS utility classes. To customize:

1. **Colors**: Replace `blue-*` with your brand colors (e.g., `indigo-*`, `emerald-*`)
2. **Sizes**: Adjust `px-*`, `py-*`, `text-*` classes
3. **Borders**: Modify `border-*` and `rounded-*` classes
4. **Focus**: Customize `focus:ring-*` and `focus:border-*` states

## 📱 Responsive Design

All components are responsive by default:
- Mobile-first approach
- Touch-friendly sizing
- Clear focus states for keyboard navigation

## ♿ Accessibility

- Clear focus indicators on all interactive elements
- Proper label associations
- Sufficient color contrast
- Touch-friendly sizes (minimum 44px)

## 📄 License

Part of the DevSnips component library. Free for personal and commercial use.
