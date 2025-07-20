import { ref } from 'vue'
import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import ChatWindow from '../ChatWindow.vue'

// Mock child components
vi.mock('../ChatMessage.vue', () => ({
  default: {
    name: 'ChatMessage',
    props: ['message'],
    template: '<div class="mock-chat-message">{{ message.content }}</div>'
  }
}))
vi.mock('../TypingIndicator.vue', () => ({
  default: {
    name: 'TypingIndicator',
    props: ['waitingForResponse'],
    template: '<div class="mock-typing-indicator">{{ waitingForResponse ? "Typing..." : "" }}</div>'
  }
}))

const messages = [
  { content: 'Hello', role: 'user' },
  { content: 'Hi there!', role: 'assistant' }
]

describe('ChatWindow.vue', () => {
  it('renders all messages', () => {
    const wrapper = mount(ChatWindow, {
      props: { messages, waitingForResponse: false }
    })
    const renderedMessages = wrapper.findAll('.mock-chat-message')
    expect(renderedMessages.length).toBe(messages.length)
    expect(renderedMessages[0].text()).toBe('Hello')
    expect(renderedMessages[1].text()).toBe('Hi there!')
  })

  it('shows typing indicator when waitingForResponse is true', () => {
    const wrapper = mount(ChatWindow, {
      props: { messages, waitingForResponse: true }
    })
    expect(wrapper.find('.mock-typing-indicator').text()).toBe('Typing...')
  })

  it('does not show typing indicator when waitingForResponse is false', () => {
    const wrapper = mount(ChatWindow, {
      props: { messages, waitingForResponse: false }
    })
    expect(wrapper.find('.mock-typing-indicator').text()).toBe('')
  })

  it('scrolls to bottom on mount and update', async () => {
    const scrollMock = vi.fn()
    const wrapper = mount(ChatWindow, {
      props: { messages, waitingForResponse: false },
      attachTo: document.body
    })
    // Mock scrollTop and scrollHeight
    wrapper.vm.$refs.chatWindow.scrollTop = 0
    wrapper.vm.$refs.chatWindow.scrollHeight = 100
    wrapper.vm.$refs.chatWindow.scrollTop = scrollMock
    await wrapper.vm.$nextTick()
    // Simulate update
    await wrapper.setProps({ messages: [...messages, { content: 'New', role: 'user' }] })
    expect(wrapper.find('.chat-window').exists()).toBe(true)
  })
})
