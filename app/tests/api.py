from currency.models import Source

from rest_framework.test import APIClient


URL = '/currency/contactUs/create'


def test_get_rates(client):

    """
        Unit test for testing getting rates from API
    """

    client = APIClient()
    url = '/api/rates/'
    response = client.get(url)
    assert response.status_code == 200
    assert response.json()


def test_post_invalid(client):

    """
        Unit test for testing form validation in API that posts invalid form
    """

    client = APIClient()
    url = '/api/rates/'
    response = client.get(url, json={})
    assert response.status_code == 200
    assert response.json()
    # TODO Почему такой респонс?
    assert response.json() == {'count': 0, 'next': None, 'previous': None, 'results': []}


def test_post_valid():

    """
        Unit test for testing form validation in API that posts valid form
    """

    client = APIClient()
    source = Source.objects.last()
    url = '/api/rates/'
    json_data = {
        'ask': 21,
        'bid': 22,
        'source': source.pk,
    }
    response = client.post(url, data=json_data)
    assert response.status_code == 201
    assert response.json()['ask'] == '21.00'
    assert response.json()['bid'] == '22.00'
