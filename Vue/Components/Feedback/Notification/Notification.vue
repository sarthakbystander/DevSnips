<script setup lang="ts">
withDefaults(defineProps<{ title?: string; message?: string; dismissible?: boolean }>(), { dismissible: true })
const emit = defineEmits<{ close: [] }>()
</script>
<template>
  <aside role="status" class="flex w-full items-start gap-3 rounded-xl border border-slate-200 bg-white p-4 text-slate-900 shadow-sm dark:border-slate-800 dark:bg-slate-950 dark:text-white">
    <span class="mt-0.5 grid size-8 shrink-0 place-items-center rounded-full bg-slate-100 text-sm dark:bg-slate-900" aria-hidden="true">i</span>
    <div class="min-w-0 flex-1"><p v-if="title" class="text-sm font-semibold">{{ title }}</p><p v-if="message" class="mt-1 text-sm leading-5 text-slate-600 dark:text-slate-400">{{ message }}</p><slot /></div>
    <button v-if="dismissible" type="button" aria-label="Dismiss notification" class="rounded-md p-1 text-slate-400 hover:bg-slate-100 hover:text-slate-900 focus:outline-none focus:ring-2 focus:ring-slate-400 dark:hover:bg-slate-900 dark:hover:text-white" @click="emit('close')">×</button>
  </aside>
</template>
