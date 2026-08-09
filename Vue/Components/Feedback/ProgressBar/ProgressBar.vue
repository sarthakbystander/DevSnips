<script setup lang="ts">
withDefaults(defineProps<{ value?: number; label?: string }>(), { value: 0 })
</script>

<template>
  <div class="w-full">
    <div v-if="label" class="mb-2 flex justify-between text-sm font-medium"><span>{{ label }}</span><span>{{ value }}%</span></div>
    <div class="h-2 overflow-hidden rounded-full bg-slate-100 dark:bg-slate-800" role="progressbar" :aria-valuenow="value" aria-valuemin="0" aria-valuemax="100">
      <div class="h-full rounded-full bg-slate-900 transition-[width] duration-300 dark:bg-white" :style="{ width: `${Math.min(100, Math.max(0, value))}%` }" />
    </div>
  </div>
</template>
