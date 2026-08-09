<script setup lang="ts">
withDefaults(defineProps<{ modelValue?: number | null; min?: number; max?: number; step?: number }>(), { modelValue: null, min: undefined, max: undefined, step: 1 })
const emit = defineEmits<{ 'update:modelValue': [value: number | null] }>()
</script>
<template><input :value="modelValue ?? ''" type="number" :min="min" :max="max" :step="step" class="min-h-11 w-full rounded-lg border border-slate-300 bg-white px-3.5 text-base outline-none focus:border-slate-900 focus:ring-2 focus:ring-slate-200 sm:text-sm" @input="emit('update:modelValue', ($event.target as HTMLInputElement).value === '' ? null : Number(($event.target as HTMLInputElement).value))" /></template>
