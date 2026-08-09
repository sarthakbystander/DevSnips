<script setup lang="ts">
defineProps<{ title?: string; message: string; variant?: 'info' | 'success' | 'warning' | 'error' }>()
</script>

<template>
  <div role="alert" class="w-full rounded-xl border border-slate-200 bg-white p-4 text-slate-900 shadow-sm dark:border-slate-800 dark:bg-slate-950 dark:text-slate-100">
    <div class="flex gap-3">
      <div class="min-w-0 flex-1">
        <p v-if="title" class="text-sm font-semibold">{{ title }}</p>
        <p class="mt-1 text-sm leading-6 text-slate-600 dark:text-slate-400">{{ message }}</p>
      </div>
    </div>
  </div>
</template>
