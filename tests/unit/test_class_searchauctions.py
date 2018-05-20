import codecs
import os
from collections import namedtuple
from datetime import date
from unittest import mock

import requests

from comprasnet import SearchAuctions


def test_class_attributes_and_properties():
    search_auctions = SearchAuctions(date.today())
    assert search_auctions.day == date.today()
    assert search_auctions.total_results == 0
    assert search_auctions.current_page == 1
    assert search_auctions.SEARCH_URL == \
           "http://comprasnet.gov.br/ConsultaLicitacoes/ConsLicitacao_Relacao.asp"
    assert search_auctions.OFFSET == 10

    assert search_auctions.total_pages == 0
    assert search_auctions.is_done is True

    search_auctions.total_results = 27
    assert search_auctions.total_pages == 3
    assert search_auctions.is_done is False
    search_auctions.current_page = 4
    assert search_auctions.is_done is True


def test_method_get_search_params():
    search_auctions = SearchAuctions()
    assert list(search_auctions.get_search_params().keys()) == [
        'numprp', 'dt_publ_ini', 'dt_publ_fim', 'chkModalidade', 'chk_concor', 'chk_pregao',
        'chk_rdc', 'optTpPesqMat', 'optTpPesqServ', 'chkTodos', 'chk_concorTodos',
        'chk_pregaoTodos', 'txtlstUf', 'txtlstMunicipio', 'txtlstUasg', 'txtlstGrpMaterial',
        'txtlstClasMaterial', 'txtlstMaterial', 'txtlstGrpServico', 'txtlstServico', 'txtObjeto',
        'numpag'
    ]


@mock.patch('comprasnet.requests.get')
def test_method_get_search_metadata(get):
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            '../assets/result_page_sample.html')
    with codecs.open(filename, 'r', 'iso-8859-1') as handle:
        page_result_content = handle.read()

    MockResponse = namedtuple('Response', 'status_code, text')
    MockResponse.status_code = requests.codes.ok
    MockResponse.text = page_result_content
    get.return_value = MockResponse

    search_auctions = SearchAuctions()
    search_auctions.get_search_metadata()
    assert search_auctions.total_results == 183
    assert search_auctions.total_pages == 19
    assert get.called_with(search_auctions.SEARCH_URL, search_auctions.get_search_params())


def test_method_get_search_page_data():
    assert False


