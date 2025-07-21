<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { createSvgFromPaths } from './SVGUtils';

const props = defineProps<{
  submitFunction: (svg:string) => void
}>()

const strokes = ref<{x: number, y:number}[][]>([]) // array of arrays of points
const drawing = ref(false)
const currentStroke = ref<{x: number, y: number}[]>([])
const canvasRef = ref<HTMLCanvasElement | null>(null)
const width = ref(400)
const height = ref(400)

function getCanvasPos(e: MouseEvent | TouchEvent) {
  const canvas = canvasRef.value
  if (!canvas) return { x: 0, y: 0 }
  const rect = canvas.getBoundingClientRect()
  let clientX = 0, clientY = 0
  if (e instanceof MouseEvent) {
    clientX = e.clientX
    clientY = e.clientY
  } else if (e.touches && e.touches.length > 0) {
    clientX = e.touches[0].clientX
    clientY = e.touches[0].clientY
  }
  return {
    x: clientX - rect.left,
    y: clientY - rect.top
  }
}

function startStroke(e: MouseEvent | TouchEvent) {
  drawing.value = true
  currentStroke.value = []
  const pos = getCanvasPos(e)
  currentStroke.value.push(pos)
}

function moveStroke(e: MouseEvent | TouchEvent) {
  if (!drawing.value) return
  const pos = getCanvasPos(e)
  currentStroke.value.push(pos)
  drawCanvas()
}

function endStroke() {
  if (!drawing.value) return
  drawing.value = false
  if (currentStroke.value.length > 0) {
    console.log("added stroke",currentStroke.value)
    strokes.value.push([...currentStroke.value])
    currentStroke.value = []
    drawCanvas()
  }
}

function drawCanvas() {
  const canvas = canvasRef.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')
  if (!ctx) return
  ctx.clearRect(0, 0, canvas.width, canvas.height)
  ctx.strokeStyle = '#222'
  ctx.lineWidth = 2
  ctx.lineCap = 'round'
  // Draw all strokes
  for (const stroke of strokes.value) {
    if (stroke.length < 2) continue
    ctx.beginPath()
    ctx.moveTo(stroke[0].x, stroke[0].y)
    for (let i = 1; i < stroke.length; i++) {
      ctx.lineTo(stroke[i].x, stroke[i].y)
    }
    ctx.stroke()
  }
  // Draw current stroke
  if (currentStroke.value.length > 1) {
    ctx.beginPath()
    ctx.moveTo(currentStroke.value[0].x, currentStroke.value[0].y)
    for (let i = 1; i < currentStroke.value.length; i++) {
      ctx.lineTo(currentStroke.value[i].x, currentStroke.value[i].y)
    }
    ctx.stroke()
  }
}

function handleSubmit() {
  if (strokes.value.length === 0) return
  const svg = createSvgFromPaths(strokes.value,width.value,height.value)
  console.log("converted strokes to svg:",svg.innerHTML)
  props.submitFunction(svg.outerHTML)
}

onMounted(() => {
  drawCanvas()
})

watch(strokes, drawCanvas)

</script>

<template>
  <div class="input-container">
    <canvas
      ref="canvasRef"
      :width="width"
      :height="height"
      class="draw-canvas"
      @mousedown="startStroke"
      @mousemove="moveStroke"
      @mouseup="endStroke"
      @mouseleave="endStroke"
      @touchstart.prevent="startStroke"
      @touchmove.prevent="moveStroke"
      @touchend.prevent="endStroke"
      aria-label="Drawing canvas"
      tabindex="0"
    ></canvas>
    <button
      class="send-button"
      @click="handleSubmit"
      :disabled="strokes.length === 0"
      aria-label="Send"
    >
      <svg
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M2 21L23 12L2 3V10L17 12L2 14V21Z"
          fill="currentColor"
        />
      </svg>
    </button>
  </div>
</template>


<style scoped>
.input-container {
  display: flex;
  align-items: center;
  padding: 8px;
  background: #f0f0f0;
  border-radius: 24px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}

.input-field {
  flex: 1;
  border: none;
  outline: none;
  padding: 10px 16px;
  border-radius: 20px;
  font-size: 16px;
  background: #fff;
  margin-right: 8px;
}

.send-button {
  background: #25d366;
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  cursor: pointer;
  transition: background 0.2s;
}

.send-button:disabled {
  background: #bdbdbd;
  cursor: not-allowed;
}
</style>
