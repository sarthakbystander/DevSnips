<script setup lang="ts">
withDefaults(defineProps<{ removable?: boolean }>(), { removable: false })
const emit = defineEmits<{ remove: [] }>()
</script>
<template><span class="inline-flex max-w-full items-center gap-1 rounded-lg border border-slate-200 bg-white px-2.5 py-1 text-xs font-medium text-slate-700 dark:border-slate-800 dark:bg-slate-950 dark:text-slate-300"><span class="truncate"><slot /></span><button v-if="removable" type="button" aria-label="Remove" class="rounded p-0.5 text-slate-400 hover:bg-slate-100 hover:text-slate-900 focus:outline-none focus:ring-2 focus:ring-slate-400 dark:hover:bg-slate-900 dark:hover:text-white" @click="emit('remove')">×</button></span></template>
