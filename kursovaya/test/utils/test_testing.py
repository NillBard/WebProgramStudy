import pytest

from analyzer.utils.testing import generate_citizens


def test_generate_citizens():
    generate_citizens(citizens_num=2, relations_num=1)

    with pytest.raises(ValueError):
        generate_citizens(citizens_num=2, relations_num=2)