def test_method_scrap_search_page():
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            '../assets/result_page_sample.html')
    with codecs.open(filename, 'r', 'iso-8859-1') as handle:
        page_result_content = handle.read()

    search_auctions = SearchAuctions(day=date(day=11, month=5, year=2018))
    results = search_auctions.scrap_search_page(page_result_content)
    
    output = [{'abertura-da-proposta': date(2018, 5, 14),
                'abertura-da-proposta-str': '14/05/2018',
                'cabecalho': ['MINISTÉRIO DA DEFESA',
                                'Comando do Exército',
                                'Comando Militar do Sul',
                                '1º Batalhão Ferroviário'],
                'cidade': 'Lages',
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
                'telefone': '(49) 32519515',
                'uf': 'SC'},
                {'abertura-da-proposta': date(2018, 5, 14),
                'abertura-da-proposta-str': '14/05/2018',
                'cabecalho': ['MINISTÉRIO DA DEFESA',
                                'Comando do Exército',
                                'Comando Militar do Sul',
                                '5ª Região Militar',
                                '15ªBrigada de Infantaria Mecanizada',
                                '26ºGrupo de Artilharia de Campanha'],
                'cidade': 'Guarapuava',
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
                'telefone': '(42) 31419115',
                'uf': 'PR'},
                {'abertura-da-proposta': date(2018, 5, 14),
                'abertura-da-proposta-str': '14/05/2018',
                'cabecalho': ['MINISTÉRIO DA DEFESA',
                                'Comando do Exército',
                                'Comando Militar do Nordeste',
                                '7ª Região Militar/7ª Divisão de Exército',
                                '10ªBrigada de Infantaria Motorizada',
                                '72ºBatalhão de Infantaria Motorizado'],
                'cidade': 'Petrolina',
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
                'telefone': '',
                'uf': 'PE'},
                {'abertura-da-proposta': date(2018, 5, 14),
                'abertura-da-proposta-str': '14/05/2018',
                'cabecalho': ['MINISTÉRIO DA DEFESA',
                                'Comando do Exército',
                                'Comando Militar do Sul',
                                '6ªDivisão de Exército',
                                '8ªBrigada de Infantaria Motorizada',
                                '9ºBatalhão de Infantaria Motorizado'],
                'cidade': 'Pelotas',
                'codigo-da-uasg': '160379',
                'edital-a-partir-de': date(2018, 5, 2),
                'edital-a-partir-de-str': '02/05/2018',
                'endereco': ' Av Duque de Caxias, 344 - Bairro Fragata - Fragata - Pelotas '
                            '(RS)',
                'entrega-da-proposta': date(2018, 5, 2),
                'entrega-da-proposta-str': '02/05/2018',
                'fax': '(53)',
                'objeto': 'Pregão Eletrônico -  Serviço Comum de Engenharia - Adequação da '
                            'Rede Elétrica do 9º Batalhão de Infantaria Motorizado (9º BIMtz).',
                'pregao-eletronico': '22018',
                'telefone': '(53) 33034044',
                'uf': 'RS'},
                {'abertura-da-proposta': date(2018, 5, 15),
                'abertura-da-proposta-str': '15/05/2018',
                'cabecalho': ['Agência de Modernização da Gestão de Processos'],
                'cidade': 'Maceió',
                'codigo-da-uasg': '925998',
                'edital-a-partir-de': date(2018, 5, 2),
                'edital-a-partir-de-str': '02/05/2018',
                'endereco': ' Rua Manoel Nobre, No 281, Farol -  - Maceió (AL)',
                'entrega-da-proposta': date(2018, 5, 2),
                'entrega-da-proposta-str': '02/05/2018',
                'fax': '',
                'objeto': 'Pregão Eletrônico -  Aquisição de Materiais Elétricos.  ATENÇÃO: '
                            'Srs. Licitantes, ao cadastrar a proposta no sistema ComprasNet, '
                            'considerar somente a descrição dos itens contidos no Termo de '
                            'Referência do Edital, sob pena de desclassificação.',
                'pregao-eletronico': '112982017',
                'telefone': '',
                'uf': 'AL'},
                {'abertura-da-proposta': date(2018, 5, 17),
                'abertura-da-proposta-str': '17/05/2018',
                'cabecalho': ['Agência de Modernização da Gestão de Processos'],
                'cidade': 'Maceió',
                'codigo-da-uasg': '925998',
                'edital-a-partir-de': date(2018, 5, 2),
                'edital-a-partir-de-str': '02/05/2018',
                'endereco': ' Rua Manoel Nobre, No 281, Farol -  - Maceió (AL)',
                'entrega-da-proposta': date(2018, 5, 2),
                'entrega-da-proposta-str': '02/05/2018',
                'fax': '(82)',
                'objeto': 'Pregão Eletrônico -  A presente licitação objetiva o registro de '
                            'preços para a AQUISIÇÃO DE MEDICAMENTOS (ANTI-INFLAMATÓRIOS E '
                            'ANALGÉSICOS)   PLS Nº 028/2018',
                'pregao-eletronico': '102792018',
                'telefone': '(82) 33153092',
                'uf': 'AL'},
                {'abertura-da-proposta': date(2018, 5, 17),
                'abertura-da-proposta-str': '17/05/2018',
                'cabecalho': ['Agência de Modernização da Gestão de Processos'],
                'cidade': 'Maceió',
                'codigo-da-uasg': '925998',
                'edital-a-partir-de': date(2018, 5, 2),
                'edital-a-partir-de-str': '02/05/2018',
                'endereco': ' Rua Manoel Nobre, No 281, Farol -  - Maceió (AL)',
                'entrega-da-proposta': date(2018, 5, 2),
                'entrega-da-proposta-str': '02/05/2018',
                'fax': '(82)',
                'objeto': 'Pregão Eletrônico -  A presente licitação tem por objeto a '
                            'AQUISIÇÃO DE GÊNEROS ALIMENTÍCIOS  (MOLHOS E CONDIMENTOS)   PLS '
                            'Nº 054/2017',
                'pregao-eletronico': '102772018',
                'telefone': '(82) 99181712',
                'uf': 'AL'},
                {'abertura-da-proposta': date(2018, 5, 16),
                'abertura-da-proposta-str': '16/05/2018',
                'cabecalho': ['Agência de Modernização da Gestão de Processos'],
                'cidade': 'Maceió',
                'codigo-da-uasg': '925998',
                'edital-a-partir-de': date(2018, 5, 2),
                'edital-a-partir-de-str': '02/05/2018',
                'endereco': ' Rua Manoel Nobre, No 281, Farol -  - Maceió (AL)',
                'entrega-da-proposta': date(2018, 5, 2),
                'entrega-da-proposta-str': '02/05/2018',
                'fax': '',
                'objeto': 'Pregão Eletrônico -  A presente licitação objetiva o registro de '
                            'preços para a AQUISIÇÃO DE EMBALAGEM DE ALUMÍNIO - PLS N¨ '
                            '026-2016 EXCLUSIVO',
                'pregao-eletronico': '102752018',
                'telefone': '',
                'uf': 'AL'},
                {'abertura-da-proposta': date(2018, 5, 15),
                'abertura-da-proposta-str': '15/05/2018',
                'cabecalho': ['Agência de Modernização da Gestão de Processos'],
                'cidade': 'Maceió',
                'codigo-da-uasg': '925998',
                'edital-a-partir-de': date(2018, 5, 2),
                'edital-a-partir-de-str': '02/05/2018',
                'endereco': ' Rua Manoel Nobre, No 281, Farol -  - Maceió (AL)',
                'entrega-da-proposta': date(2018, 5, 2),
                'entrega-da-proposta-str': '02/05/2018',
                'fax': '',
                'objeto': 'Pregão Eletrônico -  Aquisição de materiais de consumo para '
                            'utilização no Laboratório de Microbiologia e Tuberculose.',
                'pregao-eletronico': '102692018',
                'telefone': '',
                'uf': 'AL'},
                {'abertura-da-proposta': date(2018, 5, 15),
                'abertura-da-proposta-str': '15/05/2018',
                'cabecalho': ['Agência de Modernização da Gestão de Processos'],
                'cidade': 'Maceió',
                'codigo-da-uasg': '925998',
                'edital-a-partir-de': date(2018, 5, 2),
                'edital-a-partir-de-str': '02/05/2018',
                'endereco': ' Rua Manoel Nobre, No 281, Farol -  - Maceió (AL)',
                'entrega-da-proposta': date(2018, 5, 2),
                'entrega-da-proposta-str': '02/05/2018',
                'fax': '',
                'objeto': 'Pregão Eletrônico -  Aquisição de equipamento médico hospitalares',
                'pregao-eletronico': '102662018',
                'telefone': '',
                'uf': 'AL'}]
    assert output == results
