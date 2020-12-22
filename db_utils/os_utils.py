import os
import db_utils


def get_project_dir():
    """Return path to the project root."""
    return os.path.dirname(os.path.abspath(db_utils.__file__))

