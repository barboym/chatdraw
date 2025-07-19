/*
Pseudocode:
1. Import necessary testing utilities from Vue Test Utils.
2. Import the ChatMessage component.
3. Define a set of test cases:
  - Render a user message (text).
  - Render a system message (text).
  - Render a sketch message with image.
  - Render a sketch message without image (should fallback to text).
4. For each test case:
  - Mount the component with appropriate props.
  - Assert correct rendering of classes, text, and image.
*/

import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import ChatMessage from '../ChatMessage.vue'
import type { SystemMessage } from '../setChat'

const baseMessage: SystemMessage = {
  text: 'Hello world!',
  isUser: false,
  isSketch: false,
}

describe('ChatMessage.vue', () => {
  it('renders a system text message', () => {
    const wrapper = mount(ChatMessage, {
      props: { message: { ...baseMessage } },
    })
    expect(wrapper.find('.chat-message--system').exists()).toBe(true)
    expect(wrapper.find('.chat-text').text()).toBe('Hello world!')
    expect(wrapper.find('img').exists()).toBe(false)
  })

  it('renders a user text message', () => {
    const wrapper = mount(ChatMessage, {
      props: { message: { ...baseMessage, isUser: true } },
    })
    expect(wrapper.find('.chat-message--user').exists()).toBe(true)
    expect(wrapper.find('.chat-text').text()).toBe('Hello world!')
    expect(wrapper.find('img').exists()).toBe(false)
  })

  it('renders a sketch message with image', () => {
    const wrapper = mount(ChatMessage, {
      props: {
        message: {
          ...baseMessage,
          isSketch: true,
          imageUrl: 'https://example.com/sketch.png',
        },
      },
    })
    const img = wrapper.find('img')
    expect(img.exists()).toBe(true)
    expect(img.attributes('src')).toBe('https://example.com/sketch.png')
    expect(img.attributes('alt')).toBe('Sketch')
    expect(wrapper.find('.chat-text').exists()).toBe(false)
  })

  it('renders a sketch message without image as text', () => {
    const wrapper = mount(ChatMessage, {
      props: {
        message: {
          ...baseMessage,
          isSketch: true,
          imageUrl: '',
        },
      },
    })
    expect(wrapper.find('img').exists()).toBe(false)
    expect(wrapper.find('.chat-text').text()).toBe('Hello world!')
  })
})


