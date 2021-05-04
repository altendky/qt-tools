import os


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


from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


def bin_path():
    return qt_applications._bin


def application_names():
    return qt_applications._application_names()


def application_path(name):
    return qt_applications._application_path(name)


def create_environment(reference=None):
    # noop for now, but just in case something needs added
    if reference is None:
        reference = os.environ

    return dict(reference)