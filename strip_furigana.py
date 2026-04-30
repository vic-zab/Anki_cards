"""
Strip furigana bracket readings from the Expression field in an Anki export.

Turns  漢字[かんじ]  →  漢字
Only touches column 2 (Expression). All other fields stay untouched.

Usage:
    python strip_furigana.py input.txt output.txt
"""

import sys
import re

def strip_brackets(text):
    """Remove all [reading] brackets from a string."""
    return re.sub(r"\[[^\]]*\]", "", text)

def main():
    if len(sys.argv) != 3:
        print("Usage: python strip_furigana.py input.txt output.txt")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    output_lines = []
    count = 0

    for line in lines:
        if line.startswith("#") or not line.strip():
            output_lines.append(line)
            continue

        fields = line.rstrip("\n").split("\t")

        if len(fields) >= 3:
            original = fields[2]
            fields[2] = strip_brackets(original)
            if original != fields[2]:
                count += 1

        output_lines.append("\t".join(fields) + "\n")

    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(output_lines)

    print(f"Done! Cleaned furigana from {count} notes.")
    print(f"Output saved to: {output_path}")

if __name__ == "__main__":
    main()