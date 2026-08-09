<script setup>
import { ref } from 'vue'
defineOptions({ name: 'Sidebar' })
defineProps({ items: { type: Array, default: () => [] }, title: { type: String, default: 'Menu' } })
const open = ref(false)
</script>
<template><aside class="w-full md:w-64"><button type="button" class="mb-2 flex w-full items-center justify-between rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm font-medium md:hidden dark:border-slate-700 dark:bg-slate-950" @click="open=!open">{{ title }} <span>{{ open ? '−' : '+' }}</span></button><nav :class="[open ? 'block' : 'hidden','space-y-1 md:block']"><a v-for="item in items" :key="item.href" :href="item.href" class="flex items-center rounded-lg px-3 py-2.5 text-sm text-slate-600 hover:bg-slate-100 hover:text-slate-950 dark:text-slate-400 dark:hover:bg-slate-900 dark:hover:text-white">{{ item.label }}</a></nav></aside></template>
