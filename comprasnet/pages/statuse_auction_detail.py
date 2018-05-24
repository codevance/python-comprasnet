from . import BaseDetail, log
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import requests


class StatuseAuctionDetail(BaseDetail):
    """Retrive information from statuse details, in this page:
    http://comprasnet.gov.br/ConsultaLicitacoes/download/download_editais_detalhe.asp"""

    DETAIL_URL = "http://comprasnet.gov.br/ConsultaLicitacoes/download/download_editais_detalhe.asp"

    @property
    def url(self):
        return "{}?{}".format(self.DETAIL_URL, urlencode(self.get_params()))

    def get_params(self):
        """Forcing that params stay ordained"""
        params = {
            'coduasg': self.uasg_code,
            'numprp': self.auction_code,
            'modprp': 5,
        }
        return self._order_dict(params)

    def get_data(self):
        response = requests.get(self.DETAIL_URL, params=self.get_params())
        if not response.status_code == requests.codes.ok:
            log.error('error trying to get statuse from auction {}/{}. Status code: {}'.format(
                self.uasg_code, self.auction_code, response.status_code
            ))
            return

        return response.text

    def scrap_data(self):
        output = {
            'codigo-da-uasg': int(self.uasg_code),
            'pregao-eletronico': int(self.auction_code),
        }
        data = self.get_data()
        bs_object = BeautifulSoup(data, "html.parser")

        for span in bs_object('span', class_='tex3b'):
            if 'Itens de ' in span.text:
                items_table = span.find_next('table')

                output['itens'] = []
                for items in items_table.find_all('tr'):
                    item = {}
                    header = items.find('span', class_='tex3b')
                    description = items.find('span', class_='tex3')
                    try:
                        item_number, title = header.text.split(' - ')[:2]
                        item['numero'] = int(item_number)
                        item['titulo'] = title.strip()

                        description = str(description).split('<br/>')
                        description_text = description[0].split('<br/>')
                        description_text = description_text[0].split('<span class="tex3">')[1]
                        diff_treattment = description[1].split(':')

                        item['tratamento-diferenciado'] = diff_treattment[1].strip()
                        item['aplicabilidade-decreto'] = description[2].split(':')[1].strip()
                        item['aplicabilidade-margem-de-preferencia'] = description[3].split(':')[1].strip()
                        item['quantidade'] = int(description[4].split(':')[1].strip())
                        item['unidade-de-fornecimento'] = description[5].split(':')[1].strip('</span>').split()[0]

                        output['itens'].append(item)
                    except (ValueError, IndexError) as e:
                        log.error('error on extract description in "{}". {}'.format(
                            items, self.url))
                        log.exception(e)
        return output
