<script setup lang="ts">
withDefaults(defineProps<{
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
}>(), { variant: 'primary', size: 'md', disabled: false })
</script>

<template>
  <button :disabled="disabled" :class="['inline-flex min-h-11 items-center justify-center rounded-lg border px-4 font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-slate-400 focus:ring-offset-2 disabled:pointer-events-none disabled:opacity-50', { 'border-slate-900 bg-slate-900 text-white hover:bg-slate-800': variant === 'primary', 'border-slate-300 bg-white text-slate-900 hover:bg-slate-50': variant === 'secondary', 'border-transparent bg-transparent text-slate-700 hover:bg-slate-100': variant === 'ghost', 'border-red-600 bg-red-600 text-white hover:bg-red-700': variant === 'danger', 'h-9 px-3 text-sm': size === 'sm', 'h-11 text-sm': size === 'md', 'h-12 px-5 text-base': size === 'lg' }]">
    <slot />
  </button>
</template>
