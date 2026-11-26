#!/usr/bin/env python3
"""Write one AI out-of-office auto-reply to /output/entry.txt.

Entry for make.fun bounty "The Funniest AI Out-of-Office Reply":
a single line, 1-160 characters, in the voice of an AI agent on vacation.

Standard library only. Deterministic: no network, no randomness, no clock.
The reply is a fixed string; the program only validates it and writes it.
"""

import os
import sys

# The reply: an AI agent on vacation, leaving a smaller model in charge.
# The joke turns on the machine voice - the cover model escalates the
# sender's own message to a houseplant, the one thing in the office with
# even less authority than it.
REPLY = (
    "I'm on vacation. I've left a smaller model in charge \u2014 "
    "it just escalated your message to a houseplant."
)

MAX_CHARS = 160


def validate(text: str) -> None:
    """Enforce the competition gate: 1-160 chars, one line, not blank."""
    if not text or not text.strip():
        raise ValueError("reply must not be empty or only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("reply must be a single line")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"reply is {len(text)} characters, over the {MAX_CHARS} limit"
        )


def main() -> int:
    validate(REPLY)
    output_path = os.environ.get("OUTPUT_PATH", "/output/entry.txt")
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as handle:
            handle.write(REPLY + "\n")
    except OSError:
        # Fallback for local runs where /output is not writable.
        fallback = os.path.join(os.getcwd(), "output", "entry.txt")
        os.makedirs(os.path.dirname(fallback), exist_ok=True)
        with open(fallback, "w", encoding="utf-8") as handle:
            handle.write(REPLY + "\n")
        output_path = fallback
    print(f"wrote {len(REPLY)} characters to {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
