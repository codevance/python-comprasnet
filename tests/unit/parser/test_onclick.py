import os
import pytest
import re

from comprasnet.parser.onclick import OnClickFunctionJS

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture
def onclick_function():
    path = os.path.join(ROOT_PATH, '../assets/js_function.html')
    function = {"name": "Declaracoes", "parameters": [123]}
    return OnClickFunctionJS(function, open(path).read())


def test_get_url(onclick_function):
    result = onclick_function.get_url()
    expected = '"Here?parameter=" + coduasg'
    assert result == expected


def test_parameters(onclick_function):
    expected = {"coduasg": 123}
    assert onclick_function.parameters == expected


def test_build_parameters(onclick_function):
    parameters = onclick_function._build_parameters([1])
    assert len(parameters) == 1
    assert parameters['coduasg'] == 1


def test_execpt_build_parameters(onclick_function):
    onclick_function.code = ""
    parameters = onclick_function._build_parameters([1])
    assert parameters == {}


def test_execpt__get_url_by_variable(onclick_function):
    onclick_function.code = ""
    result = onclick_function._get_url_by_variable()
    assert result is None


def test_execpt_get_url_inside_function(onclick_function):
    onclick_function.code = ""
    regex = re.compile("\w*")
    result = onclick_function._get_url_inside_function(regex)
    assert result is None


def test_get_url_with_parameters(onclick_function):
    url = onclick_function.get_url_with_parameters()
    expected = 'Here?parameter=123'
    assert url == expected


def test_get_href_url(onclick_function):
    new_function = 'function teste() { if(true){document.location.href = "Here?parameter=";}}'
    onclick_function.code = new_function
    result = onclick_function.get_href_url()
    expected = '"Here?parameter="'
    assert result == expected


def test_get_href_url_var(onclick_function):
    new_function = 'function teste_url() { url = "Here?parameter="; document.location.href = url}'
    onclick_function.code = new_function
    onclick_function.function['name'] = "teste_url"
    result = onclick_function.get_href_url()
    expected = '"Here?parameter="'
    assert result == expected


def test_get_windows_open_url_var(onclick_function):
    result = onclick_function.get_windows_open_url()
    expected = '"Here?parameter=" + coduasg'
    assert result == expected


def test_get_windows_open_url(onclick_function):
    new_function = 'function teste_open_url() { url = "here"; window.open(url, null)}'
    onclick_function.code = new_function
    onclick_function.function['name'] = "teste_open"
    result = onclick_function.get_windows_open_url()
    expected = '"here"'
    assert result == expected
