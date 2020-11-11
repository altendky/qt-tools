import os
import sys
import sysconfig

import qt5_applications


from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


fspath = getattr(os, 'fspath', str)


def add_to_env_var_path_list(environment, name, before, after):
    return {
        name: os.pathsep.join((
            *before,
            environment.get(name, ''),
            *after
        ))
    }


def create_environment(reference):
    environment = dict(reference)

    if sys.platform == 'linux':
        environment.update(add_to_env_var_path_list(
            environment=environment,
            name='LD_LIBRARY_PATH',
            before=[''],
            after=[sysconfig.get_config_var('LIBDIR')],
        ))
    if sys.platform == 'win32':
        environment.update(add_to_env_var_path_list(
            environment=environment,
            name='PATH',
            before=[''],
            after=[sysconfig.get_path('scripts')],
        ))

    return environment
