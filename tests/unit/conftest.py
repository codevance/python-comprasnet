from collections import namedtuple
from comprasnet.pages.auction_minutes import AuctionMinutes
from unittest import mock
import pytest
import os


@mock.patch('comprasnet.pages.auction_minutes.requests.get')
@pytest.fixture
def auction_minute(get):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        '../assets/result_minutes_auction.html')
    MockResponse = namedtuple('Response', 'status_code, text')
    MockResponse.status_code = 200
    with open(path) as html:
        MockResponse.text = html.read()
    get.return_value = MockResponse
    return AuctionMinutes(1234, 987)
