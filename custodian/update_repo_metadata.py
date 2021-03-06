#!/usr/bin/python3

# update_repo_metadata -- a daemon for updating repo metadata once an hour

from . import data_collector
import os
import os.path
import sys
import json
import time
import pathlib

# Export path
REPO_HOMEPAGE_DIR = '/srv/repo/aptly/public/'
REPO_INFO_DIR = os.path.join(REPO_HOMEPAGE_DIR, 'info/')
SLEEP_TIME = 3600

def _ensure_dir(dir_name: str = REPO_INFO_DIR):
    if not os.path.isdir(dir_name):
        try:
            os.unlink(dir_name)
        except:
            pass
        os.mkdir(dir_name)
    return

def _write_repodata(dir_name: str, rdata):
    f_codename = open(os.path.join(dir_name, 'codename.json'), 'w')
    f_codename.write(json.dumps(json.loads(str(rdata).replace("'", '"')))) # XXX: so hacky
    f_codename.close()
    for i in rdata:
        f = open(os.path.join(dir_name, i + '.json'), 'w')
        f.write(json.dumps(rdata[i].components))
        f.close()

def update_homepage():
    """cd /data/home; make update; """
    return
    os.system('sh -c "cd /data/home; git pull; make update;"')
    return

def main():
    print('Initializing update-repo-metadata daemon...')
    while True:
        print('Triggering repo metadata update...')
        r = data_collector.parse_debrepo()
        _ensure_dir(REPO_INFO_DIR)
        _write_repodata(REPO_INFO_DIR, r)

        update_homepage()
        print('Process complete!')
        time.sleep(SLEEP_TIME)
    pass

if __name__ == "__main__":
    main()
