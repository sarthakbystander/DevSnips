<script setup>
defineOptions({ name: 'Select' })
withDefaults(defineProps({ modelValue: [String, Number], options: { type: Array, default: () => [] }, placeholder: { type: String, default: 'Select an option' }, disabled: Boolean }), {})
defineEmits(['update:modelValue'])
</script>
<template><select :value="modelValue" :disabled="disabled" class="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-slate-900 focus:ring-4 focus:ring-slate-900/10 disabled:cursor-not-allowed disabled:opacity-50 dark:border-slate-700 dark:bg-slate-950 dark:text-white" @change="$emit('update:modelValue', $event.target.value)"><option value="" disabled>{{ placeholder }}</option><option v-for="option in options" :key="option.value ?? option" :value="option.value ?? option">{{ option.label ?? option }}</option></select></template>
