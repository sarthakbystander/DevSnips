<script setup lang="ts">
withDefaults(defineProps<{ title?: string; description?: string; href?: string }>(), {})
</script>
<template>
  <component :is="href ? 'a' : 'article'" :href="href" class="group block w-full overflow-hidden rounded-2xl border border-slate-200 bg-white p-5 text-slate-950 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md focus:outline-none focus:ring-2 focus:ring-slate-400 dark:border-slate-800 dark:bg-slate-950 dark:text-white">
    <div v-if="$slots.media" class="mb-5 overflow-hidden rounded-xl"><slot name="media" /></div>
    <h2 v-if="title" class="text-base font-semibold tracking-tight">{{ title }}</h2>
    <p v-if="description" class="mt-1.5 text-sm leading-6 text-slate-600 dark:text-slate-400">{{ description }}</p>
    <div v-if="$slots.default" class="mt-5"><slot /></div>
  </component>
</template>
