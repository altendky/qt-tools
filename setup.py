import os
import setuptools
import versioneer

import _build
import local_backend


qt_tools_wrapper_version = versioneer.get_versions()['version']
qt_tools_version = '{}.{}'.format(
    local_backend.qt_version,
    qt_tools_wrapper_version,
)


with open('README.rst') as f:
    readme = f.read()

# TODO: CAMPid 98743987416764218762139847764318798
qt_major_version = os.environ['QT_VERSION'].partition('.')[0]


if qt_major_version == '5':
    replacements = [
        ["qt6", "qt5"],
        ["Qt6", "Qt5"],
        ["Qt6", "Qt 5"],
        ["6.4", "5.15"],
    ]
    for a, b in replacements:
        readme = readme.replace(a, b)


distribution_name = "qt{}-tools".format(qt_major_version)
import_name = distribution_name.replace('-', '_')


setuptools.setup(
    name=distribution_name,
    description="Wrappers for the raw Qt programs from qt{}-applications".format(qt_major_version),
    long_description=readme,
    long_description_content_type='text/x-rst',
    url='https://github.com/altendky/qt-tools',
    author="Kyle Altendorf",
    author_email='sda@fstab.net',
    license='LGPLv3',
    classifiers=[
        # complete classifier list: https://pypi.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
    cmdclass={'build_py': _build.BuildPy},
    packages=[
        package.replace('qt_', 'qt{}_'.format(qt_major_version))
        for package in setuptools.find_packages('src')
    ],
    package_dir={import_name: 'src/qt_tools'},
    version=qt_tools_version,
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=[
        local_backend.qt_applications_requirement,
        'click',
    ],
    entry_points={
        'console_scripts': ['qt{major}-tools = qt{major}_tools.entrypoints:main'.format(major=qt_major_version)],
    }
)
