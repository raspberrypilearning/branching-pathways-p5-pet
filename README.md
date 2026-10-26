# My p5 Pet · Branching pathways

A pick-a-path project for learners aged 10–14. Learners write and edit **Python with p5** in the Raspberry Pi Code Editor to create a digital pet. This repository contains the learning website and Markdown instructions, not a pet-making configurator.

- [Live project](https://raspberrypilearning.github.io/branching-pathways-p5-pet/)
- [Markdown pathway](en/landing.md)
- [Starter Python](starters/pet.py)
- [Every-page route map](en/pathway-map.md)

## Learning design

Open the editor, paste the supplied working pet starter, run it and test its click reaction. This is the sole shared prerequisite. Learners then choose controls, body, movement, personality or home in any order. The sidebar suggests an order but does not require it. Examples are inspiration, not preset routes.

Every coding option replaces a complete named function in the same starter. Parts remain compatible: body, face and decorations use the same coordinates; controls call the reaction function; the draw loop calls each visual part. Alternatives targeting the same function replace one another. Pages state exactly what to replace and what to test.

The starter is supplied here because a dedicated hosted Raspberry Pi editor project has not been registered. Setup links to the official blank Python project and provides the full starter with a copy button. Learners save/download their Python in the editor. The pathway's Save notes/Open notes controls only export/import checks and notes. No code or notes are sent to a server by this site.

## Authoring and checks

Named Markdown pages in `en/` are canonical. The manifest, numbered copies, metadata and page-level route map follow the existing pathway format. Python's standard library builds the static web data; no package installation is needed.

```sh
python3 scripts/sync-pathway-files.py
python3 scripts/build-web.py
python3 scripts/sync-pathway-files.py --check
python3 scripts/build-web.py --check
python3 -m unittest discover -s tests -v
node --check app.js
python3 -m http.server 4198
```

GitHub Pages serves the repository root from `main`. The build check workflow verifies generated content and the learner examples. Runtime logic checks use a small p5 test double; browser checks in the real editor are documented in VALIDATION.md. Classroom testing is still valuable for pace and clarity.

## Sources and reuse

See [SOURCES.md](SOURCES.md) for the existing Python Bytes and Python Wild projects, editor documentation and interface provenance. Content and illustration are licensed under CC BY-SA 4.0; code under MIT. See LICENSE.md.
