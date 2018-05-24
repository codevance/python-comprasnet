from comprasnet.parser.onclick import OnClickFunctionJS
from comprasnet.parser.javascript import JavaScriptParser
import pytest
import os

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture
def javascript_parser():
    path = os.path.join(ROOT_PATH, '../assets/parser_javascript.html')
    return JavaScriptParser(open(path).read())


def test_get_onclick_function_by_id(javascript_parser):
    expected = "localhost"
    assert javascript_parser.get_link_inside_onclick_function_by_id("btnDeclaracoes") == expected


def test_invalid_id_at_get_onclick_function_by_id(javascript_parser):
    assert javascript_parser.get_link_inside_onclick_function_by_id("test") is None


def test_invalid_name_at_get_onclick_function_by_name(javascript_parser):
    assert javascript_parser.get_link_inside_onclick_function_by_name("test") is None


def test_get_onclick_function_by_name(javascript_parser):
    expected = 'Here?parameter=coduasg'
    result = javascript_parser.get_link_inside_onclick_function_by_name("btnResultadoFornecr")
    assert result == expected


def test_get_js_code(javascript_parser):
    path = os.path.join(ROOT_PATH, '../assets/result_script.html')
    with open(path) as html:
        expected = html.read()
    assert javascript_parser._get_js_code() == expected


def test_no_script_code():
    javascript_parser = JavaScriptParser("")
    assert javascript_parser._get_js_code() == []


def test_clean_onlick_function(javascript_parser):
    text = "javascript:resultadoFornecedor(712965);"
    result = javascript_parser._clean_onlick_function(text)
    assert result['name'] == "resultadoFornecedor"
    assert result['parameters'] == ["712965"]


def test_html_without_onlick_function():
    javascript_parser = JavaScriptParser("")
    text = "712965;"
    result = javascript_parser._clean_onlick_function(text)
    assert result['name'] == ""
    assert result['parameters'] == []


def test_clean_onlick_function_multiple_parameters(javascript_parser):
    text = "javascript:resultadoFornecedor(712965, 123, 9);"
    result = javascript_parser._clean_onlick_function(text)
    assert result['name'] == "resultadoFornecedor"
    assert result['parameters'] == ["712965", "123", "9"]


def test_find_js_function(javascript_parser):
    function = {"name": "teste"}
    result = javascript_parser.get_js_function(function)
    assert isinstance(result, OnClickFunctionJS)
