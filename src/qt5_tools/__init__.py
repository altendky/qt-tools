import os
import sys

import qt5_applications


fspath = getattr(os, 'fspath', str)


from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


def bin_path():
    return qt5_applications._bin


def application_names():
    return qt5_applications._application_names()


def application_path(name):
    return qt5_applications._application_path(name)


def create_environment(reference=None):
    # noop for now, but just in case something needs added
    if reference is None:
        reference = os.environ

    return dict(reference)


def create_command_elements(name, sys_platform=sys.platform):
    path = application_path(name)

    if sys_platform == 'darwin' and path.suffix == '.app':
        inner = path.joinpath('Contents', 'MacOS', path.stem)
        return [fspath(inner)]

    return [fspath(path)]
