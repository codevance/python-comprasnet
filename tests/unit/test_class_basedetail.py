from comprasnet import BaseDetail
import pytest

def test_class():
    assert hasattr(BaseDetail, 'DETAIL_URL')
    for attr in ('get_params', 'get_data', 'scrap_data', 'data'):
        assert hasattr(BaseDetail, attr)
        with pytest.raises(NotImplementedError):
            obj = BaseDetail()
            method = getattr(obj, attr)
            method()


