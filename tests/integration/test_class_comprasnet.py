from comprasnet import ComprasNet
from datetime import date
from json_tricks import load, dump
import os


def test_search_auctions_by_date():
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            '../assets/result_test_search_auctions_by_date.json')

    with open(filename) as handle:
        local_results = load(handle)

    comprasnet = ComprasNet()
    results = comprasnet.search_auctions_by_date(date(year=2018, month=5, day=11))
    assert results == local_results

