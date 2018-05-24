from comprasnet.pages import BaseDetail
import pytest


@pytest.fixture
def base_detail():
    return BaseDetail(uasg_code=160478, auction_code=32018)


def test_class(base_detail):
    assert hasattr(BaseDetail, 'DETAIL_URL')
    for attr in ('get_params', 'get_data', 'scrap_data', 'data', 'url'):
        assert hasattr(BaseDetail, attr)
        with pytest.raises(NotImplementedError):
            method = getattr(base_detail, attr)
            method()

    assert str(base_detail) == '160478/32018'


def test__order_dict(base_detail):
    params = {"x": None, "z": None, "a": None}
    expected = {"a": None, "x": None, "z": None}
    assert base_detail._order_dict(params) == expected
