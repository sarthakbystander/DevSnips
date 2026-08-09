<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
const open = ref(false)
const root = ref<HTMLElement | null>(null)
const close = (e: MouseEvent) => { if (root.value && !root.value.contains(e.target as Node)) open.value = false }
onMounted(() => document.addEventListener('click', close)); onBeforeUnmount(() => document.removeEventListener('click', close))
</script>
<template><div ref="root" class="relative inline-flex"><button class="min-h-11 rounded-l-lg border border-slate-900 bg-slate-900 px-4 text-sm font-medium text-white hover:bg-slate-800 focus:z-10 focus:outline-none focus:ring-2 focus:ring-slate-400"><slot name="action">Action</slot></button><button aria-label="Open actions" :aria-expanded="open" class="min-h-11 w-11 rounded-r-lg border border-l-slate-700 border-slate-900 bg-slate-900 text-white hover:bg-slate-800 focus:z-10 focus:outline-none focus:ring-2 focus:ring-slate-400" @click.stop="open = !open">⌄</button><div v-if="open" class="absolute right-0 top-[calc(100%+0.5rem)] z-20 min-w-44 rounded-xl border border-slate-200 bg-white p-1.5 shadow-xl"><slot name="menu"><button class="block w-full rounded-lg px-3 py-2 text-left text-sm hover:bg-slate-100">Secondary action</button></slot></div></div></template>
