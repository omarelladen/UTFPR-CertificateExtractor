import sys
import csv
import re
import os

from pypdf import PdfReader


PATTERN_NUM = r"\d+"
PATTERN_WORD = r"[A-Za-zÀ-ÿ\s]+"
PATTERN_STR = ".*"
PATTERN_EVENT = "evento"

map_replace = {
    "\n":   " ",
    "\xa0": " ",
    "    ": " ",
    "   ":  " ",
    "  ":   " ",
    "projeto": "evento",
}


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


        RE_1 = fr"Declaramos que ({PATTERN_WORD}) participou" \
               fr" como ({PATTERN_WORD}) do {PATTERN_EVENT}" \
               fr" de extensão ({PATTERN_STR}), promovido" \
               fr" pelo\(a\) ({PATTERN_STR}) da" \
               fr" ({PATTERN_STR}), realizado" \
               fr" no período de ({PATTERN_STR})" \
               fr" dedicando ({PATTERN_NUM}) hora\(s\)." \
               fr" Emitida pelo ({PATTERN_WORD})" \
               fr" a autenticidade deste documento pode ser verificada" \
               fr" através da URL: ({PATTERN_STR})"

        m1 = re.search(RE_1, text)
        if m1:
            name  = m1.group(1)
            role  = m1.group(2)
            event = m1.group(3)
            dep   = m1.group(4)
            org   = m1.group(5)
            date  = m1.group(6)
            hours = m1.group(7)
            emit  = m1.group(8)
            url   = m1.group(9)

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


def save_csv(path, list_data):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(list_data)


print("Failed to extract data from:")
for f in list_failed:
    print("-", f[0])
print()


print(f"Total hours: {total_hours}\n")


hours_path = os.path.join("output", "hours.txt")
save_csv(hours_path, [[total_hours]])
print(f"Total hours saved in {hours_path}")

extracted_data_path = os.path.join("output", "extracted_data.csv")
save_csv(extracted_data_path, list_data)
print(f"Extracted data saved in {extracted_data_path}")

errors_path = os.path.join("output", "erros.csv")
save_csv(errors_path, list_failed)
print(f"Errors saved in {errors_path}")
