<script setup lang="ts">
withDefaults(defineProps<{ modelValue?: number; min?: number; max?: number; step?: number; showValue?: boolean }>(), { modelValue: 50, min: 0, max: 100, step: 1, showValue: true })
const emit = defineEmits<{ 'update:modelValue': [value: number] }>()
</script>
<template><div class="w-full min-w-0"><div v-if="showValue" class="mb-2 flex items-center justify-between text-xs font-medium text-slate-600"><span>Value</span><output>{{ modelValue }}</output></div><input type="range" :value="modelValue" :min="min" :max="max" :step="step" class="h-2 w-full cursor-pointer accent-slate-900" @input="emit('update:modelValue', Number(($event.target as HTMLInputElement).value))" /></div></template>
