<script setup lang="ts">
withDefaults(defineProps<{ label?: string; blur?: boolean }>(), { label: 'Loading…', blur: true })
</script>
<template>
  <div class="absolute inset-0 z-10 grid place-items-center rounded-[inherit] bg-white/70 p-6 dark:bg-slate-950/70" :class="blur ? 'backdrop-blur-sm' : ''" role="status" aria-live="polite"><div class="flex items-center gap-3 rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm font-medium text-slate-800 shadow-sm dark:border-slate-800 dark:bg-slate-950 dark:text-slate-200"><span class="size-4 animate-spin rounded-full border-2 border-slate-300 border-t-slate-900 dark:border-slate-700 dark:border-t-white" aria-hidden="true" />{{ label }}</div></div>
</template>
