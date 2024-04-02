import pytest
import sys
import os
import azentengine

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from conftest import skip_openai  # noqa: E402


@pytest.mark.skipif(skip_openai, reason="requested to skip openai tests")
def test_nested():
    pass

if __name__ == "__main__":
    test_nested()