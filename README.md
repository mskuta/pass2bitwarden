# pass2bitwarden

A Python script to export data from [Pass](https://www.passwordstore.org/) in [Bitwarden](https://bitwarden.com/) CSV format. This started as a quick and dirty script to move my passwords to Bitwarden, but it turned out worthy of being shared.

Inspired by [reinefjord/pass2csv](https://github.com/reinefjord/pass2csv), but rewritten from scratch. There's probably some similarities.

Like pass2csv, this script needs [python-gnupg](https://pypi.org/project/python-gnupg/) and Python 3.

## Config

Currently, the parsed fields and any resulting formatting with regexp group matches or functions can be done in a `config.py` file.

The script exports data in the [Bitwarden .csv format](https://bitwarden.com/help/condition-bitwarden-import/).

The GPG encrypted password store data is decrypted and processed. As an example: `login_password` is grabbed from the first line of the data, `login_uri` is matched with `^url ?: ?(.*)$` and the `type` is always `login`.

Most likely, the `fields` and `notes` parsing could be implemented in some nice way by default. Feel free to create pull requests.

## Usage

```
$ ./pass2bitwarden.py -h
usage: pass2bitwarden.py [-h] [--directory DIRECTORY] [--gpg-binary BINARY]
                         [--output-file OUTPUT] [--gpg-agent]

Exports a .csv for import into Bitwarden/Vaultwarden from Pass.

options:
  -h, --help            show this help message and exit
  --directory DIRECTORY, -d DIRECTORY
                        Directory of the password store.
  --gpg-binary BINARY, -b BINARY
                        Path to the GPG binary.
  --output-file OUTPUT, -o OUTPUT
                        File to write the CSV in. If OUTPUT is -, standard output is being used.
  --gpg-agent, -a       Use GPG agent.
```

Example:

```
$ ./pass2bitwarden.py -d ~/.password-store/subdir -a -o only_subdir.csv
```
