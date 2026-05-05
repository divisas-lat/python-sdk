from typing import Dict, Optional
from pydantic import BaseModel, Field


class RateData(BaseModel):
    currency_code: str
    buy: float
    sell: float


class TodayRatesResponse(BaseModel):
    country: str
    base_currency: str
    date: str
    source: str
    cached: bool
    rate: RateData
    rates: Optional[Dict[str, RateData]] = None


class CurrencyAmount(BaseModel):
    currency: str
    amount: float


class ConversionResponse(BaseModel):
    from_: CurrencyAmount = Field(alias="from")
    to: CurrencyAmount
    amount: float
    result: float
    effective_rate: float
    via: str
    date: str
    note: str


class HistoricalRateResponse(BaseModel):
    country: str
    base_currency: str
    currency: str
    from_: str = Field(alias="from")
    to: str
    data: Dict[str, RateData]


class StatsResponse(BaseModel):
    country: str
    base_currency: str
    currency: str
    period: str
    min: RateData
    max: RateData
    avg: RateData


class ForecastResponse(BaseModel):
    country: str
    base_currency: str
    currency: str
    forecast: Dict[str, RateData]


class PercentileResponse(BaseModel):
    country: str
    base_currency: str
    currency: str
    period: str
    percentile: float


class ErrorResponse(BaseModel):
    error: str
    docs: str
