import os
import copy
import inspect
import importlib.util


DEFAULT_CONFIG = {
    'PATH': os.curdir,
    'HOST': 'localhost',
    'PORT': 8000,
    'DATABASE_URI': 'sqlite://aurora.db',
    'TIMEZONE': 'UTC'
}


def load_source(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def get_config_from_file(path):
    """Loads settings from a file path, returning a dict."""

    name, ext = os.path.splitext(os.path.basename(path))
    module = load_source(name, path)
    return get_config_from_module(module)


def get_config_from_module(module=None):
    """Loads settings from a module, returns a dictionary."""

    context = {}
    if module is not None:
        context.update(
            (k, v) for k, v in inspect.getmembers(module) if k.isupper())
    return context


def get_config(path=None, override=None):
    config = override or {}
    
    if path:
        config = dict(get_config_from_file(path))
    
    config = dict(copy.deepcopy(DEFAULT_CONFIG), **config)
    
    return config