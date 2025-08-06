<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { createSvgFromPaths } from './SVGUtils';
import IconSendButton from './icons/IconSendButton.vue';
import IconEraseButton from './icons/IconEraseButton.vue';
import IconUndoButton from './icons/IconUndoButton.vue';

const props = defineProps<{
  submitFunction: (svg:string) => void
}>()

const strokes = ref<{x: number, y:number}[][]>([]) // array of arrays of points
const drawing = ref(false)
const currentStroke = ref<{x: number, y: number}[]>([])
const canvasRef = ref<HTMLCanvasElement | null>(null)
const width = ref(400)
const height = ref(400)

/**
 * Calculates the position of the mouse or touch event relative to the canvas element.
 *
 * @param {MouseEvent | TouchEvent} e - The mouse or touch event.
 * @returns {{ x: number, y: number }} The x and y coordinates relative to the canvas.
 *
 * The function determines the event type (mouse or touch), extracts the client coordinates,
 * and computes the position relative to the top-left corner of the canvas.
 * If the canvas reference is not available, it returns { x: 0, y: 0 }.
 */
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
      class="erase-button"
      @click="() => { strokes = []; currentStroke = []; drawCanvas(); }"
      :disabled="strokes.length === 0 && currentStroke.length === 0"
      aria-label="Erase"
    >
      <IconEraseButton/>
    </button>
    <button
      class="Undo-button"
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
  </template>

  <style scoped>
  .erase-button {
    position: absolute;
    top: 8px;
    right: 8px;
    background: #ff5252;
    border: none;
    border-radius: 50%;
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    cursor: pointer;
    transition: background 0.2s;
    margin: 0;
    z-index: 2;
  }
  .erase-button:disabled {
    background: #bdbdbd;
    cursor: not-allowed;
  }
  .undo-button {
    position: absolute;
    top: 8px;
    right: 8px;
    background: #ffba52;
    border: none;
    border-radius: 50%;
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    cursor: pointer;
    transition: background 0.2s;
    margin: 0;
    z-index: 2;
  }
  .undo-button:disabled {
    background: #bdbdbd;
    cursor: not-allowed;
  }
.input-container {
  display: flex;
  align-items: flex-end; /* Align items to the bottom */
  padding: 8px;
  background: #f0f0f0;
  border-radius: 24px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
  position: relative; /* Needed for absolute positioning of send button if required */
}

/* Add a light border and rounded corners to the canvas */
.draw-canvas {
  border: 1.5px solid #e0e0e0; /* Light border */
  border-radius: 12px;
  background: #fff;
  flex: 1;
  display: block;
  margin-right: 12px; /* Space between canvas and button */
  box-sizing: border-box;
  max-width: 100%;
  cursor: crosshair;
}

/* The send button stays at the bottom right of the container */
.send-button {
  background: #25d366;
  border: none;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  cursor: pointer;
  transition: background 0.2s;
  /* No need for absolute positioning since flex aligns it to the end */
  margin-bottom: 4px; /* Optional: small offset from bottom */
  right: 8px;
}

/* Remove .input-field since it's not used in this component */

/* Keep the disabled style for the send button */
.send-button:disabled {
  background: #bdbdbd;
  cursor: not-allowed;
}

/*
Explanation:
- .input-container uses align-items: flex-end to keep children (canvas and button) aligned at the bottom.
- .draw-canvas gets a light border and rounded corners for better visibility.
- .send-button remains at the bottom right due to flex layout and margin.
- Removed .input-field since it's not present in the template.
*/
</style>
