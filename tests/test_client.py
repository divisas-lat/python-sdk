import pytest
import respx
import httpx
from divisas_lat import DivisasClient, Country, Currency, DivisasException

def test_client_init():
    client = DivisasClient(api_key="test-key")
    assert client.api_key == "test-key"
    assert client.base_url == "https://api.divisas.lat/v1"

@respx.mock
def test_get_today():
    mock_response = {
        "country": "GT",
        "base_currency": "GTQ",
        "date": "2026-05-05",
        "source": "Banguat",
        "cached": False,
        "rate": {
            "currency_code": "USD",
            "buy": 7.63,
            "sell": 7.63
        }
    }
    
    respx.get("https://api.divisas.lat/v1/GT/rates").mock(return_value=httpx.Response(200, json=mock_response))
    
    with DivisasClient() as client:
        res = client.query().for_country(Country.GUATEMALA).get_today()
        
        assert res.country == "GT"
        assert res.base_currency == "GTQ"
        assert res.rate.buy == 7.63
        assert res.rate.currency_code == "USD"

@respx.mock
def test_convert():
    mock_response = {
        "from": {"currency": "USD", "amount": 100},
        "to": {"currency": "GTQ", "amount": 763},
        "amount": 100,
        "result": 763,
        "effective_rate": 7.63,
        "via": "Banguat",
        "date": "2026-05-05",
        "note": ""
    }
    
    # Matching the GET with query parameters
    respx.get("https://api.divisas.lat/v1/GT/rates/convert").mock(return_value=httpx.Response(200, json=mock_response))
    
    with DivisasClient() as client:
        res = client.query().for_country(Country.GUATEMALA).with_currency(Currency.USD).convert(Currency.GTQ, 100)
        
        assert res.result == 763
        assert res.effective_rate == 7.63
        assert res.from_.currency == "USD"

@respx.mock
def test_api_error():
    mock_response = {"error": "API key required", "docs": "https://divisas.lat"}
    respx.get("https://api.divisas.lat/v1/GT/rates").mock(return_value=httpx.Response(401, json=mock_response))
    
    with DivisasClient() as client:
        with pytest.raises(DivisasException) as excinfo:
            client.query().for_country(Country.GUATEMALA).get_today()
            
        assert excinfo.value.status_code == 401
        assert "API key required" in str(excinfo.value)
