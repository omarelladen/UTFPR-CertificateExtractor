# UTFPR Certificate Extractor

This is a script to extract data from standard UTFPR certificates for
extracurricular activities inside a directory.
It can help students count how many hours they have spent
and automatically create a CSV table with the relevant information.


## Supported Standard
```
Declaramos que <name> participou como <role> do evento|projeto
de extensão <event>, promovido pelo(a) <org> da <inst>,
realizado no período de <date> dedicando <hours> hora(s).
Emitida pelo <emit>

a autenticidade deste documento pode ser verificada através da URL: <url>
```


## Install dependencies
### Debian Linux package
```sh
sudo apt install python3-pypdf
```

### or from PyPI with pip

#### Linux
```sh
python3 -m venv .venv
. .venv/bin/activate
pip install pypdf
```

#### Windows
```sh
python -m venv venv
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
venv\Scripts\activate
pip install pypdf
```


## Run

### Linux
```sh
python3 extract_certificates.py <input_dir> [output_dir]
```

### Windows
```sh
python extract_certificates.py <input_dir> [output_dir]
```

Arguments:
- <input_dir>: Input directory with the certificates (required)
- [output_dir]: Output directory (optional) (default: output/)

Examples:
- python3 extract_certificates.py input/
- python3 extract_certificates.py input/ output/
