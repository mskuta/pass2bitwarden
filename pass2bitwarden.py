#!/usr/bin/env python3

import argparse
import csv
import re
import os
import sys

import gnupg

from config import CSV_FIELDS, FIELD_DEFAULTS, FIELD_FUNCTIONS, FIELD_PATTERNS

DOMAIN_REGEX_RAW = "^((?!-)[A-Za-z0-9-]" + "{1,63}(?<!-)\\.)" + "+[A-Za-z]{2,6}"
DOMAIN_REGEX = re.compile(DOMAIN_REGEX_RAW)


def traverse(directory):
    pass_files = []

    for root, dirs, files in os.walk(directory):
        if '.git' in dirs:
            dirs.remove('.git')

        for name in files:
            pass_files.append(os.path.join(root, name))

    return pass_files


def decrypt(files, binary, agent, verbose):
    gpg = gnupg.GPG(gpgbinary=binary,
                    use_agent=agent)
    gpg.encoding = 'utf-8'

    datas = []

    for path in files:
        file = os.path.splitext(path)[0]
        extension = os.path.splitext(path)[1]

        if extension == '.gpg':
            if verbose:
                print(f"Decrypting: {path}", file=sys.stderr)
            with open(path, 'rb') as gpg_file:
                decrypted = {
                    'path': file,
                    'data': str(gpg.decrypt_file(gpg_file))
                }

                datas.append(decrypted)

    return datas


def _guess_uri(row):
    if 'login_uri' not in row:
        return ''
    if re.search(DOMAIN_REGEX, row["name"]):
        return row["name"]
    return ''


def parse(base_dir, files, verbose):
    parsed = []

    for file in files:
        if verbose:
            print(f"Parsing: {os.path.basename(file['path'])}", file=sys.stderr)

        row = {}

        for field in CSV_FIELDS:
            if field in FIELD_DEFAULTS:
                row[field] = FIELD_DEFAULTS[field]
            elif field in FIELD_FUNCTIONS:
                row[field] = FIELD_FUNCTIONS[field](base_dir, file['path'], file['data'])
            elif field in FIELD_PATTERNS:
                try:
                    row[field] = re.search(FIELD_PATTERNS[field], file['data'], re.I | re.M).group(1)
                except AttributeError:
                    row[field] = ''
            else:
                row[field] = ''

        if row['login_uri'] == '':
            row['login_uri'] = _guess_uri(row)
        parsed.append(row)

    return parsed


def write(data, output_file):
    csv_file = sys.stdout if output_file == '-' else open(output_file, 'w', newline='')
    writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDS)
    writer.writeheader()
    for row in data:
        writer.writerow(row)
    if csv_file != sys.stdout:
        csv_file.close()


def main():
    parser = argparse.ArgumentParser(description='Exports a .csv for import into Bitwarden/Vaultwarden from Pass.')

    parser.add_argument('-a', '--gpg-agent', action='store_true', dest='agent',
                        help='use GPG agent')
    parser.add_argument('-b', '--gpg-binary', default='/usr/bin/gpg', dest='binary',
                        help='path to the GPG binary')
    parser.add_argument('-d', '--directory', default='~/.password-store',
                        help='directory of the password store')
    parser.add_argument('-o', '--output-file', default=os.path.splitext(os.path.basename(sys.argv[0]))[0] + '.csv', dest='output',
                        help='file to write the CSV in; if OUTPUT is -, standard output is being used')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='be verbose and display progress on standard error')

    args = parser.parse_args()

    password_store = os.path.expanduser(args.directory)

    encrypted_files = traverse(password_store)
    decrypted_files = decrypt(encrypted_files, args.binary, args.agent, args.verbose)

    csv_data = parse(password_store, decrypted_files, args.verbose)

    write(csv_data, args.output)


if __name__ == '__main__':
    main()
