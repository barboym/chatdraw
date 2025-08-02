import { nextTick } from 'vue'
import { describe, it, expect, beforeEach } from 'vitest'
import ChatWindow from '../ChatWindow.vue'
import ChatMessage from '../ChatMessage.vue'
import { mount } from '@vue/test-utils'
import type { SystemMessage } from '../setChat'

const mockMessages: SystemMessage[] = [
  {text: "Hi", isUser:true, isSketch:false},
  {text: "Hello!", isUser:false, isSketch:false}
]

describe('ChatWindow.vue', () => {
  let wrapper: ReturnType<typeof mount>

  beforeEach(() => {
    wrapper = mount(ChatWindow, {
      props: { messages: mockMessages },
      global: {
        components: { ChatMessage }
      }
    })
  })

  it('renders the correct number of ChatMessage components', () => {
    const chatMessages = wrapper.findAllComponents(ChatMessage)
    expect(chatMessages.length).toBe(mockMessages.length)
  })

  it('passes the correct message prop to each ChatMessage', () => {
    const chatMessages = wrapper.findAllComponents(ChatMessage)
    chatMessages.forEach((cm, idx) => {
      expect(cm.props('message')).toEqual(mockMessages[idx])
    })
  })

  it.skip('scrolls to bottom on mount', async () => {
    const chatWindowDiv = wrapper.find('.chat-window').element as HTMLDivElement
    chatWindowDiv.scrollTop = 0
    Object.defineProperty(chatWindowDiv, 'scrollHeight', {
      value: 1000,
      configurable: true,
    });
    await nextTick()
    await nextTick()
    expect(chatWindowDiv.scrollTop).toBe(chatWindowDiv.scrollHeight)
  })

  it('scrolls to bottom on update', async () => {
    const chatWindowDiv = wrapper.find('.chat-window').element as HTMLDivElement
    chatWindowDiv.scrollTop = 0
    Object.defineProperty(chatWindowDiv, 'scrollHeight', {
      value: 1000,
      configurable: true,
    });
    await wrapper.setProps({
      messages: [...mockMessages, { role: 'user', content: 'Another message' }]
    })
    await nextTick()
    expect(chatWindowDiv.scrollTop).toBe(chatWindowDiv.scrollHeight)
  })
})
