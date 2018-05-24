from datetime import datetime
import math
import requests
from bs4 import BeautifulSoup
from slugify import slugify
from unicodedata import normalize
from . import log


class SearchAuctions:
    """Handle with this search: http://comprasnet.gov.br/ConsultaLicitacoes/ConsLicitacao_Filtro
    .asp"""

    SEARCH_URL = "http://comprasnet.gov.br/ConsultaLicitacoes/ConsLicitacao_Relacao.asp"
    OFFSET = 10

    def __init__(self, day=datetime.today(), **kwargs):
        self.day = day
        self.total_results = 0
        self.current_page = 1

    @property
    def total_pages(self):
        """Return total of pages based on attributes information"""
        return math.ceil(self.total_results / self.OFFSET)

    @property
    def is_done(self):
        return self.current_page > self.total_pages

    @property
    def results(self):
        """Generator that return each page result on every iteration."""
        while not self.is_done:
            data = self.get_search_page_data()
            if data:
                yield self.scrap_search_page(data)
                self.current_page += 1
        self.current_page = 1

    def search(self):
        """method that starts class logic. After this method, itarate over `restults` property to
        get the class results"""
        self.get_search_metadata()

    def get_search_params(self):
        """mount the POST params dict to send to request"""
        return {
            "numprp": "",
            "dt_publ_ini": self.day.strftime("%d/%m/%Y"),
            "dt_publ_fim": self.day.strftime("%d/%m/%Y"),
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
            "numpag": self.current_page,
        }

    def get_search_metadata(self):
        """Retrieve informations about the search to mount all class logic. In practice,
        its the start command."""
        log.info('getting informations from auctions from {:%d/%m/%Y}...'.format(self.day))
        data = self.get_search_params()

        response = requests.get(self.SEARCH_URL, data)
        if not response.status_code == requests.codes.ok:
            log.error('error trying to get auctions from {}, page {}. Status code: {}'.format(
                data['dt_publ_ini'], data['numpag'], response.status_code
            ))
            return

        bs_object = BeautifulSoup(response.text, 'html.parser')
        footer = None
        for item in bs_object.find_all('td', class_='td_titulo_campo'):
            if '(Licita' in str(item):
                footer = item.find('center').text

        if footer:
            total_results = footer.split(' de ')[-1]
            self.total_results = int(total_results.replace(')', ''))

    def get_search_page_data(self):
        """Retrieve raw html from current page."""
        log.info('getting auctions from {:%d/%m/%Y}, page {}...'.format(self.day,
                                                                        self.current_page))

        data = self.get_search_params()
        response = requests.get(self.SEARCH_URL, data)
        if not response.status_code == requests.codes.ok:
            log.error('error trying to get auctions from {}, page {}. Status code: {}'.format(
                data['dt_publ_ini'], data['numpag'], response.status_code
            ))
            return

        return response.text

    def scrap_search_page(self, data):
        """ Gets data from results page of auctions search and
            retrieve a dict with scrapped informations.
        """
        page_results = []

        bs_object = BeautifulSoup(data, "html.parser")
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

            for line in str(td).split("<br/>"):

                if 'digo da UASG' in line:

                    try:
                        current_result['cabecalho'] = header
                        codigo_da_uasg_chave = line.split(":")[0]
                        codigo_da_uasg_chave = slugify(codigo_da_uasg_chave)
                        codigo_da_uasg_valor = line.split("digo da UASG: ")[-1].strip()
                        current_result[codigo_da_uasg_chave] = codigo_da_uasg_valor
                    except IndexError as e:
                        log.error('error when trying to extract "código da UASG" - {}'.format(
                            current_result))
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
                        log.error(
                            'error when trying to extract "Pregão Eletrônico No" - {}'.format(
                                current_result))
                        log.exception(e)
                        pass

                if 'Objeto:' in line:
                    try:
                        objeto_chave = line.split()[1].split(':')[0].lower()
                        objeto_valor = line.split('Objeto:')[-1].strip()
                        current_result[objeto_chave] = objeto_valor
                    except IndexError as e:
                        log.error('error when trying to extract "Objeto" - {}'.format(
                            current_result))
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
                        log.error('error when trying to extract "Edital a partir de" - {}'.format(
                            current_result))
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
                        log.error('error when trying to extract "Endereço" - {}'.format(
                            current_result))
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
                        log.error('error when trying to extract "Telefone" - {}'.format(
                            current_result))
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
                        log.error('error when trying to extract "Fax" - {}'.format(current_result))
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
                        log.error('error when trying to extract "Entrega da proposta" - {}'.format(
                            current_result))
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
                        log.error(
                            'error when trying to extract "Abertura da proposta" - {}'.format(
                                current_result))
                        log.exception(e)
                        pass

            page_results.append(current_result)
        return page_results
