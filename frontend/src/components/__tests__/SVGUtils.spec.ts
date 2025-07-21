import { describe, it, expect, beforeEach } from 'vitest'
import { createSvgFromPaths } from '../SVGUtils'

describe('createSvgFromPaths', () => {
  beforeEach(() => {
    // Reset DOM for each test
    document.body.innerHTML = ''
  })

  it('creates an SVG element with correct width, height, and viewBox', () => {
    const svg = createSvgFromPaths([], 400, 300)
    expect(svg.tagName).toBe('SVG')
    expect(svg.getAttribute('width')).toBe('400')
    expect(svg.getAttribute('height')).toBe('300')
    expect(svg.getAttribute('viewBox')).toBe('0 0 400 300')
    expect(svg.getAttribute('xmlns')).toBe('http://www.w3.org/2000/svg')
  })

  it('creates a path for each path in paths', () => {
    const paths = [
      [
        {x:10, y:10},
        {x:20, y:20},
        {x:30, y:40},
      ],
      [
        {x:100, y:100},
        {x:110, y:120},
      ],
    ]
    const svg = createSvgFromPaths(paths)
    const pathElements = svg.querySelectorAll('path')
    expect(pathElements.length).toBe(2)
  })

  it('sets correct attributes on path elements', () => {
    const paths = [
      [
        {x:5, y:5},
        {x:10, y:10},
      ],
    ]
    const svg = createSvgFromPaths(paths)
    const path = svg.querySelector('path')
    expect(path).not.toBeNull()
    expect(path!.getAttribute('stroke')).toBe('black')
    expect(path!.getAttribute('fill')).toBe('none')
    expect(path!.getAttribute('stroke-width')).toBe('2')
  })

  it('returns an SVG with no paths if input is empty', () => {
    const svg = createSvgFromPaths([])
    expect(svg.querySelectorAll('path').length).toBe(0)
  })

  it('skips empty path arrays', () => {
    const paths = [
      [],
      [
        {x:1, y:2},
        {x:3, y:4},
      ],
    ]
    const svg = createSvgFromPaths(paths)
    expect(svg.querySelectorAll('path').length).toBe(1)
  })

  it('generates correct "d" attribute for a single path', () => {
    const paths = [
      [
        {x:10, y:20},
        {x:15, y:25},
        {x:20, y:30},
      ],
    ]
    const svg = createSvgFromPaths(paths)
    const path = svg.querySelector('path')
    // The first command is always "M x y"
    expect(path!.getAttribute('d')).toMatch(/^M 10 20 L 5 5 L 5 5$/)
  })
})
