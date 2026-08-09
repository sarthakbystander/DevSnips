<script setup>
defineOptions({ name: 'DatePicker' })
defineProps({ modelValue: String, min: String, max: String, disabled: Boolean })
defineEmits(['update:modelValue'])
</script>
<template><input type="date" :value="modelValue" :min="min" :max="max" :disabled="disabled" class="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-slate-900 focus:ring-4 focus:ring-slate-900/10 disabled:opacity-50 dark:border-slate-700 dark:bg-slate-950 dark:text-white" @input="$emit('update:modelValue',$event.target.value)"></template>
