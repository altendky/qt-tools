import functools
import os
import subprocess
import sys

import click
import qt5_applications

import qt5_tools


fspath = getattr(os, 'fspath', str)


@click.group()
def main():
    pass


def run(
        application_name,
        args=(),
        environment=os.environ,
        sys_platform=sys.platform,
):
    modified_environment = qt5_tools.create_environment(
        reference=environment,
    )

    command_elements = qt5_tools.create_command_elements(
        name=application_name,
        sys_platform=sys_platform,
    )

    completed_process = subprocess.run(
        [*command_elements, *args],
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
