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
    assert page_results[:3] == [{
                                    'cabecalho': [
                                            'MINISTÉRIO DA DEFESA',
                                            'Comando do Exército',
                                            'Comando Militar do Sul',
                                            '1º Batalhão Ferroviário',
                                    ],
                                    'cidade': 'Lages',
                                    'uf': 'SC',
                                    'abertura-da-proposta': date(2018, 5, 14),
                                    'abertura-da-proposta-str': '14/05/2018',
                                    'codigo-da-uasg': '160447',
                                    'edital-a-partir-de': date(2018, 5, 2),
                                    'edital-a-partir-de-str': '02/05/2018',
                                    'endereco': ' Rua 2.batalhao Rodoviario,sn * - Conta Dinheiro - Lages (SC)',
                                    'entrega-da-proposta': date(2018, 5, 2),
                                    'entrega-da-proposta-str': '02/05/2018',
                                    'fax': '(49)',
                                    'objeto': 'Pregão Eletrônico -  Eventual aquisição de  materiais de '
                                                'construção, para utilização na Obra da Construção da Ferrovia das '
                                                'Bromélias, Revitalização da Estrada de Acesso ao Destacamento de '
                                                'Controle de Espaço Aéreo do Morro da Igreja,  Obra da SC 114 '
                                                '(antiga SC-430), e Sede da OM - manutenção de PNRs e Instalações '
                                                'internas do Batalhão.',
                                    'pregao-eletronico': '122018',
                                    'telefone': '(49) 32519515'},
                                {
                                    'cabecalho': [
                                            'MINISTÉRIO DA DEFESA',
                                            'Comando do Exército',
                                            'Comando Militar do Sul',
                                            '5ª Região Militar',
                                            '15ª Brigada de Infantaria Mecanizada',
                                            '26º Grupo de Artilharia de Campanha'],
                                    'cidade': 'Guarapuava',
                                    'uf': 'PR',
                                    'abertura-da-proposta': date(2018, 5, 14),
                                    'abertura-da-proposta-str': '14/05/2018',
                                    'codigo-da-uasg': '160228',
                                    'edital-a-partir-de': date(2018, 5, 2),
                                    'edital-a-partir-de-str': '02/05/2018',
                                    'endereco': ' Av Manoel Ribas, 2286 - Centro - Centro - Guarapuava (PR)',
                                    'entrega-da-proposta': date(2018, 5, 2),
                                    'entrega-da-proposta-str': '02/05/2018',
                                    'fax': '(42)',
                                    'objeto': 'Pregão Eletrônico -  Aquisição de Material de Acondicionamento e '
                                                'Embalagens',
                                    'pregao-eletronico': '112018',
                                    'telefone': '(42) 31419115'
                                },
                                {
                                'cabecalho': [
                                            'MINISTÉRIO DA DEFESA',
                                            'Comando do Exército',
                                            'Comando Militar do Nordeste',
                                            '7ª Região Militar/7º Divisão de Exército',
                                            '10ª Brigada de Infantaria Motorizada',
                                            '72º Batalhão de Infantaria Motorizado'],
                                'cidade': 'Petrolina',
                                'uf': 'PE',
                                'abertura-da-proposta': date(2018, 5, 14),
                                'abertura-da-proposta-str': '14/05/2018',
                                'codigo-da-uasg': '160183',
                                'edital-a-partir-de': date(2018, 5, 2),
                                'edital-a-partir-de-str': '02/05/2018',
                                'endereco': ' Av. Cardoso de Sa, S/n - Vila Eduardo - Vila Eduardo - '
                                            'Petrolina (PE)',
                                'entrega-da-proposta': date(2018, 5, 2),
                                'entrega-da-proposta-str': '02/05/2018',
                                'fax': '',
                                'objeto': 'Pregão Eletrônico -  Registro de preços para eventual contratação '
                                            'de serviços de gerenciamento, controle e fornecimento de '
                                            'combustível por meio de sistema informatizado e utilização de '
                                            'cartão eletrônico ou magnético.',
                                'pregao-eletronico': '22018',
                                'telefone': ''
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
