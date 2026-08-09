<script setup lang="ts">
withDefaults(defineProps<{ title?: string; message?: string }>(), { title: 'Something went wrong', message: 'We could not complete this request. Please try again.' })
</script>
<template>
  <section role="alert" class="flex min-h-48 w-full flex-col items-center justify-center rounded-2xl border border-red-200 bg-red-50/50 px-5 py-10 text-center dark:border-red-950 dark:bg-red-950/20"><div class="mb-4 grid size-10 place-items-center rounded-full bg-red-100 font-semibold text-red-700 dark:bg-red-950 dark:text-red-300">!</div><h2 class="text-base font-semibold text-slate-950 dark:text-white">{{ title }}</h2><p class="mt-1 max-w-md text-sm leading-6 text-slate-600 dark:text-slate-400">{{ message }}</p><div v-if="$slots.default" class="mt-5 flex w-full flex-col gap-2 sm:w-auto sm:flex-row"><slot /></div></section>
</template>
