<script setup lang="ts">
import { setChat } from './components/setChat.ts'
import ChatWindow from './components/ChatWindow.vue'
import InputContainer from './components/InputContainer.vue'
import InputContainerImage from './components/InputContainerImage.vue'

const { messages, sendMessage } = setChat()

const submitMessage = async (input:string) => {
  await sendMessage({ mtype: 'text', content: input })
}
const submitMessageImage = async (input:string) => {
  await sendMessage({ mtype: 'image', content: input })
}
</script>

<template>
  <main>
    <ChatWindow :messages="messages" />
    <InputContainerImage :submitFunction="submitMessageImage"/>
    
    <InputContainer :submitFunction="submitMessage"/>
  </main>
</template>
