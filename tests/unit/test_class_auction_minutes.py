import requests_mock
import os
import json


ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_to_json_should_return_auction_fields(auction_minute):
    with open("{}/assets/scrap_data_auction_minutes.json".format(ROOT_PATH)) as response:
        expected = json.loads(response.read().replace("\n", ""))
    result = json.loads(auction_minute.to_json())
    assert result == expected


def test_to_json_size(auction_minute):
    result = json.loads(auction_minute.to_json())
    assert len(result) == 9


def test_scrap_data_result(auction_minute):
    with open("{}/assets/scrap_data_auction_minutes.json".format(ROOT_PATH)) as response:
        expected = json.loads(response.read())
    result = auction_minute.scrap_data()
    for key, value in expected.items():
        assert result[key] == value


def test_url(auction_minute):
    expected = "http://comprasnet.gov.br/livre/pregao/ata2.asp?co_no_uasg=1234&numprp=987"
    assert auction_minute.url == expected


def test_get_params(auction_minute):
    expected = dict(co_no_uasg=1234, numprp=987)
    assert auction_minute.get_params() == expected


def test_get_data(auction_minute):
    with requests_mock.mock() as mock:
        mock.get(auction_minute.url, text="Success")
        assert auction_minute.get_data() == "Success"


def test_keys_scrap_data(auction_minute):
    result = auction_minute.scrap_data()
    assert "result_per_provider" in result
    assert "declaration" in result
    assert "minutes_of_backup_register" in result
    assert "proposal_attachments" in result
    assert "terms_of_adjudication" in result
    assert "terms_of_homologation" in result
    assert "clarification" in result
    assert "auction_minute" in result
    assert "auction_id" in result


def test_get_result_per_provider_url(auction_minute):
    expected = "http://comprasnet.gov.br/livre/pregao/FornecedorResultado.asp?" \
               "prgcod=712965&strTipoPregao=E"
    result = auction_minute.get_result_per_provider_url()
    assert result == expected


def test_get_declaration_url(auction_minute):
    expected = "http://comprasnet.gov.br/livre/pregao/declaracoesProposta.asp?prgCod=712965"
    result = auction_minute.get_declaration_url()
    assert result == expected


def test_get_terms_of_adjudication_url(auction_minute):
    expected = "http://comprasnet.gov.br/livre/pregao/termojulg.asp?"\
               "prgcod=712965&Acao=A&co_no_uasg=986589&numprp=192018&f_lstSrp=&f_Uf=&f_numPrp="\
               "&f_coduasg=&f_tpPregao=&f_lstICMS=&f_dtAberturaIni=&f_dtAberturaFim="
    result = auction_minute.get_terms_of_adjudication_url()
    assert result == expected


def test_get_clarification_url(auction_minute):
    expected = "http://comprasnet.gov.br/livre/pregao/avisos1.asp?" \
               "prgCod=712965&Origem=Avisos&Tipo=E"
    result = auction_minute.get_clarification_url()
    assert result == expected


def test_get_proposal_attachments(auction_minute):
    expected = "http://comprasnet.gov.br/livre/pregao/AnexosProposta.asp?" \
               "uasg=986589&numprp=192018&prgcod=712965"
    assert auction_minute.get_proposal_attachments() == expected


def test_get_terms_of_homologation(auction_minute):
    expected = "http://comprasnet.gov.br/livre/pregao/termohom.asp?prgcod=712965&co_no_uasg=986589" \
               "&numprp=192018&f_lstSrp=" \
               "&f_Uf=&f_numPrp=&f_coduasg=&f_tpPregao=&f_lstICMS=&f_dtAberturaIni=&f_dtAberturaFim="
    assert auction_minute.get_terms_of_homologation() == expected


def test_get_minutes_of_backup_register(auction_minute):
    expected = "http://comprasnet.gov.br/livre/pregao/termocadres.asp?prgcod=712965" \
               "&co_no_uasg=986589&numprp=192018&f_lstSrp=&f_Uf=&f_numPrp=&f_coduasg=" \
               "&f_tpPregao=&f_lstICMS=&f_dtAberturaIni=&f_dtAberturaFim="
    assert auction_minute.get_minutes_of_backup_register() == expected


def test_get_auction_minute(auction_minute):
    expected = "http://comprasnet.gov.br/livre/pregao/AtaEletronico.asp?" \
               "co_no_uasg=986589&&uasg=986589&numprp=192018&Seq=1&f_lstSrp=" \
               "&f_Uf=&f_numPrp=&f_coduasg=&f_tpPregao=&f_lstICMS=" \
               "&f_dtAberturaIni=&f_dtAberturaFim="
    assert auction_minute.get_auction_minute() == expected


def test_get_auction_id(auction_minute):
    expected = "Nº 00019/2018 (SRP)"
    assert auction_minute.get_auction_id() == expected
