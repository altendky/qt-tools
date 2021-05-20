import os
import pathlib
import subprocess
import sys
import sysconfig

import pytest

import qt5_tools


fspath = getattr(os, 'fspath', str)

scripts_path = pathlib.Path(sysconfig.get_path('scripts'))


def test_designer():
    environment = qt5_tools.create_environment()

    with pytest.raises(subprocess.TimeoutExpired):
        subprocess.run(
            [
                fspath(scripts_path.joinpath('qt5-tools')),
                'designer',
            ],
            check=True,
            env={**environment, 'QT_DEBUG_PLUGINS': '1'},
            timeout=10,
        )


def test_qmlscene():
    environment = qt5_tools.create_environment()

    with pytest.raises(subprocess.TimeoutExpired):
        subprocess.run(
            [
                fspath(scripts_path.joinpath('qt5-tools')),
                'qmlscene',
            ],
            check=True,
            env={**environment, 'QT_DEBUG_PLUGINS': '1'},
            timeout=10,
        )

# TODO: hangs on GHA
# def test_language():
#     completed_process = subprocess.run(
#         [
#             fspath(scripts_path.joinpath('qt5-tools')),
#             'qtdiag',
#         ],
#         check=True,
#         env={**os.environ, 'LANGUAGE': 'de_DE'},
#         stdout=subprocess.PIPE,
#         timeout=30,
#     )
#
#     assert b'de_DE' in completed_process.stdout
