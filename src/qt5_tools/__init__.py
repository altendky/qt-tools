import os
import sys
import sysconfig

import qt5_applications


from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


def bin_path():
    return qt5_applications._bin


def application_names():
    return qt5_applications._application_names()


def application_path(name):
    return qt5_applications._application_path(name)


def _add_to_env_var_path_list(environment, name, before, after):
    return {
        name: os.pathsep.join((
            *before,
            environment.get(name, ''),
            *after
        ))
    }


def create_environment(reference=None):
    if reference is None:
        reference = os.environ

    environment = dict(reference)

    if sys.platform in ['linux', 'darwin']:
        environment.update(_add_to_env_var_path_list(
            environment=environment,
            name='LD_LIBRARY_PATH',
            before=[''],
            after=[sysconfig.get_config_var('LIBDIR')],
        ))
    if sys.platform == 'win32':
        environment.update(_add_to_env_var_path_list(
            environment=environment,
            name='PATH',
            before=[''],
            after=[sysconfig.get_path('scripts')],
        ))

    return environment