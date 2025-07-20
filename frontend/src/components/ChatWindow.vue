<script setup lang="ts">
import type { SystemMessage } from './setChat'
import ChatMessage from './ChatMessage.vue'
import { onMounted, onUpdated, ref } from 'vue';

const chatWindow = ref<HTMLDivElement>()


defineProps<{
  messages:SystemMessage[]
}>()

onUpdated(()=>{
  if (chatWindow.value){
    chatWindow.value.scrollTop = chatWindow.value.scrollHeight
  }
})

onMounted(()=>{
  if (chatWindow.value){
    chatWindow.value.scrollTop = chatWindow.value.scrollHeight
  }
})
</script>

<template>
  <div class="chat-window" ref="chatWindow">
    <div v-for="(message, index) in messages" :key="index">
      <ChatMessage :message="message" />
    </div>
  </div>
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
</style>
