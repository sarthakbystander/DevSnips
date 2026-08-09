<script setup>
defineOptions({ name: 'ColorPicker' })
defineProps({ modelValue: { type: String, default: '#111827' }, disabled: Boolean })
defineEmits(['update:modelValue'])
</script>
<template><label class="inline-flex h-12 w-full cursor-pointer items-center gap-3 rounded-xl border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950"><input type="color" :value="modelValue" :disabled="disabled" class="h-8 w-8 cursor-pointer rounded-lg border-0 bg-transparent p-0" @input="$emit('update:modelValue',$event.target.value)"><span class="font-mono text-slate-700 dark:text-slate-300">{{ modelValue }}</span></label></template>
