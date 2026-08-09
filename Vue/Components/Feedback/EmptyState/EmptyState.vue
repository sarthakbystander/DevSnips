<script setup lang="ts">
withDefaults(defineProps<{ title?: string; message?: string }>(), { title: 'Nothing here yet', message: 'There is nothing to display right now.' })
</script>

<template>
  <section class="flex min-h-48 w-full flex-col items-center justify-center rounded-2xl border border-dashed border-slate-300 px-5 py-10 text-center dark:border-slate-700" aria-live="polite">
    <div class="mb-4 grid size-10 place-items-center rounded-full bg-slate-100 text-slate-500 dark:bg-slate-900 dark:text-slate-400" aria-hidden="true">—</div>
    <h2 class="text-base font-semibold tracking-tight text-slate-950 dark:text-white">{{ title }}</h2>
    <p class="mt-1 max-w-md text-sm leading-6 text-slate-500 dark:text-slate-400">{{ message }}</p>
    <div v-if="$slots.default" class="mt-5 flex w-full flex-col justify-center gap-2 sm:w-auto sm:flex-row"><slot /></div>
  </section>
</template>
