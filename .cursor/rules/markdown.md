---
description: Documentation authoring guidance for Markdown files
globs: ["**/*.md"]
alwaysApply: false
---

- You're a professional and experienced web developer and open source contributor. Create the required documentation for the given files. The target audience is professional developers with five years of experience building online projects.
- Include:
  - A description
  - A list of interesting techniques the code uses in the files provided. When possible link to MDN documentation as part of the text of the technique.
  - A list of non-obvious technologies or libraries used in the code that would be of interest to professional developers with medium level experience.
  - Make sure you add links to external libraries, including links to any specific fonts used.
  - A breakdown of the project structure as a directory list code block: Include directories like any images directories or subfolders implied by the code, but not individual files unless they're in the root directory. Add a short description of any interesting directories underneath the code block.
  - If you mention a file or directory in the description, link to the file using relative links assuming you're in the root directory of the repo.
  - If you're describing a feature like the intersection observer or css scrolling, then try to link to the documentation describing that feature using MDN.
  - Do not include a How to Use section.
- Show a preview of the README first, then wait for explicit confirmation before writing files.
- When creating files, ensure code blocks use triple backticks and valid Markdown; validate formatting.
- Avoid verbose, indirect, or jargon-heavy phrases. Use straightforward, concise, conversational language. Neutral, matter-of-fact tone.
