<script setup lang="ts">
defineProps<{
  waitingForResponse: boolean
}>()
</script>

<template>
  <div v-if="waitingForResponse" class="typing-indicator">
    <span></span>
    <span></span>
    <span></span>
  </div>
</template>

<style scoped>

.typing-indicator {
  display: flex;
  align-items: center;
  margin: 5px 0;
}

.typing-indicator span {
  height: 8px;
  width: 8px;
  margin: 0 2px;
  background-color: #ffffff;
  border-radius: 50%;
  display: inline-block;
  animation: bounce 1.5s infinite ease-in-out;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}
</style>
