<script setup lang="ts">
import { ref } from 'vue'
const props = defineProps<{ text: string }>(); const copied = ref(false)
const copy = async () => { await navigator.clipboard.writeText(props.text); copied.value = true; setTimeout(() => copied.value = false, 1600) }
</script>
<template><button :aria-label="copied ? 'Copied' : 'Copy'" class="inline-flex min-h-11 items-center gap-2 rounded-lg border border-slate-300 bg-white px-3 text-sm font-medium text-slate-700 transition hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-slate-400" @click="copy">{{ copied ? 'Copied' : 'Copy' }}</button></template>
