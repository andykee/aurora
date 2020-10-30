import importlib
import pkgutil

import aurora.drivers



def iter_namespace(ns_pkg):
    # Specifying the second argument (prefix) to iter_modules makes the
    # returned name an absolute name instead of a relative one. This allows
    # import_module to work without having to do additional modification to
    # the name.
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")


def import_namespace_plugins():
    # NOTE: driver class MUST be importable at the top level (i.e. imported in the driver __init__.py file)
    for finder, name, ispkg in iter_namespace(aurora.drivers):
        if ispkg:
            importlib.import_module(name)


def get_namespace_plugins(ns_pkg=None):
    if ns_pkg is None:
        import aurora.drivers as ns_pkg

    return {
        name: importlib.import_module(name)
        for finder, name, ispkg
        in iter_namespace(ns_pkg)
        if ispkg
    }



def list_drivers(ns_pkg=None):
    ns_plugins = get_namespace_plugins(ns_pkg)
    if ns_plugins:
        print('Drivers found:\n' + '\n'.join(ns_plugins))
    else:
        print('No drivers are installed')