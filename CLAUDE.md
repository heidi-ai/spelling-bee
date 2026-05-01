# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A minimal Python CLI tool for managing a spelling bee word list. Two files matter: `bee.py` (the script) and `words.txt` (the word database).

## Running the Tool

```bash
python3 bee.py export              # print all words to stdout
python3 bee.py add WORD [WORD...]  # add one or more words
python3 bee.py search PREFIX       # list words starting with prefix
```

The script locates `words.txt` relative to its own file path (`__file__`), not the working directory, so it works from any directory.

## How Words Are Stored

`words.txt` is a plain newline-separated file. On every write, `save_words` sorts all words alphabetically and deduplicates them. Words are always stored and compared lowercase. There is no schema or format beyond one word per line.

## No Test Suite or Linter

There are no tests, no linter config, and no dependencies beyond the Python standard library. Verify behavior by running the commands directly.
