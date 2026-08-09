<script setup>
defineOptions({ name: 'MobileNavigation' })
defineProps({ items: { type: Array, default: () => [] }, modelValue: String })
defineEmits(['update:modelValue'])
</script>
<template><nav class="fixed inset-x-0 bottom-0 z-40 border-t border-slate-200 bg-white/95 px-2 pb-[env(safe-area-inset-bottom)] pt-2 backdrop-blur md:hidden dark:border-slate-800 dark:bg-slate-950/95"><div class="mx-auto grid max-w-lg grid-cols-4 gap-1"><button v-for="item in items.slice(0,4)" :key="item.value" type="button" class="min-h-12 rounded-xl px-2 text-xs font-medium" :class="modelValue===item.value?'bg-slate-100 text-slate-950 dark:bg-slate-800 dark:text-white':'text-slate-500'" @click="$emit('update:modelValue',item.value)">{{ item.label }}</button></div></nav></template>
