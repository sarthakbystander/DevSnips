<script setup lang="ts">
defineProps<{ label?: string }>()
const emit = defineEmits<{ close: [] }>()
</script>
<template><button :aria-label="label || 'Close'" class="inline-flex h-10 w-10 items-center justify-center rounded-full text-2xl leading-none text-slate-500 transition hover:bg-slate-100 hover:text-slate-900 focus:outline-none focus:ring-2 focus:ring-slate-400" @click="emit('close')"><span aria-hidden="true">×</span></button></template>
