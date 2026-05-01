#!/usr/bin/env python3
import sys
import os

WORDS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "words.txt")


def load_words():
    if not os.path.exists(WORDS_FILE):
        return []
    with open(WORDS_FILE) as f:
        return [w.strip().lower() for w in f if w.strip()]


def save_words(words):
    with open(WORDS_FILE, "w") as f:
        f.write("\n".join(sorted(set(words))) + "\n" if words else "")


def print_word_list(words):
    for i, word in enumerate(words, 1):
        print(f"{i:3}. {word}")


def cmd_export():
    words = load_words()
    if words:
        print_word_list(words)


def cmd_add(new_words):
    words = set(load_words())
    added = []
    for w in new_words:
        w = w.lower()
        if w not in words:
            words.add(w)
            added.append(w)
    save_words(list(words))
    if added:
        print(f"Added: {', '.join(sorted(added))}")
    else:
        print("No new words (all duplicates).")


def cmd_search(prefix):
    prefix = prefix.lower()
    matches = [w for w in load_words() if w.startswith(prefix)]
    if matches:
        print_word_list(matches)
    else:
        print(f"No words starting with '{prefix}'.")


def main():
    if len(sys.argv) < 2:
        print("Usage: bee.py export | add WORD... | search PREFIX")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "export":
        cmd_export()
    elif command == "add":
        if len(sys.argv) < 3:
            print("Usage: bee.py add WORD1 WORD2 ...")
            sys.exit(1)
        cmd_add(sys.argv[2:])
    elif command == "search":
        if len(sys.argv) < 3:
            print("Usage: bee.py search PREFIX")
            sys.exit(1)
        cmd_search(sys.argv[2])
    else:
        print(f"Unknown command: {command}")
        print("Usage: bee.py export | add WORD... | search PREFIX")
        sys.exit(1)


if __name__ == "__main__":
    main()
