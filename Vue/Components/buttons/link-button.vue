<script setup lang="ts">
withDefaults(defineProps<{ href?: string; external?: boolean }>(), { href: '#', external: false })
</script>
<template><a :href="href" :target="external ? '_blank' : undefined" :rel="external ? 'noreferrer' : undefined" class="inline-flex min-h-11 items-center justify-center rounded-lg px-3 text-sm font-medium text-slate-900 underline decoration-slate-300 underline-offset-4 transition hover:decoration-slate-900 focus:outline-none focus:ring-2 focus:ring-slate-400"> <slot /> </a></template>
