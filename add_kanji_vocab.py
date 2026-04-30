import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python add_kanji_vocab.py input.txt output.txt")
        sys.exit(1)

    with open(sys.argv[1], "r", encoding="utf-8") as f:
        lines = f.readlines()

    output_lines = []

    for line in lines:
        if line.startswith("#"):
            if line.startswith("#tags column:"):
                col = int(line.strip().split(":")[1])
                line = f"#tags column:{col + 1}\n"
            output_lines.append(line)
            continue

        if not line.strip():
            output_lines.append(line)
            continue

        fields = line.rstrip("\n").split("\t")

        if len(fields) < 7:
            output_lines.append(line)
            continue

        kanji = fields[2]          # col 3 (0-indexed 2) — the target kanji
        vocab_maru = fields[5]     # col 6 (0-indexed 5) — vocab with ○

        vocab_kanji = vocab_maru.replace("○", kanji)

        fields.insert(6, vocab_kanji)  # insert after col 6, pushing col 7+ right

        output_lines.append("\t".join(fields) + "\n")

    with open(sys.argv[2], "w", encoding="utf-8") as f:
        f.writelines(output_lines)

    print(f"Done! Output saved to: {sys.argv[2]}")

if __name__ == "__main__":
    main()
