<script setup lang="ts">
withDefaults(defineProps<{ modelValue?: string; options: { label: string; value: string }[]; name?: string }>(), { modelValue: '', name: 'options' })
const emit = defineEmits<{ 'update:modelValue': [value: string] }>()
</script>
<template><fieldset class="grid gap-2"><legend class="sr-only">Choose an option</legend><label v-for="option in options" :key="option.value" class="flex min-h-11 cursor-pointer items-center gap-3 rounded-lg border border-slate-200 px-3 transition hover:bg-slate-50"><input :name="name" type="radio" :value="option.value" :checked="modelValue === option.value" class="h-4 w-4 accent-slate-900" @change="emit('update:modelValue', option.value)"><span class="text-sm text-slate-700">{{ option.label }}</span></label></fieldset></template>
