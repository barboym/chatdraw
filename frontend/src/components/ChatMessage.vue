<script setup lang="ts">
import type { SystemMessage } from './setChat.ts'

defineProps<{
  message: SystemMessage
}>();
</script>

<template>
    <div
        class="chat-message"
        :class="{
            'chat-message--user': message.isUser,
            'chat-message--system': !message.isUser
        }"
    >
        <div class="chat-bubble">
            <template v-if="message.isSketch && message.imageUrl">
                  <img
                    :src="message.imageUrl"
                    alt="Had some parsing error"
                    class="chat-image"
                />
            </template>
            <template v-else>
                <span class="chat-text">{{ message.text }}</span>
            </template>
        </div>
    </div>
</template>



<style scoped>
.chat-message {
    display: flex;
    margin: 8px 0;
}

.chat-message--user {
    justify-content: flex-end;
}

.chat-message--system {
    justify-content: flex-start;
}

.chat-bubble {
    max-width: 70%;
    padding: 10px 14px;
    border-radius: 18px;
    background: #e5e5ea;
    color: #222;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    position: relative;
    word-break: break-word;
}

.chat-message--user .chat-bubble {
    background: #dcf8c6;
    color: #222;
}

.chat-image {
    max-width: 220px;
    max-height: 220px;
    border-radius: 12px;
    display: block;
}

.chat-text {
    font-size: 16px;
    line-height: 1.5;
}
</style>
