<script setup>
defineOptions({ name: 'Stepper' })
defineProps({ modelValue: { type: Number, default: 0 }, steps: { type: Array, default: () => [] } })
defineEmits(['update:modelValue'])
</script>
<template><ol class="flex w-full items-start overflow-x-auto"><li v-for="(step,index) in steps" :key="step.label" class="flex min-w-28 flex-1 items-center"><button type="button" class="flex items-center gap-2" @click="$emit('update:modelValue',index)"><span class="grid h-8 w-8 shrink-0 place-items-center rounded-full text-xs font-semibold" :class="index<=modelValue?'bg-slate-950 text-white dark:bg-white dark:text-slate-950':'bg-slate-100 text-slate-500 dark:bg-slate-800'">{{ index+1 }}</span><span class="hidden text-sm font-medium sm:block">{{ step.label }}</span></button><span v-if="index<steps.length-1" class="mx-2 h-px flex-1 bg-slate-200 dark:bg-slate-800" /></li></ol></template>
