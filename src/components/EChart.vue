<template>
  <div ref="chartRef" class="chart-wrap"></div>
</template>

<script setup>
import * as echarts from 'echarts'
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'

const props = defineProps({
  option: { type: Object, required: true }
})
const emit = defineEmits(['chart-click'])

const chartRef = ref(null)
let chart
let resizeObserver

function render() {
  if (!chartRef.value) return
  if (!chart) {
    chart = echarts.init(chartRef.value, null, { renderer: 'canvas' })
    chart.on('click', (params) => emit('chart-click', params))
  }
  chart.setOption(props.option, true)
  chart.resize()
}

onMounted(() => {
  render()
  resizeObserver = new ResizeObserver(() => {
    if (chart) chart.resize()
  })
  resizeObserver.observe(chartRef.value)
})

watch(
  () => props.option,
  () => render(),
  { deep: true }
)

onBeforeUnmount(() => {
  resizeObserver?.disconnect()
  if (chart) chart.dispose()
})
</script>
