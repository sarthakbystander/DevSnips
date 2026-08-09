<script setup>
defineOptions({ name: 'Tabs' })
defineProps({ modelValue: [String, Number], tabs: { type: Array, default: () => [] } })
defineEmits(['update:modelValue'])
</script>
<template><div class="w-full overflow-x-auto border-b border-slate-200 dark:border-slate-800"><div class="flex min-w-max gap-1" role="tablist"><button v-for="tab in tabs" :key="tab.value" type="button" role="tab" :aria-selected="modelValue===tab.value" class="border-b-2 px-4 py-3 text-sm font-medium transition" :class="modelValue===tab.value?'border-slate-950 text-slate-950 dark:border-white dark:text-white':'border-transparent text-slate-500 hover:text-slate-900 dark:hover:text-white'" @click="$emit('update:modelValue',tab.value)">{{ tab.label }}</button></div></div></template>
