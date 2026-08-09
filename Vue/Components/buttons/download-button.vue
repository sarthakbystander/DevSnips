<script setup lang="ts">
defineProps<{ href: string; filename?: string }>()
</script>
<template><a :href="href" :download="filename" class="inline-flex min-h-11 items-center justify-center rounded-lg border border-slate-900 bg-slate-900 px-4 text-sm font-medium text-white transition hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-slate-400 focus:ring-offset-2"><slot>Download</slot></a></template>
