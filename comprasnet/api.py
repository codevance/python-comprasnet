import logging

import requests

log = logging.getLogger('comprasnet')


class ComprasNetApi:
    BASE_SEARCH_URL = "http://compras.dados.gov.br/{modulo}/{version}/{metodo}.{formato}"
    BASE_DETAIL_URL = "http://compras.dados.gov.br/{modulo}/{version}/{metodo}/{item}.{formato}"

    def __init__(self):
        self.last_response = None

    def _raw_request(self, url, **params):
        log.info('requesting to {}...'.format(url))
        response = requests.get(url, params=params)
        log.debug('response status code: {}'.format(response.status_code))

        self.last_response = response
        return response

    def _request_search(self, modulo, metodo, version='v1', formato='json', **params):
        url = self.BASE_SEARCH_URL.format(modulo=modulo, metodo=metodo, version=version,
                                          formato=formato)
        return self._raw_request(url, **params)

    def _request_detail(self, modulo, metodo, item, version='id', formato='json', **params):
        url = self.BASE_DETAIL_URL.format(modulo=modulo, metodo=metodo, version=version,
                                          formato=formato, item=item)
        return self._raw_request(url, **params)

    def get_licitacoes_uasg(self, uasg_id, **params):
        """http://compras.dados.gov.br/docs/licitacoes/uasg.html"""
        response = self._request_detail('licitacoes', 'uasg', uasg_id, **params)
        if response.status_code == 200:
            return response.json()

    def get_licitacoes_uasgs(self, **params):
        """http://compras.dados.gov.br/docs/licitacoes/v1/uasgs.html"""
        response = self._request_search('licitacoes', 'uasgs', **params)
        if response.status_code == 200:
            return response.json()


