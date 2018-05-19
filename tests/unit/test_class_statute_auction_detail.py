import codecs
import os
from collections import namedtuple
from datetime import date
from unittest import mock

import requests

from comprasnet import StatuseAuctionDetail

statuse_detail = StatuseAuctionDetail(uasg_code=160478, auction_code=32018)


def test_class_attributes_and_properties():
    assert statuse_detail.auction_code == 32018
    assert statuse_detail.uasg_code == 160478
    assert statuse_detail.url == "http://comprasnet.gov.br/ConsultaLicitacoes/download" \
                                 "/download_editais_detalhe.asp?coduasg=160478&numprp=32018" \
                                 "&modprp=5"


def test_method_get_params():
    assert statuse_detail.get_params() == {'coduasg': 160478, 'modprp': 5, 'numprp': 32018}


@mock.patch('comprasnet.requests.get')
def test_method_get_data(get):
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            '../assets/statusedetail_page_example.html')
    with codecs.open(filename, 'r', 'iso-8859-1') as handle:
        page_content = handle.read()

    MockResponse = namedtuple('Response', 'status_code, text')
    MockResponse.status_code = requests.codes.ok
    MockResponse.text = page_content
    get.return_value = MockResponse

    assert statuse_detail.get_data() == page_content


@mock.patch('comprasnet.StatuseAuctionDetail.get_data')
def test_method_scrap_data(get_data):
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            '../assets/statusedetail_page_example.html')
    with codecs.open(filename, 'r', 'iso-8859-1') as handle:
        page_content = handle.read()

    get_data.return_value = page_content

    output = {'codigo-da-uasg': 160478,
              'itens': [{'aplicabilidade-decreto': 'Não',
                'aplicabilidade-margem-de-preferencia': 'Não',
                'numero': 1,
                'quantidade': 60,
                'titulo': 'Pacote de Serviços SMP (Voz, Dados, SMS, Etc)',
                'tratamento-diferenciado': '-',
                'unidade-de-fornecimento': 'Assinatura'},
            {'aplicabilidade-decreto': 'Não',
                'aplicabilidade-margem-de-preferencia': 'Não',
                'numero': 2,
                'quantidade': 60,
                'titulo': 'Pacote de Serviços SMP (Voz, Dados, SMS, Etc)',
                'tratamento-diferenciado': '-',
                'unidade-de-fornecimento': 'Assinatura'},
            {'aplicabilidade-decreto': 'Não',
                'aplicabilidade-margem-de-preferencia': 'Não',
                'numero': 3,
                'quantidade': 60,
                'titulo': 'Pacote de Serviços SMP (Voz, Dados, SMS, Etc)',
                'tratamento-diferenciado': '-',
                'unidade-de-fornecimento': 'Assinatura'},
            {'aplicabilidade-decreto': 'Não',
                'aplicabilidade-margem-de-preferencia': 'Não',
                'numero': 4,
                'quantidade': 60,
                'titulo': 'Pacote de Serviços SMP (Voz, Dados, SMS, Etc)',
                'tratamento-diferenciado': '-',
                'unidade-de-fornecimento': 'Assinatura'},
            {'aplicabilidade-decreto': 'Não',
                'aplicabilidade-margem-de-preferencia': 'Não',
                'numero': 5,
                'quantidade': 6000,
                'titulo': 'Chamadas  Locais Móvel-Móvel  Intraoperadora '
                        'SMP-Local-MM-IO(VC1)',
                'tratamento-diferenciado': '-',
                'unidade-de-fornecimento': 'Minutos'},
            {'aplicabilidade-decreto': 'Não',
                'aplicabilidade-margem-de-preferencia': 'Não',
                'numero': 6,
                'quantidade': 6000,
                'titulo': 'Chamadas  Locais Móvel-Móvel  Extraoperadora '
                        'SMP-Local-MM-EO(VC1)',
                'tratamento-diferenciado': '-',
                'unidade-de-fornecimento': 'Minutos'},
            {'aplicabilidade-decreto': 'Não',
                'aplicabilidade-margem-de-preferencia': 'Não',
                'numero': 7,
                'quantidade': 6000,
                'titulo': 'Chamadas Locais Móvel-Fixo SMP-Local-MF (VC1)',
                'tratamento-diferenciado': '-',
                'unidade-de-fornecimento': 'Minutos'},
            {'aplicabilidade-decreto': 'Não',
                'aplicabilidade-margem-de-preferencia': 'Não',
                'numero': 8,
                'quantidade': 12000,
                'titulo': 'Pacote de Serviços SMP (Voz, Dados, SMS, Etc)',
                'tratamento-diferenciado': '-',
                'unidade-de-fornecimento': 'Minutos'},
            {'aplicabilidade-decreto': 'Não',
                'aplicabilidade-margem-de-preferencia': 'Não',
                'numero': 9,
                'quantidade': 6000,
                'titulo': 'Pacote de Serviços SMP (Voz, Dados, SMS, Etc)',
                'tratamento-diferenciado': '-',
                'unidade-de-fornecimento': 'Minutos'},
            {'aplicabilidade-decreto': 'Não',
                'aplicabilidade-margem-de-preferencia': 'Não',
                'numero': 10,
                'quantidade': 9000,
                'titulo': 'Pacote de Serviços SMP (Voz, Dados, SMS, Etc)',
                'tratamento-diferenciado': '-',
                'unidade-de-fornecimento': 'Ligação'},
            {'aplicabilidade-decreto': 'Não',
                'aplicabilidade-margem-de-preferencia': 'Não',
                'numero': 11,
                'quantidade': 9000,
                'titulo': 'Pacote de Serviços SMP (Voz, Dados, SMS, Etc)',
                'tratamento-diferenciado': '-',
                'unidade-de-fornecimento': 'Ligação'},
            {'aplicabilidade-decreto': 'Não',
                'aplicabilidade-margem-de-preferencia': 'Não',
                'numero': 12,
                'quantidade': 1800,
                'titulo': 'Pacote de Serviços SMP (Voz, Dados, SMS, Etc)',
                'tratamento-diferenciado': '-',
                'unidade-de-fornecimento': 'Minutos'},
            {'aplicabilidade-decreto': 'Não',
                'aplicabilidade-margem-de-preferencia': 'Não',
                'numero': 13,
                'quantidade': 3000,
                'titulo': 'Pacote de Serviços SMP (Voz, Dados, SMS, Etc)',
                'tratamento-diferenciado': '-',
                'unidade-de-fornecimento': 'Mensagem'},
            {'aplicabilidade-decreto': 'Não',
                'aplicabilidade-margem-de-preferencia': 'Não',
                'numero': 14,
                'quantidade': 3000,
                'titulo': 'Pacote de Serviços SMP (Voz, Dados, SMS, Etc)',
                'tratamento-diferenciado': '-',
                'unidade-de-fornecimento': 'Mensagem'},
            {'aplicabilidade-decreto': 'Não',
                'aplicabilidade-margem-de-preferencia': 'Não',
                'numero': 15,
                'quantidade': 6000,
                'titulo': 'Chamadas  Nacionais Móvel-Móvel Intraoperadora '
                        'SMP-LDN-MM-IO(VC2 e VC3)',
                'tratamento-diferenciado': '-',
                'unidade-de-fornecimento': 'Minutos'},
            {'aplicabilidade-decreto': 'Não',
                'aplicabilidade-margem-de-preferencia': 'Não',
                'numero': 16,
                'quantidade': 6000,
                'titulo': 'Chamadas  Nacionais Móvel-Móvel Extraoperadora '
                        'SMP-LDN-MM-EO(VC2 e VC3)',
                'tratamento-diferenciado': '-',
                'unidade-de-fornecimento': 'Minutos'},
            {'aplicabilidade-decreto': 'Não',
                'aplicabilidade-margem-de-preferencia': 'Não',
                'numero': 17,
                'quantidade': 6000,
                'titulo': 'Chamadas Nacionais Móvel-Fixo SMP-LDM-MF (VC2 e VC3)',
                'tratamento-diferenciado': '-',
                'unidade-de-fornecimento': 'Minutos'},
            {'aplicabilidade-decreto': 'Não',
                'aplicabilidade-margem-de-preferencia': 'Não',
                'numero': 18,
                'quantidade': 6000,
                'titulo': 'Chamadas  Nacionais Móvel-Móvel Intraoperadora '
                        'SMP-LDN-MM-IO(VC2 e VC3)',
                'tratamento-diferenciado': '-',
                'unidade-de-fornecimento': 'Minutos'},
            {'aplicabilidade-decreto': 'Não',
                'aplicabilidade-margem-de-preferencia': 'Não',
                'numero': 19,
                'quantidade': 6000,
                'titulo': 'Chamadas  Nacionais Móvel-Móvel Extraoperadora '
                        'SMP-LDN-MM-EO(VC2 e VC3)',
                'tratamento-diferenciado': '-',
                'unidade-de-fornecimento': 'Minutos'},
            {'aplicabilidade-decreto': 'Não',
                'aplicabilidade-margem-de-preferencia': 'Não',
                'numero': 20,
                'quantidade': 6000,
                'titulo': 'Chamadas Nacionais Móvel-Fixo SMP-LDM-MF (VC2 e VC3)',
                'tratamento-diferenciado': '-',
                'unidade-de-fornecimento': 'Minutos'}],
            'pregao-eletronico': 32018}

    assert statuse_detail.scrap_data() == output
    assert statuse_detail.data == output
