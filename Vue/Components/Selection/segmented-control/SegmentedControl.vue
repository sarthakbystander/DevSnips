<script setup>
defineOptions({ name: 'SegmentedControl' })
defineProps({ modelValue: [String, Number], options: { type: Array, default: () => [] } })
defineEmits(['update:modelValue'])
</script>
<template><div class="grid w-full grid-cols-2 gap-1 rounded-xl bg-slate-100 p-1 sm:flex dark:bg-slate-800"><button v-for="option in options" :key="option.value ?? option" type="button" class="min-h-10 flex-1 rounded-lg px-3 py-2 text-sm font-medium transition" :class="modelValue === (option.value ?? option) ? 'bg-white text-slate-900 shadow-sm dark:bg-slate-950 dark:text-white' : 'text-slate-500 hover:text-slate-900 dark:hover:text-white'" @click="$emit('update:modelValue',option.value ?? option)">{{ option.label ?? option }}</button></div></template>
