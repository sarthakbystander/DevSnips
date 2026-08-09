<script setup lang="ts">
withDefaults(defineProps<{ label: string; size?: 'sm' | 'md' | 'lg'; disabled?: boolean }>(), { size: 'md', disabled: false })
</script>
<template><button :aria-label="label" :title="label" :disabled="disabled" :class="['inline-flex shrink-0 items-center justify-center rounded-lg border border-slate-300 bg-white text-slate-700 shadow-sm transition hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-slate-400 disabled:opacity-50', size === 'sm' ? 'h-9 w-9' : size === 'lg' ? 'h-12 w-12' : 'h-11 w-11']"><slot /></button></template>
