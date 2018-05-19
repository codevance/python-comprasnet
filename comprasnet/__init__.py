import logging.config
from datetime import date, datetime
import re

import requests
from bs4 import BeautifulSoup
from slugify import slugify
from unicodedata import normalize

from .api import ComprasNetApi

log = logging.getLogger('comprasnet')


class ComprasNet:
    TMP_DIR = '/tmp/'
    SEARCH_BIDS_URL = "http://comprasnet.gov.br/ConsultaLicitacoes/ConsLicitacao_Relacao.asp"

    def __init__(self):
        pass

    def get_data_dict_to_search_auctions(self):
        return {
            "numprp": "",
            "dt_publ_ini": None,
            "dt_publ_fim": None,
            "chkModalidade": "1,2,3,20,5,99",
            "chk_concor": "",
            "chk_pregao": "",
            "chk_rdc": "",
            "optTpPesqMat": "M",
            "optTpPesqServ": "S",
            "chkTodos": "-1",
            "chk_concorTodos": "",
            "chk_pregaoTodos": "",
            "txtlstUf": "",
            "txtlstMunicipio": "",
            "txtlstUasg": "",
            "txtlstGrpMaterial": "",
            "txtlstClasMaterial": "",
            "txtlstMaterial": "",
            "txtlstGrpServico": "",
            "txtlstServico": "",
            "txtObjeto": "",
            "numpag": 1,
        }

    def get_data_auctions_pages(self, data):
        """ Gets data from results page of auctions search and
            retrieve a dict with scrapped informations.
        """
        is_last_page = False
        page_results = []

        response = requests.get(self.SEARCH_BIDS_URL, data)
        if not response.status_code == requests.codes.ok:
            log.error('error trying to get auctions from {}, page {}. Status code: {}'.format(
                data['dt_publ_ini'], data['numpag'], response.status_code
            ))
            return None, is_last_page

        bs_object = BeautifulSoup(response.text, "html.parser")
        header = []
        for form in bs_object.find_all('form'):
            if 'Form' not in form.attrs['name']:
                continue

            current_result = {}
            td = form.find('tr', class_="tex3").find('td')

            titulo_td = form.find_all('td', class_="td_titulo_campo")[1]
            cidade = str(titulo_td).split()[-2]
            cidade = cidade.strip('-')
            uf = str(titulo_td).split()[-1]
            uf = uf.strip('</td>')

            current_result['cidade'] = cidade
            current_result['uf'] = uf
            headers = [element for element in td.b.contents
                       if 'Código da UASG' not in element]
            headers = [element.strip() for element in headers
                       if isinstance(element, str)]
            current_result['cabecalho'] = headers

            for line in str(td).split("<br/>"):

                if 'digo da UASG' in line:
                    try:
                        current_result['cabecalho'] = header
                        codigo_da_uasg_chave = line.split(":")[0]
                        codigo_da_uasg_chave = slugify(codigo_da_uasg_chave)
                        codigo_da_uasg_valor = line.split("digo da UASG: ")[-1].strip()
                        current_result[codigo_da_uasg_chave] = codigo_da_uasg_valor
                    except IndexError as e:
                        log.error('error when trying to extract "código da UASG":')
                        log.exception(e)
                        pass

                if 'Pregão Eletrônico Nº' in line:
                    try:
                        pregao_eletronico_chave = line.split('Nº')[0].split('<b>')[-1]
                        pregao_eletronico_chave = slugify(pregao_eletronico_chave)
                        pregao_eletronico_valor = line.split("Pregão Eletrônico Nº ")[-1].strip()
                        pregao_eletronico_valor = pregao_eletronico_valor.replace('/', '')
                        pregao_eletronico_valor = pregao_eletronico_valor.replace('<b>', '')
                        pregao_eletronico_valor = pregao_eletronico_valor.replace('</b>', '')
                        current_result[pregao_eletronico_chave] = pregao_eletronico_valor
                    except IndexError as e:
                        log.error('error when trying to extract "Pregão Eletrônico No":')
                        log.exception(e)
                        pass

                if 'Objeto:' in line:
                    try:
                        objeto_chave = line.split()[1].split(':')[0].lower()
                        objeto_valor = line.split('Objeto:')[-1].strip()
                        current_result[objeto_chave] = objeto_valor
                    except IndexError as e:
                        log.error('error when trying to extract "Objeto":')
                        log.exception(e)
                        pass

                if 'Edital a partir de' in line:

                    try:
                        edital_a_partir_de = line.split(':')[1].strip()
                        edital_a_partir_de = edital_a_partir_de.split('</b>')[1]
                        edital_a_partir_de = normalize('NFKD', edital_a_partir_de)
                        edital_a_partir_de = edital_a_partir_de.split('das')[0]
                        edital_a_partir_de = edital_a_partir_de.replace(' ', '')
                        edital_a_partir_de_data = datetime.strptime(edital_a_partir_de,
                                                                    '%d/%m/%Y').date()
                        current_result['edital-a-partir-de-str'] = edital_a_partir_de
                        current_result['edital-a-partir-de'] = edital_a_partir_de_data
                    except IndexError as e:
                        log.error('error when trying to extract "Edital a partir de":')
                        log.exception(e)
                        pass

                if 'Endereço' in line:
                    try:
                        endereco_chave = line.split()[0].strip('<b>')
                        endereco_chave = endereco_chave.split(':</')[0]
                        endereco_chave = slugify(endereco_chave)
                        endereco_valor = line.split(':')[1]
                        endereco_valor = endereco_valor.split('</b>')[1]
                        endereco_valor = normalize('NFKD', endereco_valor)
                        current_result[endereco_chave] = endereco_valor
                    except IndexError as e:
                        log.error('error when trying to extract "Endereço":')
                        log.exception(e)
                        pass

                if 'Telefone' in line:
                    try:
                        telefone_chave = line.split(':')[0]
                        telefone_chave = telefone_chave.split('<b>')[1]
                        telefone_chave = slugify(telefone_chave)
                        telefone_valor = line.split(':')[1]

                        if telefone_valor:
                            telefone_valor = telefone_valor.split('</b>')[1]
                            telefone_valor = normalize('NFKD', telefone_valor)
                            telefone_valor = telefone_valor.strip(' ')
                            telefone_valor = telefone_valor.replace('0xx', '')
                        else:
                            telefone_valor = None

                        current_result[telefone_chave] = telefone_valor
                    except IndexError as e:
                        log.error('error when trying to extract "Telefone":')
                        log.exception(e)
                        pass

                if 'Fax' in line:
                    try:
                        fax_chave = line.split(':')[0]
                        fax_chave = fax_chave.split('<b>')[1]
                        fax_chave = slugify(fax_chave)
                        fax_valor = line.split(':')[1]

                        if fax_valor:
                            fax_valor = fax_valor.split('</b>')[1]
                            fax_valor = fax_valor.replace(' ', '')
                            fax_valor = normalize('NFKD', fax_valor)
                            fax_valor = fax_valor.replace(' ', '')
                            fax_valor = fax_valor.replace('0xx', '')
                        else:
                            fax_valor = None

                        current_result[fax_chave] = fax_valor
                    except IndexError as e:
                        log.error('error when trying to extract "Fax":')
                        log.exception(e)
                        pass

                if 'Entrega da Proposta' in line:
                    try:
                        entrega_proposta_chave = line.split(':')[0]
                        entrega_proposta_chave = entrega_proposta_chave.split('<b>')[1]
                        entrega_proposta_chave = slugify(entrega_proposta_chave)
                        entrega_proposta_chave_str = '{}{}'.format(entrega_proposta_chave, '-str')

                        entrega_proposta_valor = line.split(':')[1]
                        entrega_proposta_valor = entrega_proposta_valor.split('</b>')[1]
                        entrega_proposta_valor_str = entrega_proposta_valor.split()[3]
                        entrega_proposta_valor_date = datetime.strptime(entrega_proposta_valor_str,
                                                                        '%d/%m/%Y').date()
                        current_result[entrega_proposta_chave_str] = entrega_proposta_valor_str
                        current_result[entrega_proposta_chave] = entrega_proposta_valor_date
                    except IndexError as e:
                        log.error('error when trying to extract "Entrega da proposta":')
                        log.exception(e)
                        pass

                if 'Abertura da Proposta' in line:
                    try:
                        abertura_proposta_chave = line.split(':')[0]
                        abertura_proposta_chave = abertura_proposta_chave.split('<b>')[1]
                        abertura_proposta_chave = slugify(abertura_proposta_chave)
                        abertura_proposta_chave_str = '{}{}'.format(abertura_proposta_chave, '-str')
                        abertura_proposta_valor = line.split(':')[1]
                        abertura_proposta_str = abertura_proposta_valor.split()[2]
                        abertura_proposta_data = datetime.strptime(abertura_proposta_str,
                                                                   '%d/%m/%Y').date()
                        current_result[abertura_proposta_chave_str] = abertura_proposta_str
                        current_result[abertura_proposta_chave] = abertura_proposta_data
                    except IndexError as e:
                        log.error('error when trying to extract "Abertura da proposta":')
                        log.exception(e)
                        pass

            page_results.append(current_result)

        if not 'id="proximo" name="btn_proximo"' in response.text:
            log.info('finished!')
            is_last_page = True
        return page_results, is_last_page

    def search_auctions_by_date(self, search_date):
        """Search auctions only by date, retrieve and save page results in tmp directory and return
        a list of filenames saved."""
        results = []

        page = 0
        data = self.get_data_dict_to_search_auctions()
        if not isinstance(search_date, date):
            search_date = search_date.date()

        log.info('getting auctions from {:%d/%m/%Y}...'.format(search_date))
        while True:
            page += 1
            data['dt_publ_ini'] = search_date.strftime("%d/%m/%Y")
            data['dt_publ_fim'] = search_date.strftime("%d/%m/%Y")
            data['numpag'] = page

            log.debug('getting page {:04d}...'.format(page))
            # page_results, is_last_page = self.get_search_result_page(data)
            page_results, is_last_page = self.get_data_auctions_pages(data)
            results += page_results
            if is_last_page:
                break

        return results

    def get_search_result_page(self, data):
        """Receive data dict, make the request and retrive search page. Save page and returns a
        tuple with filename and if is the last page"""
        is_last_page = False
        page_results = []

        response = requests.get(self.SEARCH_BIDS_URL, data)
        if not response.status_code == requests.codes.ok:
            log.error('error trying to get auctions from {}, page {}. Status code: {}'.format(
                data['dt_publ_ini'], data['numpag'], response.status_code
            ))
            return None, is_last_page

        bs_object = BeautifulSoup(response.text, "html.parser")
        for form in bs_object.find_all('form'):
            if 'Form' not in form.attrs['name']:
                continue

            current_result = {}
            td = form.find('tr', class_="tex3").find('td')

            for line in str(td).split("<br/>"):
                if 'digo da UASG' in line:
                    codigo_da_uasg = line.split("digo da UASG: ")[-1].strip()
                    current_result['codigo_da_uasg'] = codigo_da_uasg

                if 'Pregão Eletrônico Nº' in line:
                    pregao_eletronico = line.split("Pregão Eletrônico Nº ")[-1].strip()
                    pregao_eletronico = pregao_eletronico.replace('/', '')
                    pregao_eletronico = pregao_eletronico.replace('<b>', '')
                    pregao_eletronico = pregao_eletronico.replace('</b>', '')
                    current_result['pregao_eletronico'] = pregao_eletronico

            page_results.append(current_result)

        if not 'id="proximo" name="btn_proximo"' in response.text:
            log.info('finished!')
            is_last_page = True

        return page_results, is_last_page
