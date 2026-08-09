<script setup lang="ts">
withDefaults(defineProps<{ label?: string; value?: string | number; change?: string }>(), {})
</script>
<template><article class="min-w-0 rounded-2xl border border-slate-200 bg-white p-5 dark:border-slate-800 dark:bg-slate-950"><p class="text-sm text-slate-500 dark:text-slate-400">{{ label }}</p><div class="mt-2 flex flex-wrap items-baseline gap-2"><strong class="text-2xl font-semibold tracking-tight text-slate-950 dark:text-white">{{ value }}</strong><span v-if="change" class="text-xs font-medium text-slate-500 dark:text-slate-400">{{ change }}</span></div><slot /></article></template>
