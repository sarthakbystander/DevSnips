<script setup lang="ts">
withDefaults(defineProps<{ modelValue?: string; placeholder?: string }>(), { modelValue: '', placeholder: 'Search…' })
const emit = defineEmits<{ 'update:modelValue': [value: string] }>()
</script>
<template><div class="relative w-full max-w-md"><span class="pointer-events-none absolute inset-y-0 left-3 flex items-center text-slate-400" aria-hidden="true">⌕</span><input :value="modelValue" type="search" :placeholder="placeholder" class="min-h-11 w-full rounded-lg border border-slate-300 bg-white pl-9 pr-3.5 text-base outline-none focus:border-slate-900 focus:ring-2 focus:ring-slate-200 sm:text-sm" @input="emit('update:modelValue', ($event.target as HTMLInputElement).value)" /></div></template>
