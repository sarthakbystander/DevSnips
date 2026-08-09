<script setup>
import { computed, ref } from 'vue'
defineOptions({ name: 'Combobox' })
const props = withDefaults(defineProps({ modelValue: [String, Number], options: { type: Array, default: () => [] }, placeholder: { type: String, default: 'Search...' } }), {})
const emit = defineEmits(['update:modelValue'])
const query = ref(''); const open = ref(false)
const filtered = computed(() => props.options.filter(o => String(o.label ?? o).toLowerCase().includes(query.value.toLowerCase())))
</script>
<template><div class="relative w-full"><input v-model="query" :placeholder="placeholder" class="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm outline-none focus:border-slate-900 focus:ring-4 focus:ring-slate-900/10 dark:border-slate-700 dark:bg-slate-950" @focus="open=true" @keydown.esc="open=false"><div v-if="open" class="absolute z-20 mt-2 max-h-60 w-full overflow-auto rounded-xl border border-slate-200 bg-white p-1 shadow-xl dark:border-slate-700 dark:bg-slate-950"><button v-for="option in filtered" :key="option.value ?? option" type="button" class="block w-full rounded-lg px-3 py-2 text-left text-sm hover:bg-slate-100 dark:hover:bg-slate-800" @click="emit('update:modelValue', option.value ?? option); query=option.label ?? option; open=false">{{ option.label ?? option }}</button><p v-if="!filtered.length" class="px-3 py-3 text-sm text-slate-500">No results found.</p></div></div></template>
