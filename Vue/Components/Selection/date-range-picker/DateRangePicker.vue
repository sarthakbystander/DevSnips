<script setup>
defineOptions({ name: 'DateRangePicker' })
withDefaults(defineProps({ start: String, end: String, disabled: Boolean }), {})
defineEmits(['update:start','update:end'])
</script>
<template><div class="grid w-full grid-cols-1 gap-2 sm:grid-cols-2"><input type="date" :value="start" :disabled="disabled" class="min-w-0 rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm outline-none focus:border-slate-900 focus:ring-4 focus:ring-slate-900/10 disabled:opacity-50 dark:border-slate-700 dark:bg-slate-950 dark:text-white" aria-label="Start date" @input="$emit('update:start',$event.target.value)"><input type="date" :value="end" :disabled="disabled" class="min-w-0 rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm outline-none focus:border-slate-900 focus:ring-4 focus:ring-slate-900/10 disabled:opacity-50 dark:border-slate-700 dark:bg-slate-950 dark:text-white" aria-label="End date" @input="$emit('update:end',$event.target.value)"></div></template>
