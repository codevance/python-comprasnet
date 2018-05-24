import re


class OnClickFunctionJS:

    HREF_REGEX = re.compile(r'document.location.href[ |]*=[ |]*([\w|.?|=|+| |"|\'|&]*)')
    FUNCTION_REGEX = re.compile(r"function[| ]*(\w*)\(([\w*| |\,|]*)\)")
    URL_REGEX = re.compile(r'url[ |]*\=([ |]*([\w|\.\?|\=|\+| |\"|\'|\&]*))')
    OPEN_REGEX = re.compile(r'window\.open\(([ |]*([\w|\.\?|\=|\+| |\"|\'|\&]*))')

    def __init__(self, function, code):
        self.code = code
        self.function = function

    def get_url(self):
        return self.get_href_url() or self.get_windows_open_url()

    @property
    def parameters(self):
        return self._build_parameters(self.function['parameters'])

    def _build_parameters(self, parameters):
        try:
            groups = self.FUNCTION_REGEX.search(self.code).groups()[1]
            parameters_names = [parameter.strip() for parameter in groups.split(",")]
            return dict(zip(parameters_names, parameters))
        except (AttributeError, IndexError):
            return dict()

    def get_url_with_parameters(self):
        url = self.get_url()
        for name, value in self.parameters.items():
            regex = "\+[ |]*({})".format(name)
            url = re.sub(regex, str(value), url)
        return re.sub(r"\'|\"|\+| ", "", url)

    def _get_url_inside_function(self, regex):
        try:
            match = regex.search(self.code, re.MULTILINE)
            url = match.groups()[0]
            if url == "url":
                return self._get_url_by_variable()
            return url
        except (IndexError, AttributeError):
            return

    def get_href_url(self):
        return self._get_url_inside_function(self.HREF_REGEX)

    def get_windows_open_url(self):
        return self._get_url_inside_function(self.OPEN_REGEX)

    def _get_url_by_variable(self):
        try:
            match = self.URL_REGEX.search(self.code, re.MULTILINE)
            return match.groups()[0].strip()
        except (IndexError, AttributeError):
            return
