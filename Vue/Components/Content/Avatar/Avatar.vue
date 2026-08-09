<script setup lang="ts">
withDefaults(defineProps<{ src?: string; alt?: string; initials?: string; size?: 'sm'|'md'|'lg' }>(), { size: 'md', alt: '' })
</script>
<template><div :class="['grid shrink-0 place-items-center overflow-hidden rounded-full bg-slate-100 font-medium text-slate-700 dark:bg-slate-900 dark:text-slate-300', size === 'sm' ? 'size-8 text-xs' : size === 'lg' ? 'size-12 text-sm' : 'size-10 text-xs']"><img v-if="src" :src="src" :alt="alt" class="size-full object-cover" /><span v-else aria-hidden="true">{{ initials }}</span></div></template>
