<script setup lang="ts">
withDefaults(defineProps<{ modelValue?: string; label?: string; placeholder?: string; rows?: number }>(), { modelValue: '', label: '', placeholder: '', rows: 4 })
const emit = defineEmits<{ 'update:modelValue': [value: string] }>()
</script>
<template><label class="grid gap-2 text-sm font-medium text-slate-800"><span v-if="label">{{ label }}</span><textarea :value="modelValue" :rows="rows" :placeholder="placeholder" class="w-full resize-y rounded-lg border border-slate-300 bg-white px-3.5 py-3 text-base outline-none transition placeholder:text-slate-400 focus:border-slate-900 focus:ring-2 focus:ring-slate-200 sm:text-sm" @input="emit('update:modelValue', ($event.target as HTMLTextAreaElement).value)" /></label></template>
