<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { setChat } from './components/setChat.ts'
import ChatWindow from './components/ChatWindow.vue'
import InputContainer from './components/InputContainer.vue'

const canvasRef = ref(null)
const ctx = ref(null)
const isDrawing = ref(false)
const lastX = ref(0)
const lastY = ref(0)

const { messages, sendMessage } = setChat()

const submitMessage = async (input:string) => {
  await sendMessage({ mtype: 'text', content: input })
}


function startDrawing(e) {
  isDrawing.value = true
  ;[lastX.value, lastY.value] = [e.offsetX, e.offsetY]
}

function draw(e) {
  if (!isDrawing.value) return

  ctx.value.beginPath()
  ctx.value.moveTo(lastX.value, lastY.value)
  ctx.value.lineTo(e.offsetX, e.offsetY)
  ctx.value.stroke()

  ;[lastX.value, lastY.value] = [e.offsetX, e.offsetY]
}

function stopDrawing() {
  isDrawing.value = false
}

function clearCanvas() {
  ctx.value.clearRect(0, 0, canvasRef.value.width, canvasRef.value.height)
}

onMounted(() => {
  if (canvasRef.value) {
    ctx.value = canvasRef.value.getContext('2d')
    ctx.value.lineWidth = 2
    ctx.value.strokeStyle = '#000'
    ctx.value.lineCap = 'round'
  }
})

</script>

<template>
  <main>
  <div>
    <ChatWindow :messages="messages" />
    <div class="canvas-container">
      <canvas
        ref="canvasRef"
        width="400"
        height="200"
        @mousedown="startDrawing"
        @mousemove="draw"
        @mouseup="stopDrawing"
        @mouseout="stopDrawing"
      ></canvas>
      <div class="canvas-controls">
        <button @click="clearCanvas">Clear</button>
      </div>
    </div>
    <InputContainer :submitFunction="submitMessage"/>
  </div>
  </main>
</template>

<style scoped>

.canvas-container {
  margin-bottom: 10px;
}

canvas {
  border: 1px solid #ccc;
  background-color: #fff;
  cursor: crosshair;
  display: block;
}

.canvas-controls {
  margin-top: 5px;
}

.sketch-image {
  max-width: 100%;
  max-height: 200px;
  border: 1px solid #eee;
}

.input-container {
  display: flex;
}

input {
  flex-grow: 1;
  margin-right: 5px;
  padding: 8px;
}

button {
  padding: 8px 16px;
  background-color: #4caf50;
  color: white;
  border: none;
  cursor: pointer;
  margin-right: 5px;
}

button:hover:not(:disabled) {
  background-color: #45a049;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

input:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}


@keyframes bounce {
  0%,
  80%,
  100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}
</style>
