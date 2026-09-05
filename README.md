# UTFPR Certificate Extractor

This is a script to extract data from standard UTFPR certificates for
extracurricular activities inside a folder.
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
See [INSTALL](./INSTALL.md)

## Run the script

### Linux
```sh
python3 main.py <input_dir> [output_dir]
```

### Windows
```sh
python main.py <input_dir> [output_dir]
```

## License
[GPLv3](./LICENSE)

Copyright 2026 Omar Zagonel El Laden
