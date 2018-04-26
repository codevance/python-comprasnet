from comprasnet import ComprasNet
from unittest import mock
from datetime import datetime


def test_should_return_attributes():
    comprasnet = ComprasNet()
    assert hasattr(comprasnet, 'TMP_DIR')
    assert hasattr(comprasnet, 'SEARCH_BIDS_URL')


def test_should_return_correct_dict_structure():
    comprasnet = ComprasNet()
    assert list(comprasnet.get_data_dict_to_search_bids().keys()) == [
        'numprp', 'dt_publ_ini', 'dt_publ_fim', 'chkModalidade', 'chk_concor', 'chk_pregao',
        'chk_rdc', 'optTpPesqMat', 'optTpPesqServ', 'chkTodos', 'chk_concorTodos',
        'chk_pregaoTodos', 'txtlstUf', 'txtlstMunicipio', 'txtlstUasg', 'txtlstGrpMaterial',
        'txtlstClasMaterial', 'txtlstMaterial', 'txtlstGrpServico', 'txtlstServico', 'txtObjeto',
        'numpag'
    ]


@mock.patch('comprasnet.ComprasNet.get_search_result_page')
def test_should_search_bids_by_date(get_search_result_page):
    get_search_result_page.return_value = ('/tmp/test.html', True)
    comprasnet = ComprasNet()

    filenames = comprasnet.search_bids_by_date(datetime.now())
    assert filenames == ['/tmp/test.html']
    assert get_search_result_page.called_with(comprasnet.SEARCH_BIDS_URL,
                                              comprasnet.get_data_dict_to_search_bids())


@mock.patch('requests.get')
def test_should_retrive_and_save_search_bids_results(get):
    assert False
