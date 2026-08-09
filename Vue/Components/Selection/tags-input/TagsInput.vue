<script setup>
import { ref } from 'vue'
defineOptions({ name: 'TagsInput' })
const props = withDefaults(defineProps({ modelValue: { type: Array, default: () => [] }, placeholder: { type: String, default: 'Add a tag...' } }), {})
const emit = defineEmits(['update:modelValue'])
const input = ref('')
function add() { const value=input.value.trim(); if(value && !props.modelValue.includes(value)) emit('update:modelValue',[...props.modelValue,value]); input.value='' }
function remove(tag) { emit('update:modelValue',props.modelValue.filter(v=>v!==tag)) }
</script>
<template><div class="flex min-h-12 w-full flex-wrap items-center gap-2 rounded-xl border border-slate-200 bg-white px-3 py-2 focus-within:border-slate-900 focus-within:ring-4 focus-within:ring-slate-900/10 dark:border-slate-700 dark:bg-slate-950"><span v-for="tag in modelValue" :key="tag" class="inline-flex items-center gap-1 rounded-md bg-slate-100 px-2 py-1 text-xs font-medium dark:bg-slate-800">{{ tag }}<button type="button" class="px-1 text-slate-500 hover:text-slate-900" :aria-label="`Remove ${tag}`" @click="remove(tag)">×</button></span><input v-model="input" :placeholder="placeholder" class="min-w-24 flex-1 bg-transparent py-1 text-sm outline-none" @keydown.enter.prevent="add" @keydown.188.prevent="add"></div></template>
