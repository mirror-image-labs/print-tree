# print-tree
Simple structured file printer for building LLM contexts.

# Usage
```bash
# get list of files
uv run print-tree ../reflection-runtime --summary

# copy list of files with contents to clipboard
uv run print-tree ../reflection-runtime | pbcopy
```

# Testing
```bash
uv run pytest
```