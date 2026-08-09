<script setup lang="ts">
const stats=[['12k+','Developers'],['98.7%','Uptime'],['4.9/5','Average rating'],['32','Countries']]
</script>
<template><section class="rounded-3xl border border-slate-200 bg-white p-5 sm:p-8 dark:border-slate-800 dark:bg-slate-950"><div class="grid grid-cols-2 divide-x divide-y divide-slate-200 overflow-hidden rounded-2xl border border-slate-200 sm:grid-cols-4 sm:divide-y-0 dark:divide-slate-800 dark:border-slate-800"><article v-for="stat in stats" :key="stat[1]" class="p-5 sm:p-6"><strong class="text-2xl font-semibold tracking-tight sm:text-3xl">{{ stat[0] }}</strong><p class="mt-1 text-xs text-slate-500 sm:text-sm">{{ stat[1] }}</p></article></div></section></template>
