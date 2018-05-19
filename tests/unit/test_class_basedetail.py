from comprasnet import BaseDetail
import pytest

def test_class():
    obj = BaseDetail(uasg_code=160478, auction_code=32018)

    assert hasattr(BaseDetail, 'DETAIL_URL')
    for attr in ('get_params', 'get_data', 'scrap_data', 'data', 'url'):
        assert hasattr(BaseDetail, attr)
        with pytest.raises(NotImplementedError):
            method = getattr(obj, attr)
            method()

    assert str(obj) == '160478/32018'


