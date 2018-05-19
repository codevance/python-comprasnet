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

    output = {
        'pregao-eletronico': 32018,
        'itens': [
            {
                'descricao': 'Pacote de Serviços SMP (Voz, Dados, SMS, Etc)',
                'numero': '1'
            },
            {
                'descricao': 'Pacote de Serviços SMP (Voz, Dados, SMS, Etc)',
                'numero': '2'
            },
            {
                'descricao': 'Pacote de Serviços SMP (Voz, Dados, SMS, Etc)',
                'numero': '3'
            },
            {
                'descricao': 'Pacote de Serviços SMP (Voz, Dados, SMS, Etc)',
                'numero': '4'
            },
            {
                'descricao': 'Chamadas  Locais Móvel-Móvel  Intraoperadora SMP-Local-MM-IO(VC1)',
                'numero': '5'
            },
            {
                'descricao': 'Chamadas  Locais Móvel-Móvel  Extraoperadora SMP-Local-MM-EO(VC1)',
                'numero': '6'
            },
            {
                'descricao': 'Chamadas Locais Móvel-Fixo SMP-Local-MF (VC1)',
                'numero': '7'
            },
            {
                'descricao': 'Pacote de Serviços SMP (Voz, Dados, SMS, Etc)',
                'numero': '8'
            },
            {
                'descricao': 'Pacote de Serviços SMP (Voz, Dados, SMS, Etc)',
                'numero': '9'
            },
            {
                'descricao': 'Pacote de Serviços SMP (Voz, Dados, SMS, Etc)',
                'numero': '10'
            },
            {
                'descricao': 'Pacote de Serviços SMP (Voz, Dados, SMS, Etc)',
                'numero': '11'
            },
            {
                'descricao': 'Pacote de Serviços SMP (Voz, Dados, SMS, Etc)',
                'numero': '12'
            },
            {
                'descricao': 'Pacote de Serviços SMP (Voz, Dados, SMS, Etc)',
                'numero': '13'
            },
            {
                'descricao': 'Pacote de Serviços SMP (Voz, Dados, SMS, Etc)',
                'numero': '14'
            },
            {
                'descricao': 'Chamadas  Nacionais Móvel-Móvel Intraoperadora SMP-LDN-MM-IO(VC2 '
                               'e VC3)',
                'numero': '15'
            },
            {
                'descricao': 'Chamadas  Nacionais Móvel-Móvel Extraoperadora SMP-LDN-MM-EO(VC2 '
                               'e VC3)',
                'numero': '16'
            },
            {
                'descricao': 'Chamadas Nacionais Móvel-Fixo SMP-LDM-MF (VC2 e VC3)',
                'numero': '17'
            },
            {
                'descricao': 'Chamadas  Nacionais Móvel-Móvel Intraoperadora SMP-LDN-MM-IO(VC2 '
                               'e VC3)',
                'numero': '18'
            },
            {
                'descricao': 'Chamadas  Nacionais Móvel-Móvel Extraoperadora SMP-LDN-MM-EO(VC2 '
                               'e VC3)',
                'numero': '19'
            },
            {
                'descricao': 'Chamadas Nacionais Móvel-Fixo SMP-LDM-MF (VC2 e VC3)',
                'numero': '20'
            }
        ],
        'codigo-da-uasg': 160478
    }
    assert statuse_detail.scrap_data() == output
    assert statuse_detail.data == output
