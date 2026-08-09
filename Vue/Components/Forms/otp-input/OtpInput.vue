<script setup>
import { computed, nextTick, ref } from 'vue'

defineOptions({ name: 'OtpInput' })

const props = withDefaults(defineProps({
  length: { type: Number, default: 6 },
  modelValue: { type: String, default: '' },
  disabled: { type: Boolean, default: false }
}), {})

const emit = defineEmits(['update:modelValue', 'complete'])
const inputs = ref([])
const values = computed(() => Array.from({ length: props.length }, (_, i) => props.modelValue[i] ?? ''))

function focusAt(index) { nextTick(() => inputs.value[index]?.focus()) }
function update(index, event) {
  const value = event.target.value.replace(/\D/g, '').slice(-1)
  const next = values.value.slice(); next[index] = value
  const code = next.join('')
  emit('update:modelValue', code)
  if (value && index < props.length - 1) focusAt(index + 1)
  if (code.length === props.length && !code.includes('')) emit('complete', code)
}
function keydown(index, event) {
  if (event.key === 'Backspace' && !values.value[index] && index > 0) focusAt(index - 1)
  if (event.key === 'ArrowLeft' && index > 0) focusAt(index - 1)
  if (event.key === 'ArrowRight' && index < props.length - 1) focusAt(index + 1)
}
function paste(event) {
  const pasted = event.clipboardData?.getData('text').replace(/\D/g, '').slice(0, props.length) ?? ''
  if (!pasted) return
  event.preventDefault(); emit('update:modelValue', pasted); focusAt(Math.min(pasted.length, props.length - 1))
}
</script>

<template>
  <div class="flex w-full max-w-sm items-center gap-2 sm:gap-3" @paste="paste">
    <input
      v-for="(_, index) in values" :key="index" :ref="el => inputs[index] = el"
      :value="values[index]" :disabled="disabled" inputmode="numeric" maxlength="1"
      autocomplete="one-time-code" :aria-label="`Digit ${index + 1} of ${length}`"
      class="h-12 min-w-0 flex-1 rounded-xl border border-slate-200 bg-white text-center text-lg font-semibold text-slate-900 outline-none transition focus:border-slate-900 focus:ring-4 focus:ring-slate-900/10 disabled:cursor-not-allowed disabled:opacity-50 dark:border-slate-700 dark:bg-slate-950 dark:text-white dark:focus:border-white"
      @input="update(index, $event)" @keydown="keydown(index, $event)"
    />
  </div>
</template>
