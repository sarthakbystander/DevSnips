<script setup lang="ts">
withDefaults(defineProps<{ lines?: number; rounded?: boolean }>(), { lines: 3, rounded: true })
</script>
<template>
  <div class="w-full animate-pulse space-y-3" aria-label="Loading" role="status"><span class="sr-only">Loading</span><div v-for="line in lines" :key="line" :class="['h-4 bg-slate-200 dark:bg-slate-800', rounded ? 'rounded-md' : '']" :style="{ width: line === lines ? '65%' : '100%' }" /></div>
</template>
