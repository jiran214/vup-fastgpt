import json
import config
from contextlib import contextmanager, redirect_stdout
from io import StringIO


def write_json(filename, data):
    filename = str(config.config_path / filename)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
