from urllib.parse import urlencode
from comprasnet.parser.javascript import JavaScriptParser
from . import BaseDetail, log
from bs4 import BeautifulSoup
import requests
import json


class AuctionMinutes(BaseDetail):
    ROOT_URL = "http://comprasnet.gov.br/livre/pregao/"
    DETAIL_URL = "{}ata2.asp".format(ROOT_URL)

    def __init__(self, co_no_uasg, numprp):
        self.co_no_uasg = co_no_uasg
        self.numprp = numprp
        self._data = self.get_data()
        self.bs_object = BeautifulSoup(self._data, "html.parser")
        self.js_parser = JavaScriptParser(self._data)

    @property
    def url(self):
        return '{url}?{parameters}'.format(url=self.DETAIL_URL,
                                           parameters=urlencode(self.get_params()))

    def get_params(self):
        params = {"co_no_uasg": self.co_no_uasg,
                  "numprp": self.numprp}
        return self._order_dict(params)

    def get_data(self):
        response = requests.get(self.DETAIL_URL, params=self.get_params())
        if not response.status_code == requests.codes.ok:
            log.error('error trying to get "Ata" from "Pregão" {}/{}. Status code: {}'.format(
                self.co_no_uasg, self.numprp, response.status_code
            ))
            return
        return response.text

    def scrap_data(self):
        fields = {"result_per_provider": self.get_result_per_provider_url(),
                  "declaration": self.get_declaration_url(),
                  "minutes_of_backup_register": self.get_minutes_of_backup_register(),
                  "proposal_attachments": self.get_proposal_attachments(),
                  "terms_of_adjudication": self.get_terms_of_adjudication_url(),
                  "terms_of_homologation": self.get_terms_of_homologation(),
                  "clarification": self.get_clarification_url(),
                  "auction_minute": self.get_auction_minute(),
                  "auction_id": self.get_auction_id()
                  }
        return fields

    def get_result_per_provider_url(self):
        link = self.js_parser.get_link_inside_onclick_function_by_id("btnResultadoFornecr")
        return self._get_full_link(link)

    def get_declaration_url(self):
        link = self.js_parser.get_link_inside_onclick_function_by_id("btnDeclaracoes")
        return self._get_full_link(link)

    def get_minutes_of_backup_register (self):
        link = self.js_parser.get_link_inside_onclick_function_by_name("atacadastroreserva")
        return self._get_full_link(link)

    def get_proposal_attachments(self):
        link = self.js_parser.get_link_inside_onclick_function_by_name("AnexosProposta")
        return self._get_full_link(link)

    def get_terms_of_adjudication_url(self):
        link = self.js_parser.get_link_inside_onclick_function_by_id("btnTermAdj")
        return self._get_full_link(link)

    def get_terms_of_homologation(self):
        link = self.js_parser.get_link_inside_onclick_function_by_name("termodehomologacao")
        return self._get_full_link(link)

    def get_clarification_url(self):
        link = self.js_parser.get_link_inside_onclick_function_by_id("esclarecimento")
        return self._get_full_link(link)

    def get_auction_minute(self):
        name = "{}-{}-1".format(self.co_no_uasg, self.numprp)
        link = self.js_parser.get_link_inside_onclick_function_by_name(name)
        return self._get_full_link(link)

    def get_auction_id(self):
        return self.bs_object.find("span", {"class": "mensagem2"}).text

    def _get_full_link(self, link):
        return "{}{}".format(self.ROOT_URL, link)

    def to_json(self):
        return json.dumps(self._order_dict(self.scrap_data()))
