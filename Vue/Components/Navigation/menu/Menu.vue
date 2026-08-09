<script setup>
defineOptions({ name: 'Menu' })
defineProps({ items: { type: Array, default: () => [] } })
defineEmits(['select'])
</script>
<template><div class="w-full rounded-xl border border-slate-200 bg-white p-1 dark:border-slate-700 dark:bg-slate-950"><button v-for="item in items" :key="item.value ?? item.label" type="button" class="flex w-full items-center rounded-lg px-3 py-2.5 text-left text-sm text-slate-700 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800" :disabled="item.disabled" @click="$emit('select',item.value ?? item)">{{ item.label }}</button></div></template>
