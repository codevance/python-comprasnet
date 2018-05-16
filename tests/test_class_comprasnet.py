import codecs
import os
from collections import namedtuple
from datetime import datetime, date
from unittest import mock

import requests

from comprasnet import ComprasNet


def test_should_return_attributes():
    comprasnet = ComprasNet()
    assert hasattr(comprasnet, 'TMP_DIR')
    assert hasattr(comprasnet, 'SEARCH_BIDS_URL')


def test_should_return_correct_dict_structure():
    comprasnet = ComprasNet()
    assert list(comprasnet.get_data_dict_to_search_auctions().keys()) == [
        'numprp', 'dt_publ_ini', 'dt_publ_fim', 'chkModalidade', 'chk_concor', 'chk_pregao',
        'chk_rdc', 'optTpPesqMat', 'optTpPesqServ', 'chkTodos', 'chk_concorTodos',
        'chk_pregaoTodos', 'txtlstUf', 'txtlstMunicipio', 'txtlstUasg', 'txtlstGrpMaterial',
        'txtlstClasMaterial', 'txtlstMaterial', 'txtlstGrpServico', 'txtlstServico', 'txtObjeto',
        'numpag'
    ]


@mock.patch('comprasnet.ComprasNet.get_search_result_page')
def test_should_search_auctions_by_date(get_search_result_page):
    get_search_result_page.return_value = ([{'codigo_da_uasg': '160053', 'pregao_eletronico':
        '22018'}, {'codigo_da_uasg': '160232', 'pregao_eletronico': '32018'}], True)
    comprasnet = ComprasNet()

    results = comprasnet.search_auctions_by_date(datetime.now())
    assert results == [{'codigo_da_uasg': '160053', 'pregao_eletronico':
        '22018'}, {'codigo_da_uasg': '160232', 'pregao_eletronico': '32018'}]
    assert get_search_result_page.called_with(comprasnet.SEARCH_BIDS_URL,
                                              comprasnet.get_data_dict_to_search_auctions())

@mock.patch('comprasnet.requests.get')
def test_get_data_auctions_pages(get):
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'assets/result_page_sample.html')
    with codecs.open(filename, 'r', 'iso-8859-1') as handle:
        page_result_content = handle.read()

    MockResponse = namedtuple('Response', 'status_code, text')
    MockResponse.status_code = requests.codes.ok
    MockResponse.text = page_result_content
    get.return_value = MockResponse

    comprasnet = ComprasNet()
    page_results, is_last = comprasnet.get_data_auctions_pages({
        'dt_publ_ini': 'foo',
        'numpag': 'foo',
    })

    assert is_last is False
    assert page_results[1:3] == [{
                                'codigo-da-uasg': '160228',
                                'pregao-eletronico': '112018',
                                'objeto': 'Pregão Eletrônico -  Aquisição de '
                                'Material de Acondicionamento e Embalagens',
                                'edital-a-partir-de-str': '02/05/2018',
                                'edital-a-partir-de': date(2018, 5, 2)
                            }, {
                                'codigo-da-uasg': '160183',
                                'pregao-eletronico': '22018',
                                'objeto': 'Pregão Eletrônico -  Registro de '
                                'preços para eventual contratação de serviços'
                                ' de gerenciamento, controle e fornecimento'
                                ' de combustível por meio de sistema '
                                'informatizado e utilização de cartão '
                                'eletrônico ou magnético.',
                                'edital-a-partir-de-str': '02/05/2018',
                                'edital-a-partir-de': date(2018, 5, 2)
                            }]
@mock.patch('comprasnet.requests.get')
def test_should_search_auctions_by_date(get):
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'assets/result_page_sample.html')
    with codecs.open(filename, 'r', 'iso-8859-1') as handle:
        page_result_content = handle.read()

    MockResponse = namedtuple('Response', 'status_code, text')
    MockResponse.status_code = requests.codes.ok
    MockResponse.text = page_result_content
    get.return_value = MockResponse

    comprasnet = ComprasNet()
    page_results, is_last = comprasnet.get_search_result_page({
        'dt_publ_ini': 'foo',
        'numpag': 'foo',
    })
    assert is_last is False
    assert page_results == [{'codigo_da_uasg': '160447', 'pregao_eletronico': '122018'},
                            {'codigo_da_uasg': '160228', 'pregao_eletronico': '112018'},
                            {'codigo_da_uasg': '160183', 'pregao_eletronico': '22018'},
                            {'codigo_da_uasg': '160379', 'pregao_eletronico': '22018'},
                            {'codigo_da_uasg': '925998', 'pregao_eletronico': '112982017'},
                            {'codigo_da_uasg': '925998', 'pregao_eletronico': '102792018'},
                            {'codigo_da_uasg': '925998', 'pregao_eletronico': '102772018'},
                            {'codigo_da_uasg': '925998', 'pregao_eletronico': '102752018'},
                            {'codigo_da_uasg': '925998', 'pregao_eletronico': '102692018'},
                            {'codigo_da_uasg': '925998', 'pregao_eletronico': '102662018'}]

    assert get.called_with((comprasnet.SEARCH_BIDS_URL, {'foo': 'bar'}))
