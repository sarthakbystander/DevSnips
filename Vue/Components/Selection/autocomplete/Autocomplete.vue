<script setup>
import { computed, ref } from 'vue'
defineOptions({ name: 'Autocomplete' })
const props = withDefaults(defineProps({ modelValue: String, options: { type: Array, default: () => [] }, placeholder: { type: String, default: 'Start typing...' } }), {})
const emit = defineEmits(['update:modelValue', 'select'])
const open = ref(false)
const filtered = computed(() => props.options.filter(o => String(o).toLowerCase().includes((props.modelValue ?? '').toLowerCase())).slice(0, 8))
function choose(value) { emit('update:modelValue', String(value)); emit('select', value); open.value=false }
</script>
<template><div class="relative w-full"><input :value="modelValue" :placeholder="placeholder" class="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm outline-none focus:border-slate-900 focus:ring-4 focus:ring-slate-900/10 dark:border-slate-700 dark:bg-slate-950" @input="emit('update:modelValue',$event.target.value);open=true" @focus="open=true" @keydown.esc="open=false"><div v-if="open && filtered.length" class="absolute z-20 mt-2 w-full overflow-hidden rounded-xl border border-slate-200 bg-white p-1 shadow-xl dark:border-slate-700 dark:bg-slate-950"><button v-for="option in filtered" :key="option" type="button" class="block w-full rounded-lg px-3 py-2 text-left text-sm hover:bg-slate-100 dark:hover:bg-slate-800" @click="choose(option)">{{ option }}</button></div></div></template>
