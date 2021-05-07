import os
import pathlib
import subprocess
import sys

import pytest


fspath = getattr(os, 'fspath', str)

# TODO: CAMPid 0970432108721340872130742130870874321
import pkg_resources
major = int(pkg_resources.get_distribution(__name__.partition('.')[0]).version.partition(".")[0])


def test_designer():
    with pytest.raises(subprocess.TimeoutExpired):
        subprocess.run(
            [
                fspath(
                    pathlib.Path(sys.executable).with_name('qt{}-tools'.format(major)),
                ),
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
                fspath(
                    pathlib.Path(sys.executable).with_name('qt{}-tools'.format(major)),
                ),
                'qt{}qmlscene'.format(major),
            ],
            check=True,
            env={'QT_DEBUG_PLUGINS': '1'},
            timeout=10,
        )

# TODO: hangs on GHA
# def test_language():
#     completed_process = subprocess.run(
#         [
#             fspath(pathlib.Path(sys.executable).with_name('qtdiag')),
#         ],
#         check=True,
#         env={**os.environ, 'LANGUAGE': 'de_DE'},
#         stdout=subprocess.PIPE,
#         timeout=30,
#     )
#
#     assert b'de_DE' in completed_process.stdout
