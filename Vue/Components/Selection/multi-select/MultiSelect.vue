<script setup>
import { computed, ref } from 'vue'
defineOptions({ name: 'MultiSelect' })
const props = withDefaults(defineProps({ modelValue: { type: Array, default: () => [] }, options: { type: Array, default: () => [] }, placeholder: { type: String, default: 'Select options' } }), {})
const emit = defineEmits(['update:modelValue'])
const open = ref(false)
const selected = computed(() => props.options.filter(o => props.modelValue.includes(o.value ?? o)))
function toggle(value) { const next = props.modelValue.includes(value) ? props.modelValue.filter(v => v !== value) : [...props.modelValue, value]; emit('update:modelValue', next) }
</script>
<template><div class="relative w-full"><button type="button" class="flex min-h-12 w-full items-center gap-2 rounded-xl border border-slate-200 bg-white px-3 py-2 text-left text-sm outline-none focus:border-slate-900 focus:ring-4 focus:ring-slate-900/10 dark:border-slate-700 dark:bg-slate-950" @click="open=!open"><span v-if="!selected.length" class="text-slate-500">{{ placeholder }}</span><span v-for="item in selected" v-else :key="item.value ?? item" class="rounded-md bg-slate-100 px-2 py-1 dark:bg-slate-800">{{ item.label ?? item }}</span><span class="ml-auto">⌄</span></button><div v-if="open" class="absolute z-20 mt-2 max-h-60 w-full overflow-auto rounded-xl border border-slate-200 bg-white p-1 shadow-xl dark:border-slate-700 dark:bg-slate-950"><button v-for="option in options" :key="option.value ?? option" type="button" class="flex w-full items-center rounded-lg px-3 py-2 text-sm hover:bg-slate-100 dark:hover:bg-slate-800" @click="toggle(option.value ?? option)"><span class="mr-3">{{ modelValue.includes(option.value ?? option) ? '✓' : '' }}</span>{{ option.label ?? option }}</button></div></div></template>
