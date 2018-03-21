#!/usr/bin/python3

# use debian.deb822 to parse Packages / Sources file.

####

import os
import os.path
import debian
import debian.deb822

from debian.deb822 import Release
from debian.deb822 import Packages
from debian.deb822 import Sources

# GLOBAL VARIABLES

REPO_BASEDIR = '/srv/repo/aptly/public'

# CLASS DEFINITION

class ReleaseRepo(Release):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.components = {}
        for i in self['Components'].split(' '):
            self.components[str(i)] = None
        pass # TODO FIXME

    def get_components(self) -> list:
        """Send Component list for this codename(Release).
        """
        return self['Components'].split(' ')

def parse_debrepo_arch(basedir: str) -> list:
    """
    Parse certain arch dir.

    Structure:
    * Packages
    * Release (stripped)
    """
    result_data = []
    with open(os.path.join(basedir, 'Packages')) as f:
        while True:
            p = dict(Packages(f))
            if p == {}:
                break
            result_data.append(p)
    return result_data

def parse_debrepo_component(basedir: str) -> dict:
    """
    Parse a certain component dir.

    Structures:
    * Contents-$arch.gz
    * binary-$arch/
    * source/
    """
    for root, dirs, files in os.walk(basedir):
        _archs = dirs.copy()
        break
    archs = []
    component_object = {}

    for i in _archs:
        if i == 'source':
            archs.append(i)
        if i[:7] == 'binary-':
            archs.append(i[7:])

    for i in archs:
        if i == 'source':
            pass # XXX: complete source detection
        else:
            component_object[i] = parse_debrepo_arch(os.path.join(basedir, 'binary-' + str(i)))
        pass

    return component_object

def parse_debrepo_codename(basedir:str):
    """
    Parse dists information in a given codename directory.

    Files to process:
    * Release
    * InRelease (Optional, the gpg-signed version of Release
    * main/ or contrib/ or nonfree/ : component directories
    """
    with open(os.path.join(basedir, 'Release')) as f:
        release_info = ReleaseRepo(f)

    "That's not enough. We need to fill release_info.components."
    for i in release_info.components:
        release_info.components[i] = parse_debrepo_component(
                os.path.join(basedir, str(i)),
                )

    return release_info

def parse_debrepo(basedir:str=REPO_BASEDIR) -> dict:
    """
    Main function to get a structured Debian Repository information
    from a given directory.
    """
    "First of all, find out how many distribution codename exists."
    _codenames = []
    for root, dirs, files in os.walk(os.path.join(basedir, 'dists')):
        _codenames = dirs.copy()
        break
    pass
    "Next, we need to exclude symlink in codename list."
    codenames = []
    for i in _codenames:
        if not os.path.islink(os.path.join(basedir, 'dists', i)):
            codenames.append(i)
    del _codenames
    result = {}
    for i in codenames:
        result[i] = parse_debrepo_codename(os.path.join(basedir, 'dists', i))
    return result

def debrepo_object_jsonify(r):
    """
    Do the dirty job to jsonify the damn object.
    """

def main():
    print(parse_debrepo())
    pass

if __name__ == '__main__':
    main()
