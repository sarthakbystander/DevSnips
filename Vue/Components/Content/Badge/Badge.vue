<script setup lang="ts">
withDefaults(defineProps<{ tone?: 'neutral'|'success'|'warning'|'danger'; dot?: boolean }>(), { tone: 'neutral', dot: false })
</script>
<template><span :class="['inline-flex max-w-full items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-medium', tone === 'success' ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300' : tone === 'warning' ? 'bg-amber-50 text-amber-700 dark:bg-amber-950/40 dark:text-amber-300' : tone === 'danger' ? 'bg-red-50 text-red-700 dark:bg-red-950/40 dark:text-red-300' : 'bg-slate-100 text-slate-700 dark:bg-slate-900 dark:text-slate-300']"><i v-if="dot" class="size-1.5 rounded-full bg-current" aria-hidden="true" /><slot /></span></template>
