import os
import hashlib
import importlib
import pkgutil

def walk_dir(path):
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            files.append(os.path.join(r, file))
    return files


def compute_md5(file, blocksize=2**16):
    hasher = hashlib.md5()
    with open(file, 'rb') as f:
        buf = f.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(blocksize)

    return hasher.hexdigest()


def iter_namespace(ns_pkg):
    # Specifying the second argument (prefix) to iter_modules makes the
    # returned name an absolute name instead of a relative one. This allows
    # import_module to work without having to do additional modification to
    # the name.
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")


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