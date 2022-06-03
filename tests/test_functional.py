import functools
import os

import pytest
import utils.RunUtils


def capture_main(args=[], timeout=None):
    return utils.RunUtils.capture(args=['main.py', *args], timeout=timeout)


def test_main_no_params():
    out, err, exitcode = capture_main()

    assert exitcode == 0
    assert len(out) == 0
    assert len(err) == 0


def test_main_invalid_param():
    out, err, exitcode = capture_main('-x')

    assert exitcode == 1
    assert len(out) == 0
    assert b'error: unrecognized arguments' in err


def test_main_help_param():
    out, err, exitcode = capture_main('-h')

    assert exitcode == 1
    assert len(out) == 0
    assert b"usage:" in err


@pytest.mark.parametrize('param', ['-d', '--dir'])
def test_main_data_dir_param(param, tmp_path):
    adir = str(tmp_path / 'non_existing_dir')
    assert not os.path.exists(adir)

    _, _, exitcode = capture_main([param, adir])

    assert exitcode == 0
    assert os.path.exists(adir)
