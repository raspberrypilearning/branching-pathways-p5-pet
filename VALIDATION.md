# Validation

Checked 26 October 2026.

## Automated checks

- Nine Python checks cover the manifest, metadata, numbered copies, local links, illustration paths, starter copies, code snippets and menu order.
- Each of the 13 coding options runs when applied directly to the starter, using a p5 test double.
- 144 combinations of body, movement, reaction and home run with keyboard control and decorations added. These check shared coordinates, control calls and mood state; they do not replace testing the graphics library itself.
- Python source and all code snippets parse successfully. The web JavaScript passes Node's syntax check.
- Generated web pages are checked against the canonical Markdown. All 18 routes have a node in the pathway map.

## Browser checks

- In the Raspberry Pi Code Editor, the unchanged starter drew the pet and its click reaction changed the mouth and message.
- A combined version using ears, a hat, bouncing, random moods, keyboard input and a space background ran successfully in the same editor. Key input changed the mood/message while animation continued.
- An initial browser run found that the editor's p5 environment requires an explicit `from math import sin`. Both wave-based movement snippets now include that import inside their replacement function.
- All 18 website routes rendered their expected headings after the shared setup checkpoint. Before setup, choosing a part led back to the starter and then returned to the requested part.
- The copy-code button copied the complete function, including the import and indentation.
- Ticks and a typed note survived reloading the website. No browser console errors were observed during the route checks.
- The home page and a code lesson were inspected at desktop width. A 390-pixel iframe viewport was used to inspect the responsive phone layout; this is a layout check, not a physical-device test.

## Remaining scope

- No classroom study, physical touchscreen test or exhaustive test of every code combination inside the real editor has been performed.
- The dedicated editor-project slug is not registered. Setup deliberately opens the official blank Python starter and asks the learner to paste this repository's complete pet starter. The editor's Python and Download controls were confirmed in the live interface.
- Saved pathway notes are separate from Python project files. The learner must save or download their Python in the editor.
