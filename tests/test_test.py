# Dummy test file to validate CI/CD with Github action

import pytest

def f():
    raise ExceptionGroup(
        "Group message",
        [
            RuntimeError()
        ],
    )


def test_exception_in_group():
    with pytest.raises(ExceptionGroup) as excinfo:
        f()
    assert excinfo.group_contains(RuntimeError)
    assert not excinfo.group_contains(TypeError)
