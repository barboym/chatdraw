import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import InputContainer from '../InputContainer.vue'

describe('InputContainer.vue', () => {
  it('renders input and button', () => {
    const wrapper = mount(InputContainer, {
      props: { submitFunction: vi.fn() }
    })
    expect(wrapper.find('input.input-field').exists()).toBe(true)
    expect(wrapper.find('button.send-button').exists()).toBe(true)
  })

  it('calls submitFunction with message on button click', async () => {
    const submitFn = vi.fn()
    const wrapper = mount(InputContainer, {
      props: { submitFunction: submitFn }
    })
    const input = wrapper.find('input.input-field')
    await input.setValue('Hello world')
    await wrapper.find('button.send-button').trigger('click')
    expect(submitFn).toHaveBeenCalledWith('Hello world')
    expect((input.element as HTMLInputElement).value).toBe('')
  })

  it('does not call submitFunction when input is empty', async () => {
    const submitFn = vi.fn()
    const wrapper = mount(InputContainer, {
      props: { submitFunction: submitFn }
    })
    await wrapper.find('button.send-button').trigger('click')
    expect(submitFn).not.toHaveBeenCalled()
  })

  it('submits on Enter key', async () => {
    const submitFn = vi.fn()
    const wrapper = mount(InputContainer, {
      props: { submitFunction: submitFn }
    })
    const input = wrapper.find('input.input-field')
    await input.setValue('Test Enter')
    await input.trigger('keyup.enter')
    expect(submitFn).toHaveBeenCalledWith('Test Enter')
    expect((input.element as HTMLInputElement).value).toBe('')
  })
})
