import os
import pathlib
import textwrap
import traceback
import typing

import setuptools.build_meta


build_wheel = setuptools.build_meta.build_wheel
build_sdist = setuptools.build_meta.build_sdist
prepare_metadata_for_build_wheel = (
    setuptools.build_meta.prepare_metadata_for_build_wheel
)
get_requires_for_build_sdist = (
    setuptools.build_meta.get_requires_for_build_sdist
)


class InvalidVersionError(Exception):
    pass


def pad_version(v, segment_count=3):
    split = v.split('.')

    if len(split) > segment_count:
        raise InvalidVersionError('{} has more than three segments'.format(v))

    return '.'.join(split + ['0'] * (segment_count - len(split)))


# TODO: really doesn't seem quite proper here and probably should come
qt_version = pad_version(os.environ.setdefault('QT_VERSION', '5.15.1'))
qt_major_version = qt_version.partition('.')[0]

# When using ~=, don't pad because that affects allowed versions.  The last
# segment is the one that is allowed to increase.
qt_applications_wrapper_version = '2.0'

# Must be False for release.  PyPI won't let you uplaod with a URL dependency.
use_qt_applications_url = True

if use_qt_applications_url:
    qt_applications_url = ' @ git+https://github.com/altendky/qt-applications@split_out_most'
    qt_applications_version_specifier = ''
else:
    qt_applications_url = ''
    qt_applications_version_specifier = '~={}.{}.dev0'.format(
        qt_version,
        qt_applications_wrapper_version,
    )


qt_applications_requirement = 'qt{}-applications{}{}'.format(
    qt_major_version,
    qt_applications_version_specifier,
    qt_applications_url,
)

requirements = {
    'attrs': '== 20.3',
    'setuptools': '~= 50.3',
    'versioneer-518': '== 0.18',
    'wheel': '~= 0.35.1',
}


def to_list(*dicts):
    merged = {}
    for d in dicts:
        merged.update(d)

    return [
        package + more
        for package, more in merged.items()
    ]


def get_requires_for_build_wheel(config_settings=None):
    return [*to_list(requirements), qt_applications_requirement]


def create_script_function_name(path: pathlib.Path):
    return path.stem.replace('-', '_')
