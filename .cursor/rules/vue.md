---
description: Vue 3 SFC conventions for this project
globs: ["**/*.vue"]
alwaysApply: false
---

- Use the Vue 3 Composition API with the order: script, template, style.
- Always include required imports (`defineComponent`, `ref`, `computed`, etc.) from `vue`.
- Name components clearly and consistently using PascalCase.
- Use `<script setup>` syntax for single-file components.
- Ensure all props are typed using TypeScript.
- Use `defineProps` and `defineEmits` for props and events.
- Prefer `ref` for reactive primitives, and `reactive` for objects.
- Use `watch` and `watchEffect` for side effects.
- Always include a `<template>` section with clear, readable markup.
- Use scoped CSS in the `<style scoped>` block.
- Use comments only where necessary for clarity.
- Prefer composition over inheritance.
- Avoid global state unless absolutely necessary; use `provide`/`inject` or state management libraries (e.g., Pinia) when needed.
