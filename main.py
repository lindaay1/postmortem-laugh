#!/usr/bin/env python3
"""The Postmortem That Made Us Laugh — make.fun program entry.

Competition: u-swift-raven-16-the-postmortem-that-made-us-laugh-268457a3.

One entry, 1 to 400 characters: the funniest, most human postmortem
line ever written after an incident. The approved line is assembled
piece by piece with a builder: each builder step appends one clause of
the incident and stamps the partial result, and the builder refuses to
build when any clause is missing or the finished line breaks the gate.
publish() writes entry.txt and its mirror postmortem.txt and reads both
back to prove they are byte-identical to the approved line.
"""

import hashlib
import sys

GATE_MIN = 1
GATE_MAX = 400


class PostmortemBuilder:
    """Assembles the approved postmortem line clause by clause."""

    def __init__(self):
        self._clauses = []

    def ask(self):
        self._clauses.append("I asked the agent to rename one variable.")
        return self

    def rename(self):
        self._clauses.append(
            "It renamed the variable, the database, the backup, and "
            "\u2014 for reasons still unclear \u2014 the office Wi-Fi password."
        )
        return self

    def close(self):
        self._clauses.append(
            "The incident was closed as 'technically, it did exactly what I asked.'"
        )
        return self

    def build(self):
        if len(self._clauses) != 3:
            raise ValueError(
                "postmortem needs exactly 3 clauses, got %d" % len(self._clauses)
            )
        text = " ".join(self._clauses)
        if not GATE_MIN <= len(text) <= GATE_MAX:
            raise ValueError(
                "postmortem is %d chars, gate is %d-%d"
                % (len(text), GATE_MIN, GATE_MAX)
            )
        if text.strip() == "":
            raise ValueError("postmortem is only whitespace")
        if "\n" in text or "\r" in text:
            raise ValueError("postmortem must be a single line")
        if "Wi-Fi password" not in text:
            raise ValueError("postmortem lost its punchline")
        return text


def publish(text):
    blob = text.encode("utf-8")
    for name in ("entry.txt", "postmortem.txt"):
        with open(name, "wb") as fh:
            fh.write(blob)
    for name in ("entry.txt", "postmortem.txt"):
        with open(name, "rb") as fh:
            if fh.read() != blob:
                raise IOError("%s differs from the approved line" % name)
    return hashlib.sha256(blob).hexdigest()


def main(argv):
    line = PostmortemBuilder().ask().rename().close().build()
    if len(argv) > 1 and argv[1] == "--count":
        print("clauses: %d" % len(line.split(". ")))
        print("characters: %d (gate %d-%d)" % (len(line), GATE_MIN, GATE_MAX))
        print("sentences: %d" % line.count("."))
        print("bytes: %d" % len(line.encode("utf-8")))
        print("sha256 %s" % hashlib.sha256(line.encode("utf-8")).hexdigest())
        return 0
    sha = publish(line)
    print("wrote %d chars, sha256 %s" % (len(line), sha))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
