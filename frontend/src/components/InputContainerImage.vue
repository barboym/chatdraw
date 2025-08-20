<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { createSvgFromPaths } from './SVGUtils';
import IconSendButton from './icons/IconSendButton.vue';
import IconEraseButton from './icons/IconEraseButton.vue';
import IconUndoButton from './icons/IconUndoButton.vue';

const props = defineProps<{
  submitFunction: (svg:string) => void
}>()

const strokes = ref<{x: number, y:number}[][]>([])
const drawing = ref(false)
const currentStroke = ref<{x: number, y: number}[]>([])
const canvasRef = ref<HTMLCanvasElement | null>(null)
const width = ref(600)
const height = ref(600)

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
  const scaleX = canvas.width / rect.width
  const scaleY = canvas.height / rect.height
  return {
    x: (clientX - rect.left) * scaleX,
    y: (clientY - rect.top) * scaleY
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
  for (const stroke of strokes.value) {
    if (stroke.length < 2) continue
    ctx.beginPath()
    ctx.moveTo(stroke[0].x, stroke[0].y)
    for (let i = 1; i < stroke.length; i++) {
      ctx.lineTo(stroke[i].x, stroke[i].y)
    }
    ctx.stroke()
  }
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
  props.submitFunction(svg.outerHTML)
}

onMounted(() => {
  drawCanvas()
})

watch(strokes, drawCanvas)
</script>

<template>
  <div class="input-container">
    <div>
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
    </div>
    <div class="button-column">
      <button
        class="erase-button"
        @click="() => { strokes = []; currentStroke = []; drawCanvas(); }"
        :disabled="strokes.length === 0 && currentStroke.length === 0"
        aria-label="Erase"
      >
        <IconEraseButton/>
      </button>
      <button
        class="undo-button"
        @click="() => { strokes.pop(); currentStroke = []; drawCanvas(); }"
        :disabled="strokes.length === 0 && currentStroke.length === 0"
        aria-label="Undo"
      >
        <IconUndoButton/>
      </button>
      <button
        class="send-button"
        @click="handleSubmit"
        :disabled="strokes.length === 0"
        aria-label="Send"
      >
        <IconSendButton/>
      </button>
    </div>
  </div>
</template>

<style scoped>
.input-container {
  display: flex;
  align-items: stretch;
  padding: 8px;
  background: #f0f0f0;
  border-radius: 24px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
  position: relative;
}

.draw-canvas {
  border: 1.5px solid #8f8d8d;
  border-radius: 12px;
  background: #fff;
  flex: 1;
  display: block;
  margin-right: 12px;
  box-sizing: border-box;
  max-width: 100%;
  cursor: crosshair;
}

.button-column {
  position: relative;
  top: 8px;
  right: 8px;
  bottom: 8px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  height: calc(100% - 16px);
  z-index: 2;
}

.erase-button,
.undo-button,
.send-button {
  border: none;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  cursor: pointer;
  margin: 0;
  transition: background 0.2s;
}

.erase-button {
  background: #ff5252;
}
.erase-button:disabled {
  background: #bdbdbd;
  cursor: not-allowed;
}

.undo-button {
  background: #ffba52;
  margin-top: 12px;
}
.undo-button:disabled {
  background: #bdbdbd;
  cursor: not-allowed;
}

.send-button {
  background: #25d366;
  margin-top: 100px;
}
.send-button:disabled {
  background: #bdbdbd;
  cursor: not-allowed;
}
</style>
