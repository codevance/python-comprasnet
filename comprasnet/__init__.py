import requests
from datetime import datetime, date
import logging
import logging.config
import os
from uuid import uuid4

log = logging.getLogger('comprasnet')


class ComprasNet:
    TMP_DIR = '/tmp/'
    SEARCH_BIDS_URL = "http://comprasnet.gov.br/ConsultaLicitacoes/ConsLicitacao_Relacao.asp"

    def __init__(self):
        pass

    def get_data_dict_to_search_bids(self):
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

    def search_bids_by_date(self, search_date):
        """Search bids only by date, retrieve and save page results in tmp directory and return
        a list of filenames saved."""
        filenames = []

        page = 0
        data = self.get_data_dict_to_search_bids()
        if not isinstance(search_date, date):
            search_date = search_date.date()

        log.info('getting bids from {:%d/%m/%Y}...'.format(search_date))
        while True:
            page += 1
            data['dt_publ_ini'] = search_date.strftime("%d/%m/%Y")
            data['dt_publ_fim'] = search_date.strftime("%d/%m/%Y")
            data['numpag'] = page

            log.debug('getting page {:04d}...'.format(page))
            filename, is_last_page = self.get_search_result_page(data)
            filenames.append(filename)
            if is_last_page:
                break

        return filenames

    def get_search_result_page(self, data):
        """Receive data dict, make the request and retrive search page. Save page and returns a
        tuple with filename and if is the last page"""
        is_last_page = False

        response = requests.get(self.SEARCH_BIDS_URL, data)
        if not response.status_code == 200:
            log.error('error trying to get bids from {}, page {}. Status code: {}'.format(
                data['dt_publ_ini'], data['numpag'], response.status_code
            ))
            return None, is_last_page

        filename = os.path.join(self.TMP_DIR, '{}.html'.format(uuid4()))
        log.debug('saving page in {}...'.format(filename))
        with open(filename, 'w') as handle:
            handle.write(response.text)

        if not 'id="proximo" name="btn_proximo"' in response.text:
            log.info('finished!')
            is_last_page = True

        return filename, is_last_page


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
    comprasnet.search_bids_by_date(datetime.now())
