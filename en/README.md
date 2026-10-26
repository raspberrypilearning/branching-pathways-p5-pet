# Learner source

Named route Markdown files are canonical. `pathways.yml` orders the menu; `meta.yml` and `step_N.md` support project-format consumers. The website is built from the same Markdown using `scripts/build-web.py`.

Run `python3 scripts/sync-pathway-files.py` after editing. The starter is maintained in `starters/pet.py`; sync copies it into the resource and editor-project folders. The setup page uses a checked copy of that code.
