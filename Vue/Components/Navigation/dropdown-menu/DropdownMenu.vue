<script setup>
import { ref } from 'vue'
defineOptions({ name: 'DropdownMenu' })
defineProps({ label: { type: String, default: 'Options' }, items: { type: Array, default: () => [] } })
defineEmits(['select'])
const open=ref(false)
</script>
<template><div class="relative inline-block"><button type="button" class="inline-flex min-h-10 items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm font-medium dark:border-slate-700 dark:bg-slate-950" @click="open=!open">{{ label }} <span>⌄</span></button><div v-if="open" class="absolute right-0 z-30 mt-2 w-52 rounded-xl border border-slate-200 bg-white p-1 shadow-xl dark:border-slate-700 dark:bg-slate-950"><button v-for="item in items" :key="item.value ?? item.label" type="button" class="block w-full rounded-lg px-3 py-2.5 text-left text-sm hover:bg-slate-100 dark:hover:bg-slate-800" @click="$emit('select',item.value ?? item);open=false">{{ item.label }}</button></div></div></template>
