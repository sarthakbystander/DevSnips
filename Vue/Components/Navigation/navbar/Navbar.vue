<script setup>
defineOptions({ name: 'Navbar' })
import { ref } from 'vue'
defineProps({ links: { type: Array, default: () => [] }, brand: { type: String, default: 'Brand' } })
const open = ref(false)
</script>
<template><header class="border-b border-slate-200 bg-white/95 backdrop-blur dark:border-slate-800 dark:bg-slate-950/95"><nav class="mx-auto flex min-h-16 max-w-7xl items-center justify-between gap-4 px-4 sm:px-6 lg:px-8"><a href="#" class="shrink-0 text-base font-semibold tracking-tight text-slate-950 dark:text-white">{{ brand }}</a><div class="hidden items-center gap-1 md:flex"><a v-for="link in links" :key="link.href" :href="link.href" class="rounded-lg px-3 py-2 text-sm text-slate-600 transition hover:bg-slate-100 hover:text-slate-950 dark:text-slate-400 dark:hover:bg-slate-900 dark:hover:text-white">{{ link.label }}</a></div><button type="button" class="rounded-lg p-2 text-slate-700 md:hidden dark:text-slate-300" aria-label="Toggle navigation" @click="open=!open">☰</button></nav><div v-if="open" class="border-t border-slate-200 px-4 py-3 md:hidden dark:border-slate-800"><a v-for="link in links" :key="link.href" :href="link.href" class="block rounded-lg px-3 py-3 text-sm text-slate-700 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-900">{{ link.label }}</a></div></header></template>
