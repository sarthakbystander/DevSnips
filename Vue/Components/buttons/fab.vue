<script setup lang="ts">
withDefaults(defineProps<{ label?: string; position?: 'bottom-right' | 'bottom-left' }>(), { label: 'Create', position: 'bottom-right' })
</script>
<template><button :aria-label="label" :class="['fixed bottom-5 z-40 inline-flex h-14 w-14 items-center justify-center rounded-full bg-slate-900 text-xl text-white shadow-lg transition hover:-translate-y-0.5 hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-slate-400 sm:bottom-6 sm:h-12 sm:w-12', position === 'bottom-left' ? 'left-5 sm:left-6' : 'right-5 sm:right-6']"><slot>+</slot></button></template>
