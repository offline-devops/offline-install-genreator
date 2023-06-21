from sqlalchemy.orm import Session
import pathlib
from . import models, schemas


def get_or_create(session: Session, model: models.Base, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).one_or_none()
    if instance:
        return instance, False
    else:
        kwargs |= defaults or {}
        instance = model(**kwargs)
        try:
            session.add(instance)
            session.commit()
        except Exception:  # The actual exception depends on the specific database so we catch all exceptions. This is similar to the official documentation: https://docs.sqlalchemy.org/en/latest/orm/session_transaction.html
            session.rollback()
            instance = session.query(model).filter_by(**kwargs).one()
            return instance, False
        else:
            return instance, True


def create_scan_folder(db: Session, path: str):
    return get_or_create(db, models.ScanFolder, defaults=None, path=path)[0]


def get_install_file(db: Session):
    return db.query(models.InstallFile).all()


def get_scan_folder(db: Session):
    return db.query(models.ScanFolder).all()


def check_file(db: Session, path: pathlib.Path):
    obj, is_create = get_or_create(db, models.InstallFilePath, path=str(path))
    if is_create:
        return obj
    get_or_create(db, models.InstallFile, name=path.name)
    return obj


