## Post-processing Prompt Style Guide

`post_processing` lets you post-process transcription output before it is pasted. Each directive lives on its own line inside the multi-line TOML string, and they are applied in the order shown below.

### Casing directives (choose one)
- `sentence case`, `sentence-case`, or `capitalize sentences` — capitalize the start of each sentence and lowercase the rest.
- `uppercase` or `upper` — turn the entire transcript into uppercase.
- `lowercase` or `lower` — turn the entire transcript into lowercase.

Only one casing mode is active at a time; if multiple casing directives appear, the last one wins.

### Prefix/Suffix directives
- `prepend: <text>` — prefix the final text with `<text>`.
- `append: <text>` — suffix the final text with `<text>`.

You can combine `prepend` and `append` with any casing directive. They are added after casing adjustments.

### Examples
```toml
# Make dictated text sentence case and tag it afterward
post_processing = """
sentence case
append: — dictated with Chirp
"""

# Force uppercase and flag dictated lines up front
post_processing = """
uppercase
prepend: >>
"""
```
