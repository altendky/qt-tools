import faulthandler
faulthandler.enable()

import os
import pathlib
import sys
import tempfile
import textwrap
import traceback
import typing

import attr
import qt5_applications
import setuptools.command.build_py


fspath = getattr(os, 'fspath', str)


class BuildPy(setuptools.command.build_py.build_py):
    def build_packages(self):
        super().build_packages()

        try:
            [package_name] = (
                package
                for package in self.distribution.packages
                if '.' not in package
            )

            build_command = self.distribution.command_obj['build']

            cwd = pathlib.Path.cwd()
            lib_path = cwd / build_command.build_lib
            package_path = lib_path / package_name

            results = build(package_path=package_path)

            if getattr(self.distribution, 'entry_points', None) is None:
                self.distribution.entry_points = {}
            console_scripts = self.distribution.entry_points.setdefault('console_scripts', [])
            console_scripts.extend(results.console_scripts)
        except:
            # something apparently consumes tracebacks (not exception messages)
            # for OSError at least.  let's avoid that silliness.
            traceback.print_exc()
            raise


@attr.s(frozen=True)
class Results:
    console_scripts = attr.ib()


def checkpoint(name):
    print('    ----<==== {} ====>----'.format(name))


def build(package_path: pathlib.Path):
    applications = [
        Application(name=name, path=qt5_applications._application_path(name))
        for name in qt5_applications._application_names()
    ]

    checkpoint('Write Entry Points')
    entry_points_py = package_path.joinpath('entrypoints.py')

    console_scripts = write_entry_points(
        entry_points_py=entry_points_py,
        applications=applications,
    )

    checkpoint('Return Results')
    return Results(console_scripts=console_scripts)


def create_script_function_name(path: pathlib.Path):
    return path.stem.replace('-', '_')


@attr.s
class Application:
    name = attr.ib()
    path = attr.ib()


def write_entry_points(
        entry_points_py: pathlib.Path,
        applications: typing.List[Application],
) -> typing.List[str]:
    with entry_points_py.open('a', encoding='utf-8', newline='\n') as f:
        f.write(textwrap.dedent('''\
        
            # ----  start of generated wrapper entry points
        
        '''))

        console_scripts = []

        for application in sorted(applications, key=lambda a: a.name):
            function_name = create_script_function_name(application.path)
            script_name = application.path.stem
            stem = application.path.stem

            partial_def = (
                '{function_name}'
                ' = functools.partial(run, application_name={application!r})\n'
            )
            partial_def_formatted = partial_def.format(
                function_name=function_name,
                application=stem,
            )
            f.write(partial_def_formatted)

            console_scripts.append(
                'qt5{application} = qt5_tools.entrypoints:{function_name}'.format(
                    function_name=function_name,
                    application=script_name,
                )
            )

        f.write(textwrap.dedent('''\

            # ----  end of generated wrapper entry points

        '''))

    return console_scripts
