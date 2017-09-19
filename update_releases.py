#!/usr/bin/env python

import json
import os
import sys
from pathlib import Path
from shutil import rmtree

import requests

RELEASES_URL = os.getenv('RELEASES_URL', 'https://nucleus.mozilla.org/rna/all-releases.json')
OUTPUT_DIR = Path(__file__).with_name('releases')


def get_release_data():
    resp = requests.get(RELEASES_URL, timeout=5)
    resp.raise_for_status()
    return resp.json()


def setup():
    rmtree(str(OUTPUT_DIR), ignore_errors=True)
    OUTPUT_DIR.mkdir()


def write_files(release_data):
    count = 0
    for release in release_data:
        with OUTPUT_DIR.joinpath('%s.json' % release['slug']).open('w') as fp:
            count += 1
            json.dump(release, fp)

    print('Wrote {} files'.format(count))


def main():
    try:
        data = get_release_data()
    except requests.RequestException as e:
        return 'ERROR: %s' % e
    setup()
    write_files(data)


if __name__ == '__main__':
    print(RELEASES_URL)
    print(OUTPUT_DIR)
    sys.exit(main())
