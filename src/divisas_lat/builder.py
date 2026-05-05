from typing import Optional, TYPE_CHECKING
from .enums import Country, Currency
from .models import TodayRatesResponse, ConversionResponse, HistoricalRateResponse, StatsResponse, ForecastResponse, PercentileResponse

if TYPE_CHECKING:
    from .client import DivisasClient

class QueryBuilder:
    def __init__(self, client: 'DivisasClient'):
        self._client = client
        self._country: Optional[Country] = None
        self._currency: Optional[Currency] = None

    def for_country(self, country: Country) -> 'QueryBuilder':
        self._country = country
        return self

    def with_currency(self, currency: Currency) -> 'QueryBuilder':
        self._currency = currency
        return self

    def _get_country_code(self) -> str:
        if not self._country:
            raise ValueError("Country is required. Call for_country() first.")
        return self._country.value

    def get_today(self) -> TodayRatesResponse:
        endpoint = f"/{self._get_country_code()}/rates"
        if self._currency:
            endpoint += f"/{self._currency.value}"
            
        return self._client._request(endpoint, None, TodayRatesResponse)

    def convert(self, target_currency: Currency, amount: float) -> ConversionResponse:
        endpoint = f"/{self._get_country_code()}/rates/convert"
        params = {
            "to": target_currency.value,
            "amount": str(amount)
        }
        if self._currency:
            params["from"] = self._currency.value
            
        return self._client._request(endpoint, params, ConversionResponse)

    def get_history(self, start_date: str = "", end_date: str = "") -> HistoricalRateResponse:
        if not self._currency:
            raise ValueError("Currency is required for historical data. Call with_currency() first.")
            
        endpoint = f"/{self._get_country_code()}/rates/history"
        params = {"currency": self._currency.value}
        if start_date:
            params["from"] = start_date
        if end_date:
            params["to"] = end_date
            
        return self._client._request(endpoint, params, HistoricalRateResponse)

    def get_stats(self, period: str = "30d") -> StatsResponse:
        endpoint = f"/{self._get_country_code()}/rates/stats"
        params = {"period": period}
        if self._currency:
            params["currency"] = self._currency.value
            
        return self._client._request(endpoint, params, StatsResponse)

    def get_forecast(self, days: int = 7) -> ForecastResponse:
        endpoint = f"/{self._get_country_code()}/rates/forecast"
        params = {"days": str(days)}
        if self._currency:
            params["currency"] = self._currency.value
            
        return self._client._request(endpoint, params, ForecastResponse)

    def get_percentile(self, period: str = "1y") -> PercentileResponse:
        endpoint = f"/{self._get_country_code()}/rates/percentile"
        params = {"period": period}
        if self._currency:
            params["currency"] = self._currency.value
            
        return self._client._request(endpoint, params, PercentileResponse)
