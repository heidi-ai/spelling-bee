#!/usr/bin/env python3
import sys
import os
import subprocess
from datetime import datetime, timezone, timedelta

WORDS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "words.txt")
MOUNTAIN_TZ = timezone(timedelta(hours=-6))  # MDT (UTC-6)


def to_mountain(dt):
    return dt.astimezone(MOUNTAIN_TZ)


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
    now = to_mountain(datetime.now(timezone.utc))
    if added:
        print(f"Added: {', '.join(sorted(added))}  [{now.strftime('%Y-%m-%d %H:%M MDT')}]")
    else:
        print("No new words (all duplicates).")


def cmd_search(prefix):
    prefix = prefix.lower()
    matches = [w for w in load_words() if w.startswith(prefix)]
    if matches:
        print_word_list(matches)
    else:
        print(f"No words starting with '{prefix}'.")


def cmd_history(n):
    result = subprocess.run(
        ["git", "log", "--format=%ad %s", "--date=iso-strict", "-n", str(n)],
        cwd=os.path.dirname(os.path.abspath(__file__)),
        capture_output=True, text=True,
    )
    for line in result.stdout.splitlines():
        parts = line.split(" ", 1)
        if len(parts) < 2:
            continue
        ts_str, subject = parts
        try:
            dt = datetime.fromisoformat(ts_str)
            mdt = to_mountain(dt)
            print(f"{mdt.strftime('%Y-%m-%d %H:%M MDT')}  {subject}")
        except ValueError:
            print(line)


def main():
    if len(sys.argv) < 2:
        print("Usage: bee.py export | add WORD... | search PREFIX | history [N]")
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
    elif command == "history":
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        cmd_history(n)
    else:
        print(f"Unknown command: {command}")
        print("Usage: bee.py export | add WORD... | search PREFIX | history [N]")
        sys.exit(1)


if __name__ == "__main__":
    main()
