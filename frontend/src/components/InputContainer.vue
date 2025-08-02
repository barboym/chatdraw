<script setup lang="ts">
import { ref } from 'vue'
import IconSendButton from './icons/IconSendButton.vue';

const props = defineProps<{
  submitFunction: (msg: string) => void
}>()

const message = ref('')

function handleSubmit() {
  if (message.value.trim() === '') {
    console.log("empty message")
    return
  };
  props.submitFunction(message.value)
  message.value = ''
}
</script>

<template>
  <div class="input-container">
    <input
      v-model="message"
      class="input-field"
      placeholder="Type a message"
      @keyup.enter="handleSubmit"
    />
    <button
      class="send-button"
      @click="handleSubmit"
      aria-label="Send"
    ><IconSendButton/>
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
