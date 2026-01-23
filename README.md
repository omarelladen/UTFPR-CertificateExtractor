# UTFPR Certificate Extractor

This is a script to extract data from standard UTFPR certificates for
extracurricular activities. It can help students count how many
hours they have spent and automatically create a CSV table with
 the information.

## Supported Standard
```
Declaramos que <name> participou como <role> do evento|projeto
de extensão <event>, promovido pelo(a) <dep> da <org>,
realizado no período de <date> dedicando <hours> hora\(s\).
Emitida pelo <emit>
a autenticidade deste documento pode ser verificada através da URL: <url>
```

## Install dependencies (Linux)
```sh
python3 -m venv .venv
source .venv/bin/activate
pip install pypdf
```

## Run
```sh
source .venv/bin/activate
python3 src/extract_certificates.py <input_dir> [output_dir]
```
