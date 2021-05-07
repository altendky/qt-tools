import functools
import os
import subprocess
import sys

import click


# TODO: CAMPid 0970432108721340872130742130870874321
def import_it(*segments):
    import importlib
    import pkg_resources

    major = int(pkg_resources.get_distribution(__name__).version.partition(".")[0])

    m = {
        "pyqt_tools": "pyqt{major}_tools".format(major=major),
        "pyqt_plugins": "pyqt{major}_plugins".format(major=major),
        "qt_tools": "qt{major}_tools".format(major=major),
        "qt_applications": "qt{major}_applications".format(major=major),
    }

    majored = [m[segments[0]], *segments[1:]]
    return importlib.import_module(".".join(majored))

qt_applications = import_it("qt_applications")
qt_tools = import_it("qt_tools")


fspath = getattr(os, 'fspath', str)


@click.group()
def main():
    pass


def run(application_name, args=(), environment=os.environ):
    modified_environment = qt_tools.create_environment(
        reference=environment,
    )
    application_path = qt_applications._application_path(application_name)

    completed_process = subprocess.run(
        [
            fspath(application_path),
            *args,
        ],
        env=modified_environment,
    )

    return completed_process.returncode


# written by build.py

# @main.command(
#     add_help_option=False,
#     context_settings={
#         'ignore_unknown_options': True,
#         'allow_extra_args': True,
#     },
# )
# @click.pass_context
# def designer(ctx):
#     return run('designer', args=ctx.args)
