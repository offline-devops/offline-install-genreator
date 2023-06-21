import pathlib
from . import curd
import time
from loguru import logger


def iter_scanned_file(db):
    for folder in curd.get_scan_folder(db):
        time.sleep(1)
        p = pathlib.Path(folder.path)
        if p.exists() and p.is_dir():
            for file in p.rglob("*"):
                if file.suffix in ['.msi', '.exe']:
                    yield file
        else:
            logger.error(f"is not available path: {p}")


