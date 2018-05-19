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


@mock.patch('comprasnet.StatuseDetail.get_data')
def test_method_scrap_data(get_data):
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            '../assets/statusedetail_page_example.html')
    with codecs.open(filename, 'r', 'iso-8859-1') as handle:
        page_content = handle.read()

    get_data.return_value = page_content

    output = {
        'auction_code': 32018,
        'items': [
            {
                'description': 'Pacote de Serviços SMP (Voz, Dados, SMS, Etc)',
                'number': '1'
            },
            {
                'description': 'Pacote de Serviços SMP (Voz, Dados, SMS, Etc)',
                'number': '2'
            },
            {
                'description': 'Pacote de Serviços SMP (Voz, Dados, SMS, Etc)',
                'number': '3'
            },
            {
                'description': 'Pacote de Serviços SMP (Voz, Dados, SMS, Etc)',
                'number': '4'
            },
            {
                'description': 'Chamadas  Locais Móvel-Móvel  Intraoperadora SMP-Local-MM-IO(VC1)',
                'number': '5'
            },
            {
                'description': 'Chamadas  Locais Móvel-Móvel  Extraoperadora SMP-Local-MM-EO(VC1)',
                'number': '6'
            },
            {
                'description': 'Chamadas Locais Móvel-Fixo SMP-Local-MF (VC1)',
                'number': '7'
            },
            {
                'description': 'Pacote de Serviços SMP (Voz, Dados, SMS, Etc)',
                'number': '8'
            },
            {
                'description': 'Pacote de Serviços SMP (Voz, Dados, SMS, Etc)',
                'number': '9'
            },
            {
                'description': 'Pacote de Serviços SMP (Voz, Dados, SMS, Etc)',
                'number': '10'
            },
            {
                'description': 'Pacote de Serviços SMP (Voz, Dados, SMS, Etc)',
                'number': '11'
            },
            {
                'description': 'Pacote de Serviços SMP (Voz, Dados, SMS, Etc)',
                'number': '12'
            },
            {
                'description': 'Pacote de Serviços SMP (Voz, Dados, SMS, Etc)',
                'number': '13'
            },
            {
                'description': 'Pacote de Serviços SMP (Voz, Dados, SMS, Etc)',
                'number': '14'
            },
            {
                'description': 'Chamadas  Nacionais Móvel-Móvel Intraoperadora SMP-LDN-MM-IO(VC2 '
                               'e VC3)',
                'number': '15'
            },
            {
                'description': 'Chamadas  Nacionais Móvel-Móvel Extraoperadora SMP-LDN-MM-EO(VC2 '
                               'e VC3)',
                'number': '16'
            },
            {
                'description': 'Chamadas Nacionais Móvel-Fixo SMP-LDM-MF (VC2 e VC3)',
                'number': '17'
            },
            {
                'description': 'Chamadas  Nacionais Móvel-Móvel Intraoperadora SMP-LDN-MM-IO(VC2 '
                               'e VC3)',
                'number': '18'
            },
            {
                'description': 'Chamadas  Nacionais Móvel-Móvel Extraoperadora SMP-LDN-MM-EO(VC2 '
                               'e VC3)',
                'number': '19'
            },
            {
                'description': 'Chamadas Nacionais Móvel-Fixo SMP-LDM-MF (VC2 e VC3)',
                'number': '20'
            }
        ],
        'uasg_code': 160478
    }
    assert statuse_detail.scrap_data() == output
    assert statuse_detail.data == output
