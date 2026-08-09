<script setup lang="ts">
withDefaults(defineProps<{ modelValue?: boolean; label?: string; disabled?: boolean }>(), { modelValue: false, label: '', disabled: false })
const emit = defineEmits<{ 'update:modelValue': [value: boolean] }>()
</script>
<template><button type="button" role="switch" :aria-checked="modelValue" :disabled="disabled" class="flex min-h-11 items-center gap-3 text-sm text-slate-700 disabled:opacity-50" @click="emit('update:modelValue', !modelValue)"><span :class="['relative h-6 w-11 rounded-full p-0.5 transition-colors', modelValue ? 'bg-slate-900' : 'bg-slate-300']"><span :class="['block h-5 w-5 rounded-full bg-white shadow-sm transition-transform', modelValue && 'translate-x-5']" /></span><slot>{{ label }}</slot></button></template>
