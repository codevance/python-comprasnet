import logging.config
from datetime import datetime, date, timedelta

import requests
from bs4 import BeautifulSoup

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
            page_results, is_last_page = self.get_search_result_page(data)
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
        print(str(response.status_code))
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


if __name__ == '__main__':
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
            },
        },
        'loggers': {
            '': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False
            },
        },
    })

    comprasnet = ComprasNet()
    results = comprasnet.search_auctions_by_date(datetime.now() - timedelta(days=3))
    print(results)