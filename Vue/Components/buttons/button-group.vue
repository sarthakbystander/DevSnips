<script setup lang="ts">
defineProps<{ attached?: boolean }>()
</script>
<template><div role="group" :class="['inline-flex max-w-full flex-wrap items-center', attached ? '[&>button:not(:first-child)]:-ml-px [&>button]:rounded-none [&>button:first-child]:rounded-l-lg [&>button:last-child]:rounded-r-lg' : 'gap-2']"><slot /></div></template>
