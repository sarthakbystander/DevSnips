<script setup>
defineOptions({ name: 'Pagination' })
defineProps({ modelValue: { type: Number, default: 1 }, total: { type: Number, default: 1 }, siblingCount: { type: Number, default: 1 } })
defineEmits(['update:modelValue'])
</script>
<template><nav aria-label="Pagination" class="flex flex-wrap items-center gap-1"><button type="button" class="min-h-10 rounded-lg border border-slate-200 px-3 text-sm disabled:opacity-40 dark:border-slate-700" :disabled="modelValue<=1" @click="$emit('update:modelValue',modelValue-1)">Previous</button><button v-for="page in total" :key="page" type="button" class="min-h-10 min-w-10 rounded-lg px-3 text-sm" :class="page===modelValue?'bg-slate-950 text-white dark:bg-white dark:text-slate-950':'hover:bg-slate-100 dark:hover:bg-slate-800'" @click="$emit('update:modelValue',page)">{{ page }}</button><button type="button" class="min-h-10 rounded-lg border border-slate-200 px-3 text-sm disabled:opacity-40 dark:border-slate-700" :disabled="modelValue>=total" @click="$emit('update:modelValue',modelValue+1)">Next</button></nav></template>
