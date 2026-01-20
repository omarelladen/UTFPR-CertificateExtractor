import sys
import re

from pypdf import PdfReader


if len(sys.argv) < 2:
    sys.exit(1)
pdf_path = sys.argv[1]


reader = PdfReader(pdf_path)
page = reader.pages[0]
text = page.extract_text()
print(repr(text))


map_replace = {
    "\n":   " ",
    "\xa0": " ",
    "    ": " ",
    "   ":  " ",
    "  ":   " ",
}
for old, new in map_replace.items():
    text = text.replace(old, new)
print(repr(text))

