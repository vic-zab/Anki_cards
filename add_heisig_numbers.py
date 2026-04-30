"""
Add sequential Heisig numbers to an Anki tab-separated export file.

Usage:
    python add_heisig_numbers.py input.txt output.txt

- Cards must be sorted by creation date (Heisig order) before exporting.
- The script preserves all header comment lines (#separator, #html, etc.)
- Writes clean UTF-8 output ready for Anki import.
"""

import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python add_heisig_numbers.py input.txt output.txt")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    # Read the file as raw text to avoid csv module quoting headaches
    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    output_lines = []
    heisig_number = 1

    for line in lines:
        # Preserve Anki header comments as-is
        if line.startswith("#"):
            output_lines.append(line)
            continue

        # Skip blank lines
        if not line.strip():
            output_lines.append(line)
            continue

        # Split on tabs — Anki uses plain tab separation
        fields = line.rstrip("\n").split("\t")

        if len(fields) < 2:
            output_lines.append(line)
            continue

        # Column 0 = GUID, Column 1 = Heisig count
        # Set the Heisig count to the sequential number
        fields[1] = str(heisig_number)
        heisig_number += 1

        output_lines.append("\t".join(fields) + "\n")

    # Write as UTF-8 (no BOM)
    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(output_lines)

    print(f"Done! Assigned Heisig numbers 1–{heisig_number - 1}.")
    print(f"Output saved to: {output_path}")
    print()
    print("To import in Anki:")
    print("  1. File → Import")
    print(f"  2. Select '{output_path}'")
    print("  3. Set 'Update existing notes when first field matches'")
    print("  4. Make sure field mapping is correct")
    print("  5. Import")

if __name__ == "__main__":
    main()