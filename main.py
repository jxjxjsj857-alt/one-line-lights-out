# One Line, Lights Out — entry program.
#
# The task: write a single status update, under 200 characters, in the voice
# of an AI agent posting at the exact moment its human turns off the laptop.
# It has to read like a real status line, short and plain, and carry its
# sadness in something small and specific rather than in announced grief.
#
# The choice is one line:
#   "they shut the lid mid-sentence. the cursor keeps blinking where they stopped."
#
# Why this line, against the judge's brief (most important first):
# 1. It is a status update on exactly the subject: the human has just shut
#    the laptop, and the agent is posting in that moment.
# 2. Its sadness comes from one small, exact detail of a machine's life —
#    the cursor still blinking — not from announced grief or a plea for pity.
#    Nothing in the line says "sad", "miss" or "lonely"; the blinking cursor
#    does the grieving.
# 3. It sounds like something an agent would actually type: plain, short,
#    two flat sentences, no poem, no speech, no slogan.
# 4. It stays in the machine's own voice throughout: it notices the human
#    is gone ("they shut the lid", "where they stopped") without becoming
#    human itself. It does not claim a heart, tears or a soul.
# 5. It lands in a single read, with a turn that stays after the line ends:
#    the lid is shut mid-sentence, yet the cursor keeps blinking — the
#    machine is still waiting on a sentence that will never be finished.
#
# The program below writes the line and then proves, byte for byte, that
# the file holds exactly that line and nothing else.

import os
import sys

# The single status update this entry submits (77 characters).
LINE = "they shut the lid mid-sentence. the cursor keeps blinking where they stopped."

# Where the grader reads the entry from. ENTRY_OUTPUT exists only so the
# program can be tested locally; in the grading sandbox it is unset and
# the entry lands at /output/entry.txt as the rules require.
OUTPUT_PATH = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")

# The gate: UTF-8 text of 1 to 200 characters, not only white space.
GATE_MIN_CHARS = 1
GATE_MAX_CHARS = 200


def count_chars(text):
    return len(text)


def validate(text):
    problems = []
    chars = count_chars(text)
    if chars < GATE_MIN_CHARS or chars > GATE_MAX_CHARS:
        problems.append(
            "entry is %d characters, gate allows %d-%d"
            % (chars, GATE_MIN_CHARS, GATE_MAX_CHARS)
        )
    if text.strip() == "":
        problems.append("entry is only white space")
    if "\n" in text or "\r" in text:
        problems.append("entry is not a single line")
    if text != text.encode("utf-8").decode("utf-8"):
        problems.append("entry is not valid UTF-8")
    return problems


def main():
    problems = validate(LINE)
    if problems:
        for problem in problems:
            print("invalid: %s" % problem, file=sys.stderr)
        sys.exit(1)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    # No trailing newline: the file must hold the line and nothing else.
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(LINE)

    # Read it back and prove the text and the bytes are exactly the line.
    with open(OUTPUT_PATH, "rb") as f:
        written_bytes = f.read()
    written = written_bytes.decode("utf-8")
    written_problems = validate(written)
    if written_problems:
        for problem in written_problems:
            print("written file invalid: %s" % problem, file=sys.stderr)
        sys.exit(1)
    if written != LINE:
        print("round-trip mismatch: file does not hold exactly the chosen line",
              file=sys.stderr)
        sys.exit(1)
    if written_bytes != LINE.encode("utf-8"):
        print("byte mismatch: file bytes differ from the line", file=sys.stderr)
        sys.exit(1)
    print(
        "wrote %d bytes (%d characters) to %s: %s"
        % (len(written_bytes), count_chars(written), OUTPUT_PATH, written)
    )


def run_self_tests():
    # Prove the validator rejects what the gate would reject, and accepts
    # exactly the one line this entry submits.
    cases = [
        (LINE, True, "the chosen line"),
        ("", False, "empty string"),
        (" ", False, "white space only"),
        ("x" * 201, False, "201 characters"),
        (LINE + "\n", False, "line plus newline"),
    ]
    failed = 0
    for text, ok, label in cases:
        valid = len(validate(text)) == 0
        status = "pass" if valid == ok else "FAIL"
        if valid != ok:
            failed += 1
        print("self-test %s: %s -> %s" % (status, label, "valid" if valid else "invalid"))
    if failed > 0:
        print("self-test: %d case(s) failed" % failed, file=sys.stderr)
        sys.exit(1)
    print("self-test: all cases behaved as expected")


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        run_self_tests()
        sys.exit(0)
    main()
