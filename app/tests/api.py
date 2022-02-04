from currency.models import Source

from rest_framework.test import APIClient


URL = '/currency/contactUs/create'


#  Read
def test_get_rates(api_client_auth):

    url = '/api/rates/'
    response = api_client_auth.get(url)
    assert response.status_code == 200
    assert response.json()


#  Create
def test_post_invalid(api_client_auth):
    client = APIClient()

    url = '/api/rates/'
    response = api_client_auth.post(url, json={})

    assert response.status_code == 400
    response = client.get(url, json={})
    assert response.status_code == 200
    assert response.json()
    assert response.json() == {
        "ask": ["This field is required."],
        "bid": ["This field is required."],
        "source": ["This field is required."]
        }


def test_post_valid(api_client_auth):
    client = APIClient()
    source = Source.objects.last()
    url = '/api/rates/'
    json_data = {
        'ask': 21,
        'bid': 22,
        'source': source.pk,
    }
    response = api_client_auth.post(url, data=json_data)
    assert response.status_code == 201
    assert response.json()['ask'] == '21.00'
    assert response.json()['bid'] == '22.00'


#  Update
def test_update_valid(api_client_auth):

    url = '/api/rates/'
    json_data = {}
    response = api_client_auth.update(url, data=json_data)
    assert response.status_code == 405


#  Update
def test_delete_valid(api_client_auth):

    url = '/api/rates/'
    json_data = {}
    response = api_client_auth.delete(url, data=json_data)
    assert response.status_code == 405
