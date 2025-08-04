import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setChat } from '../setChat'

/*
Pseudocode:
1. Import necessary testing utilities from Vitest.
2. Import the setChat function and SystemMessage type.
3. Mock fetch to simulate API responses.
4. Test setChat initialization:
  - Default context value.
  - Custom context value.
  - Initial states of messages and waitingForResponse.
5. Test sendMessage:
  - Sending a text message updates waitingForResponse and messages.
  - Sending an image message updates messages correctly.
  - Handles API response and updates context.
  - Handles errors gracefully.
6. Test addMessages:
  - Adds text and image messages correctly.
  - Throws error for invalid mtype.
*/

const mockResponse = {
  response: [
    { mtype: 'text', content: 'Hello from API' },
    { mtype: 'image', content: 'base64imgdata' },
  ],
  next_context: 'next_context_value',
}

const mockFetch = vi.fn().mockResolvedValue({
  json: () => Promise.resolve(mockResponse),
})

globalThis.fetch = mockFetch as any

describe('setChat', () => {
  beforeEach(() => {
    mockFetch.mockClear()
  })

  it('initializes with default context', () => {
    const chat = setChat()
    expect(chat.messages.value).toEqual([])
  })

  it('initializes with custom context', () => {
    const chat = setChat('custom_context')
    expect(chat.messages.value).toEqual([])
  })

  it('sendMessage adds user text message and handles API response', async () => {
    const chat = setChat()
    await chat.sendMessage({ mtype: 'text', content: 'User message' })
    // First message is user text
    expect(chat.messages.value[0]).toMatchObject({
      text: 'User message',
      isSketch: false,
      isUser: true,
    })
    // API response messages
    expect(chat.messages.value[1]).toMatchObject({
      text: 'Hello from API',
      isSketch: false,
      isUser: false,
    })
    expect(chat.messages.value[2]).toMatchObject({
      imageUrl: 'data:image/png;base64,base64imgdata',
      isSketch: true,
      isUser: false,
    })
  })

  it('sendMessage adds user image message and handles API response', async () => {
    const chat = setChat()
    global.URL.createObjectURL = vi.fn(() => 'data:image/png;base64,userimgdata')
    await chat.sendMessage({ mtype: 'image', content: 'userimgdata' })
    expect(chat.messages.value[0]).toMatchObject({
      imageUrl: 'data:image/png;base64,userimgdata',
      isSketch: true,
      isUser: true,
    })
    // API response messages
    expect(chat.messages.value[1]).toMatchObject({
      text: 'Hello from API',
      isSketch: false,
      isUser: false,
    })
    expect(chat.messages.value[2]).toMatchObject({
      imageUrl: 'data:image/png;base64,base64imgdata',
      isSketch: true,
      isUser: false,
    })
  })

  it('addMessages throws error for invalid mtype', async () => {
    const chat = setChat()
    // @ts-expect-error: purposely passing invalid mtype
    const promise = chat.sendMessage({ mtype: 'invalid', content: 'oops' })
    await expect(promise).rejects.toThrow("Invalid mtype: must be either 'text' or 'image'")
  })

  it('handles fetch error gracefully', async () => {
    globalThis.fetch = vi.fn().mockRejectedValue(new Error('Network error')) as any
    const chat = setChat()
    await chat.sendMessage({ mtype: 'text', content: 'Test error' })
    // Only user message should be present
    expect(chat.messages.value[0]).toMatchObject({
      text: 'Test error',
      isSketch: false,
      isUser: true,
    })
    // Restore fetch
    globalThis.fetch = mockFetch as any
  })
})
