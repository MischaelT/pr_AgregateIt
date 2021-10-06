from currency.models import Rate
from currency.tasks import parse_privatbank

from unittest.mock import MagicMock

def test_parse_privatbank(mocker):

    privatbank_response = [
        {"ccy": "USD", "base_ccy": "UAH", "buy": "26.50000", "sale": "26.90000"},
        {"ccy": "EUR", "base_ccy": "UAH", "buy": "30.95000", "sale": "31.55000"},
        {"ccy": "RUR", "base_ccy": "UAH", "buy": "0.35000", "sale": "0.38000"},
        {"ccy": "BTC", "base_ccy": "USD", "buy": "39310.2844", "sale": "43448.2090"},
    ]

    initial_count_rate = Rate.objects.count()
    request_get_mock = mocker.patch('requests.get')
    request_get_mock.return_value =  MagicMock(json=lambda: privatbank_response)

    parse_privatbank()
    assert Rate.objects.count() == initial_count_rate+2

    parse_privatbank()
    assert Rate.objects.count() == initial_count_rate + 2

    privatbank_response = [
        {"ccy": "USD", "base_ccy": "UAH", "buy": "26.60000", "sale": "26.90000"},
    ]
    request_get_mock.return_value = MagicMock(json=lambda: privatbank_response)

    parse_privatbank()
    assert Rate.objects.count() == initial_count_rate + 3


