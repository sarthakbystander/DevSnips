<script setup>
import { computed, ref } from 'vue'
defineOptions({ name: 'CommandMenu' })
defineProps({ items: { type: Array, default: () => [] }, placeholder: { type: String, default: 'Search commands...' } })
defineEmits(['select'])
const open=ref(false); const query=ref('')
const filtered=computed(()=>items.filter(i=>String(i.label??i).toLowerCase().includes(query.value.toLowerCase())))
</script>
<template><div class="w-full max-w-lg"><button type="button" class="flex min-h-12 w-full items-center justify-between rounded-xl border border-slate-200 bg-white px-4 text-sm text-slate-500 dark:border-slate-700 dark:bg-slate-950" @click="open=true">{{ placeholder }}<kbd class="hidden rounded-md border px-2 py-1 text-xs sm:block">⌘K</kbd></button><div v-if="open" class="fixed inset-0 z-50 bg-black/20 p-4 sm:grid sm:place-items-start sm:pt-[15vh]" @click.self="open=false"><div class="mx-auto w-full max-w-lg overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-2xl dark:border-slate-700 dark:bg-slate-950"><input v-model="query" autofocus class="w-full border-b border-slate-200 bg-transparent px-4 py-4 text-sm outline-none dark:border-slate-800" :placeholder="placeholder"><div class="max-h-72 overflow-auto p-1"><button v-for="item in filtered" :key="item.value ?? item.label" type="button" class="block w-full rounded-lg px-3 py-3 text-left text-sm hover:bg-slate-100 dark:hover:bg-slate-800" @click="$emit('select',item.value ?? item);open=false">{{ item.label ?? item }}</button><p v-if="!filtered.length" class="px-3 py-6 text-center text-sm text-slate-500">No commands found.</p></div></div></div></div></template>
