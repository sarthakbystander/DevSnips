<script setup lang="ts">
import { ref } from 'vue'
withDefaults(defineProps<{ modelValue?: string; placeholder?: string }>(), { modelValue: '', placeholder: 'Password' })
const emit = defineEmits<{ 'update:modelValue': [value: string] }>(); const visible = ref(false)
</script>
<template><div class="relative"><input :value="modelValue" :type="visible ? 'text' : 'password'" :placeholder="placeholder" class="min-h-11 w-full rounded-lg border border-slate-300 bg-white px-3.5 pr-14 text-base outline-none focus:border-slate-900 focus:ring-2 focus:ring-slate-200 sm:text-sm" @input="emit('update:modelValue', ($event.target as HTMLInputElement).value)" /><button type="button" class="absolute inset-y-0 right-1 my-1 rounded-md px-3 text-xs font-medium text-slate-500 hover:bg-slate-100" @click="visible = !visible">{{ visible ? 'Hide' : 'Show' }}</button></div></template>
