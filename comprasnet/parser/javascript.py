from .onclick import OnClickFunctionJS
from bs4 import BeautifulSoup
import re


class JavaScriptParser:

    REGEX_JS = re.compile("^(?:javascript\:| |)*(\w*)\(([\w*| |\,|\'|\"|\_|\&|\=]*)\)\;$")

    def __init__(self, html):
        self.bs_object = BeautifulSoup(html, "html.parser")
        self.code = self._get_js_code()

    def _get_js_code(self):
        try:
            return self.bs_object.find_all('script', src=lambda x: x is None)[0].text
        except IndexError:
            return []

    def _clean_onlick_function(self, onclick_function):
        try:
            groups = self.REGEX_JS.search(onclick_function).groups()
            function_name = groups[0]
            parameters = [parameter.strip() for parameter in groups[-1].split(",")]
            return {"name": function_name, "parameters": parameters}
        except AttributeError:
            return {"name": "", "parameters": []}

    def get_js_function(self, function):
        begin = self.code.find("function {}(".format(function['name']))
        index_brace = self.code[begin:].find("{") + 1
        while True:
            open_braces = self.code[begin + index_brace:].find("{")
            close_braces = self.code[begin + index_brace:].find("}")
            if close_braces <= open_braces or (open_braces or close_braces) == -1:
                end = begin + index_brace + close_braces + 1
                break
            else:
                index_brace += close_braces + 1
        return OnClickFunctionJS(function, self.code[begin: end])

    def get_link_inside_onclick_function_by_id(self, id):
        element = self.bs_object.find(id=id)
        return self._get_onclick_function_link(element)

    def get_link_inside_onclick_function_by_name(self, name):
        element = self.bs_object.find("", {"name": name})
        return self._get_onclick_function_link(element)

    def _get_onclick_function_link(self, element):
        try:
            onclick_function = self._clean_onlick_function(element['onclick'])
            function = self.get_js_function(onclick_function)
            return function.get_url_with_parameters()
        except TypeError:
            return
