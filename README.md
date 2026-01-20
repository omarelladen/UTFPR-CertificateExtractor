# UTFPR Certificate Extractor

This is a script to extract data from standard UTFPR certificates for 
extracurricular activities. This can help students count how many
hours they have spent and automatically create a CSV table with 
all the information.

## Install dependencies (Linux)
```sh
python3 -m venv .venv
source 
pip install pypdf
```

## Run
```sh
python3 src/extract_certificates_dir.py <dir>
```
