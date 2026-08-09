<script setup lang="ts">
withDefaults(defineProps<{ modelValue?: boolean; label?: string; disabled?: boolean }>(), { modelValue: false, label: '', disabled: false })
const emit = defineEmits<{ 'update:modelValue': [value: boolean] }>()
</script>
<template><label class="flex min-h-11 cursor-pointer items-center gap-3 text-sm text-slate-700" :class="disabled && 'cursor-not-allowed opacity-50'"><input type="checkbox" :checked="modelValue" :disabled="disabled" class="h-5 w-5 rounded border-slate-300 accent-slate-900 focus:ring-2 focus:ring-slate-300" @change="emit('update:modelValue', ($event.target as HTMLInputElement).checked)"><span><slot>{{ label }}</slot></span></label></template>
