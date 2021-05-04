import os
import setuptools
import versioneer

import build
import local_backend


qt5_tools_wrapper_version = versioneer.get_versions()['version']
qt5_tools_version = '{}.{}'.format(
    local_backend.qt_version,
    qt5_tools_wrapper_version,
)


with open('README.rst') as f:
    readme = f.read()


# TODO: CAMPid 98743987416764218762139847764318798
qt_major_version = os.environ['QT_VERSION'].partition('.')[0]


distribution_name = "qt{}-tools".format(qt_major_version)
import_name = distribution_name.replace('-', '_')


setuptools.setup(
    name=distribution_name,
    description="Wrappers for the raw Qt programs from qt5-applications",
    long_description=readme,
    long_description_content_type='text/x-rst',
    url='https://github.com/altendky/qt-tools',
    author="Kyle Altendorf",
    author_email='sda@fstab.net',
    license='LGPLv3',
    classifiers=[
        # complete classifier list: https://pypi.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: Developers',
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
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
    cmdclass={'build_py': build.BuildPy},
    packages=setuptools.find_packages('src'),
    package_dir={import_name: 'src/qt_tools'},
    version=qt5_tools_version,
    include_package_data=True,
    python_requires=">=3.5",
    install_requires=[
        local_backend.qt_applications_requirement,
        'click~=7.0',
    ],
    entry_points={
        'console_scripts': ['qt5-tools = qt5_tools.entrypoints:main'],
    }
)
