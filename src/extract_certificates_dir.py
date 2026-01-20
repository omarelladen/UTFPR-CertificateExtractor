import sys
import csv
import re
import os

from pypdf import PdfReader


OUTPUT_DIR = "output"

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

RE_STD = fr"Declaramos que ({PATTERN_WORD}) participou" \
       fr" como ({PATTERN_WORD}) do {PATTERN_EVENT}" \
       fr" de extensão ({PATTERN_STR}), promovido" \
       fr" pelo\(a\) ({PATTERN_STR}) da" \
       fr" ({PATTERN_STR}), realizado" \
       fr" no período de ({PATTERN_STR})" \
       fr" dedicando ({PATTERN_NUM}) hora\(s\)." \
       fr" Emitida pelo ({PATTERN_WORD})" \
       fr" a autenticidade deste documento pode ser verificada" \
       fr" através da URL: ({PATTERN_STR})"


def save_csv(path, list_data):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(list_data)


if len(sys.argv) < 2:
    sys.exit(1)
dir_path = sys.argv[1]

if not os.path.isdir(dir_path):
    sys.exit(1)


list_data = []
list_failed = []
total_hours = 0
for f in os.listdir(dir_path):
    full_path = os.path.join(dir_path, f)
    if os.path.isfile(full_path) and f.lower().endswith(".pdf"):

        reader = PdfReader(full_path)
        page = reader.pages[0]
        text = page.extract_text()

        for old, new in map_replace.items():
            text = text.replace(old, new)


        m = re.search(RE_STD, text)
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


os.makedirs(OUTPUT_DIR, exist_ok=True)

hours_path = os.path.join(OUTPUT_DIR, "hours.txt")
save_csv(hours_path, [[total_hours]])
print(f"Total hours saved in {hours_path}")

extracted_data_path = os.path.join(OUTPUT_DIR, "extracted_data.csv")
save_csv(extracted_data_path, list_data)
print(f"Extracted data saved in {extracted_data_path}")

errors_path = os.path.join(OUTPUT_DIR, "errors.csv")
save_csv(errors_path, list_failed)
print(f"Errors saved in {errors_path}")
