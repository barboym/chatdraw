<script setup lang="ts">
import { ref, nextTick, onUpdated, onMounted } from 'vue'
import { setChat } from './components/setChat.ts'
import typingIndicator from './components/TypingIndicator.vue'
import ChatMessage from './components/ChatMessage.vue'

const userInput = ref('')
const chatWindow = ref(null)
const canvasRef = ref(null)
const ctx = ref(null)
const isDrawing = ref(false)
const lastX = ref(0)
const lastY = ref(0)

const { messages, waitingForResponse, sendMessage } = setChat()

async function submitMessage() {
  if (waitingForResponse.value) return
  if (userInput.value == '') return
  // const sketchDataUrl = canvasRef.value.toDataURL();
  // messages.value.push({ sender: 'You', isImage: true, imageUrl: sketchDataUrl });
  // clearCanvas();
  waitingForResponse.value = true

  try {
    await sendMessage({ mtype: 'text', content: userInput.value })
  } finally {
    waitingForResponse.value = false
    nextTick(() => {
      scrollToBottom()
    })
  }
}
function scrollToBottom() {
  chatWindow.value.scrollTop = chatWindow.value.scrollHeight
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

onUpdated(() => {
  scrollToBottom()
})
</script>

<template>
  <main>
  <div>
    <div class="chat-window" ref="chatWindow">
      <div v-for="(message, index) in messages" :key="index">
          <ChatMessage :message="message"/>
          <!-- <p>
            <strong>{{ message.isUser }} {{ message.isSketch }} {{ message.text }}</strong>
          </p> -->
      </div>
      <typingIndicator :waitingForResponse="waitingForResponse" />
    </div>
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

        <button @click="clearCanvas" :disabled="waitingForResponse">Clear</button>
        <!-- <button @click="submitSketch" :disabled="waitingForResponse">Submit Sketch</button> -->
      </div>
    </div>

    <div class="input-container">
      <input
        v-model="userInput"
        @keyup.enter="submitMessage"
        placeholder="Type a message..."
        :disabled="waitingForResponse"
      />
      <button @click="submitMessage" :disabled="waitingForResponse">
        {{ waitingForResponse ? 'Waiting...' : 'Send' }}
      </button>
    </div>
  </div>
  </main>
</template>

<style scoped>
.chat-window {
  height: 300px;
  overflow-y: auto;
  border: 1px solid #ccc;
  background-color: #6f996e;
  padding: 10px;
  margin-bottom: 10px;
}

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
