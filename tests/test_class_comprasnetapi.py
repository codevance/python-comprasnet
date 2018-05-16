from comprasnet.api import ComprasNetApi
from unittest import mock
from collections import namedtuple

MockResponse = namedtuple('Response', ['status_code', 'json', 'text'])


def test_class():
    comprasnet_api = ComprasNetApi()
    assert hasattr(comprasnet_api, 'last_response')
    assert comprasnet_api.BASE_SEARCH_URL == "http://compras.dados.gov.br/{modulo}/{version}/{" \
                                             "metodo}.{formato}"
    assert comprasnet_api.BASE_DETAIL_URL == "http://compras.dados.gov.br/{modulo}/{version}/{" \
                                             "metodo}/{item}.{" \
                                             "formato}"


@mock.patch('comprasnet.api.requests.get')
def test_method_raw_request(get):
    fake_response = MockResponse(status_code=200, json={}, text='')
    get.return_value = fake_response

    comprasnet_api = ComprasNetApi()
    response = comprasnet_api._raw_request('https://google.com.br', foo=1, bar=2)
    assert get.called_with('https://google.com.br', foo=1, bar=2)
    assert response is fake_response
    assert comprasnet_api.last_response is fake_response


@mock.patch('comprasnet.api.ComprasNetApi._raw_request')
def test_method_request_search(_raw_request):
    comprasnet_api = ComprasNetApi()
    comprasnet_api._request_search('modulo', 'metodo', foo=1, bar=2)

    url = comprasnet_api.BASE_SEARCH_URL.format(
        modulo='modulo', metodo='metodo', version='v1', formato='json')
    assert _raw_request.called_with(url, foo=1, bar=2)


@mock.patch('comprasnet.api.ComprasNetApi._raw_request')
def test_method__request_detail(_raw_request):
    comprasnet_api = ComprasNetApi()
    comprasnet_api._request_detail('modulo', 'metodo', 'item', foo=1, bar=2)

    url = comprasnet_api.BASE_DETAIL_URL.format(
        modulo='modulo', metodo='metodo', item='item', version='v1', formato='json')
    assert _raw_request.called_with(url, foo=1, bar=2)


@mock.patch('comprasnet.api.ComprasNetApi._request_detail')
def test_method_get_licitacoes_uasg(_request_detail):
    comprasnet_api = ComprasNetApi()
    comprasnet_api.get_licitacoes_uasg('123456', foo=1)

    assert _request_detail.called_with('licitacoes', 'uasg', '123456', foo=1)
