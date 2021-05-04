import os
import pathlib
import subprocess
import sys
import sysconfig

import pytest


fspath = getattr(os, 'fspath', str)

scripts_path = pathlib.Path(sysconfig.get_path('scripts'))


def test_designer():
    with pytest.raises(subprocess.TimeoutExpired):
        subprocess.run(
            [
                fspath(scripts_path.joinpath('qt5-tools')),
                'designer',
            ],
            check=True,
            env={'QT_DEBUG_PLUGINS': '1'},
            timeout=10,
        )


def test_qmlscene():
    with pytest.raises(subprocess.TimeoutExpired):
        subprocess.run(
            [
                fspath(scripts_path.joinpath('qt5-tools')),
                'qt5qmlscene',
            ],
            check=True,
            env={'QT_DEBUG_PLUGINS': '1'},
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
