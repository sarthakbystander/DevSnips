<script setup>
defineOptions({ name: 'Breadcrumbs' })
defineProps({ items: { type: Array, default: () => [] } })
</script>
<template><nav aria-label="Breadcrumb" class="w-full overflow-x-auto"><ol class="flex min-w-max items-center gap-2 text-sm"><li v-for="(item,index) in items" :key="item.href ?? index" class="flex items-center gap-2"><span v-if="index" class="text-slate-300 dark:text-slate-700">/</span><a v-if="index < items.length-1" :href="item.href" class="text-slate-500 hover:text-slate-950 dark:hover:text-white">{{ item.label }}</a><span v-else class="font-medium text-slate-950 dark:text-white">{{ item.label }}</span></li></ol></nav></template>
