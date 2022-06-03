import os
import subprocess
import sys

import pytest


def capture(args=[], timeout=None):
    proc = subprocess.Popen(
        [sys.executable, *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={**os.environ, 'PYTHONIOENCODING': 'utf-8'},
    )
    out, err = proc.communicate(timeout=timeout)
    return out, err, proc.returncode
