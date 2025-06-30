<!DOCTYPE html>
<html>
<head>
    <title>Simple Chat - Vue</title>
    <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
</head>
<body>
    <div id="app">
        <div class="chat-container">
            <div class="chat-messages" ref="messagesContainer">
                <div 
                    v-for="message in messages" 
                    :key="message.id"
                    :class="['message', message.type === 'user' ? 'user-message' : 'bot-message']">
                    {{ message.text }}
                </div>
            </div>
            <div class="chat-input">
                <input 
                    type="text" 
                    v-model="userInput" 
                    @keyup.enter="sendMessage"
                    placeholder="Type your message...">
                <button @click="sendMessage">Send</button>
            </div>
        </div>
    </div>

    <script>
        const { createApp } = Vue;

        createApp({
            data() {
                return {
                    userInput: '',
                    messages: [],
                    messageId: 0
                }
            },
            methods: {
                sendMessage() {
                    if (this.userInput.trim() === '') return;
                    
                    // Add user message
                    this.messages.push({
                        id: this.messageId++,
                        text: this.userInput,
                        type: 'user'
                    });
                    
                    // Clear input
                    this.userInput = '';
                    
                    // Add bot response after a short delay
                    setTimeout(() => {
                        this.messages.push({
                            id: this.messageId++,
                            text: 'hello',
                            type: 'bot'
                        });
                        this.scrollToBottom();
                    }, 500);
                    
                    this.scrollToBottom();
                },
                
                scrollToBottom() {
                    this.$nextTick(() => {
                        const container = this.$refs.messagesContainer;
                        container.scrollTop = container.scrollHeight;
                    });
                }
            }
        }).mount('#app');
    </script>

    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #e8f5e8;
            margin: 0;
            padding: 20px;
        }
        
        .chat-container {
            max-width: 700px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            height: 500px;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        
        .chat-messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            background-color: #fafafa;
        }
        
        .message {
            margin-bottom: 12px;
            padding: 10px 15px;
            border-radius: 20px;
            max-width: 80%;
            word-wrap: break-word;
        }
        
        .user-message {
            background-color: #4285f4;
            color: white;
            margin-left: auto;
            text-align: right;
        }
        
        .bot-message {
            background-color: #f1f3f4;
            color: #3c4043;
            border: 1px solid #e8eaed;
        }
        
        .chat-input {
            display: flex;
            padding: 20px;
            border-top: 1px solid #e8eaed;
            background: white;
            gap: 10px;
        }
        
        .chat-input input {
            flex: 1;
            padding: 12px 16px;
            border: 1px solid #dadce0;
            border-radius: 24px;
            outline: none;
            font-size: 14px;
        }
        
        .chat-input input:focus {
            border-color: #4285f4;
            box-shadow: 0 0 0 1px #4285f4;
        }
        
        .chat-input button {
            padding: 12px 24px;
            background-color: #4285f4;
            color: white;
            border: none;
            border-radius: 24px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            transition: background-color 0.3s;
        }
        
        .chat-input button:hover {
            background-color: #3367d6;
        }
        
        .chat-input button:active {
            background-color: #2b5ce6;
        }
    </style>
</body>
</html>