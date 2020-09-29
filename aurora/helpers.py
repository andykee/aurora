from sqlalchemy.exc import IntegrityError

from aurora.models import File, Data, Tag, Category


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
    safe_insert_all(session, [f,d])


def insert_tag(session, name):
    safe_insert(session, Tag(name=name))


def infer_driver_from_ext(file_extension):
    return Data