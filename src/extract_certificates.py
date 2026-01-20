import sys
import csv
import re
import os

from pypdf import PdfReader


DEFAULT_OUTPUT_DIR = "output"

map_replace = {
    "\n":   " ",
    "\xa0": " ",
    "    ": " ",
    "   ":  " ",
    "  ":   " ",
    "projeto": "evento",
}

PATTERN_NUM = r"\d+"
PATTERN_WORD = r"[A-Za-zÀ-ÿ\s]+"
PATTERN_STR = ".*"
PATTERN_EVENT = "evento"

PATTERN_STD = (
    fr"Declaramos que ({PATTERN_WORD}) participou"
    fr" como ({PATTERN_WORD}) do {PATTERN_EVENT}"
    fr" de extensão ({PATTERN_STR}), promovido"
    fr" pelo\(a\) ({PATTERN_STR}) da"
    fr" ({PATTERN_STR}), realizado"
    fr" no período de ({PATTERN_STR})"
    fr" dedicando ({PATTERN_NUM}) hora\(s\)."
    fr" Emitida pelo ({PATTERN_WORD})"
    fr" a autenticidade deste documento pode ser verificada"
    fr" através da URL: ({PATTERN_STR})"
)


def save_csv(path, list_data):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(list_data)


if len(sys.argv) < 2:
    print(
        "Usage:\n"
        "  python3 src/extract_certificates.py <input_dir> [output_dir]\n"
        "\n"
        "Arguments:\n"
        "  <input_dir>   Input directory path (required)\n"
        "  [output_dir]  Output directory path (optional)\n"
       f"                (default: {DEFAULT_OUTPUT_DIR}/)\n"
        "\n"
        "Examples:\n"
        "  python3 src/extract_certificates.py data/\n"
        "  python3 src/extract_certificates.py data/ output/\n"
    )
    sys.exit(1)
input_dir = sys.argv[1]

if len(sys.argv) >= 3:
    output_dir = sys.argv[2]
else:
    output_dir = DEFAULT_OUTPUT_DIR

if not os.path.isdir(input_dir):
    print("Input directory not found!")
    sys.exit(1)


list_data = []
list_failed = []
total_hours = 0
for f in os.listdir(input_dir):
    full_path = os.path.join(input_dir, f)
    if os.path.isfile(full_path) and f.lower().endswith(".pdf"):

        reader = PdfReader(full_path)
        page = reader.pages[0]
        text = page.extract_text()

        for old, new in map_replace.items():
            text = text.replace(old, new)


        m = re.search(PATTERN_STD, text)
        if m:
            name  = m.group(1)
            role  = m.group(2)
            event = m.group(3)
            dep   = m.group(4)
            org   = m.group(5)
            date  = m.group(6)
            hours = m.group(7)
            emit  = m.group(8)
            url   = m.group(9)

            list_data.append([
                name,
                role,
                event,
                dep,
                org,
                date,
                hours,
                emit,
                url,
            ])

            total_hours += int(hours)

        else:
            list_failed.append([f])


print("Failed to extract data from:")
for f in list_failed:
    print("-", f[0])
print()


print(f"Total hours: {total_hours}\n")


os.makedirs(output_dir, exist_ok=True)

hours_path = os.path.join(output_dir, "hours.txt")
save_csv(hours_path, [[total_hours]])
print(f"Total hours saved in {hours_path}")

extracted_data_path = os.path.join(output_dir, "extracted_data.csv")
save_csv(extracted_data_path, list_data)
print(f"Extracted data saved in {extracted_data_path}")

errors_path = os.path.join(output_dir, "errors.txt")
save_csv(errors_path, list_failed)
print(f"Errors saved in {errors_path}")
