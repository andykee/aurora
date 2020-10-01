

# This module contains functions for working with the catalog file
# 
# Things like adding data, determining whether data is missing from a catalog,
# updating data when a file is moved, etc.
#
# Checking for duplicate entry based on hash
#
# migrate helpers.py here
import re

from sqlalchemy.exc import IntegrityError

from aurora.models import File, Data, Tag, Category
from aurora.util import import_namespace_plugins


import_namespace_plugins()

DRIVER_MAPPING = {
    driver.__pattern__: driver
    for driver in Data.__subclasses__()
}

def safe_insert(session, instance):
    try:
        session.add(instance)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        raise e


def safe_insert_all(session, instances):
    try:
        session.add_all(instances)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        raise e


def insert_data(session, file, driver=Data, ignore_duplicates=True):
    f = File(file=file, compute_hash=ignore_duplicates)
    d = driver(file=f)

    if ignore_duplicates:
        if session.query(File).filter(File.hash == f.hash).count() > 0:
            raise ValueError('DUPE!')

    safe_insert_all(session, [f,d])


def get_driver(file):
    for pattern in DRIVER_MAPPING.keys():
        if re.fullmatch(pattern, file):
            return DRIVER_MAPPING[pattern]
    return Data


def insert_tag(session, name):
    safe_insert(session, Tag(name=name))


def add_from_path(session, path, driver=None, ignore_duplicates=True):
    pass

