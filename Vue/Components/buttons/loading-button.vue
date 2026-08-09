<script setup lang="ts">
withDefaults(defineProps<{ loading?: boolean; disabled?: boolean }>(), { loading: false, disabled: false })
</script>
<template><button :disabled="loading || disabled" class="inline-flex min-h-11 items-center justify-center gap-2 rounded-lg bg-slate-900 px-4 text-sm font-medium text-white transition hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-slate-400 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-60"><span v-if="loading" class="h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white" aria-hidden="true" /><slot v-if="!loading" /><span v-else aria-live="polite">Loading…</span></button></template>
