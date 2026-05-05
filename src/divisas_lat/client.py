import os
from typing import Dict, Optional, Type, TypeVar
import httpx
from pydantic import BaseModel

from .cache import MemoryCache
from .exceptions import DivisasException
from .models import ErrorResponse
from .builder import QueryBuilder

T = TypeVar('T', bound=BaseModel)

class DivisasClient:
    """Core client for interacting with the Divisas.lat API."""
    
    def __init__(
        self, 
        api_key: Optional[str] = None, 
        base_url: str = "https://api.divisas.lat/v1",
        cache_ttl_seconds: int = 3600,
        timeout_seconds: float = 10.0
    ):
        self.api_key = api_key or os.environ.get("DIVISAS_API_KEY")
        self.base_url = base_url.rstrip("/")
        self.cache = MemoryCache(default_ttl_seconds=cache_ttl_seconds)
        self.timeout = timeout_seconds
        
        headers = {
            "Accept": "application/json",
            "User-Agent": "DivisasLat-PythonSDK/1.0"
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
            
        self._http = httpx.Client(
            base_url=self.base_url,
            headers=headers,
            timeout=self.timeout
        )

    def query(self) -> QueryBuilder:
        """Starts a fluent query builder sequence."""
        return QueryBuilder(self)

    def get_countries(self) -> list['CountryResponse']:
        from .models import CountryResponse
        data = self._request("/countries", None, list)
        return [CountryResponse.model_validate(item) for item in data]

    def get_currencies(self, country: 'Country') -> list[str]:
        data = self._request(f"/{country.value}/currencies", None, list)
        return list(data)

    def _request(self, endpoint: str, query_params: Optional[Dict[str, str]], response_model: Type[T] | type) -> T | list:
        """Internal synchronous request dispatcher."""
        url = endpoint if endpoint.startswith("/") else f"/{endpoint}"
        
        # Build cache key based on URL and sorted query params
        cache_key = url
        if query_params:
            query_string = "&".join(f"{k}={v}" for k, v in sorted(query_params.items()))
            cache_key = f"{url}?{query_string}"
            
        cached_data = self.cache.get(cache_key)
        if cached_data:
            return response_model.model_validate(cached_data)

        try:
            response = self._http.get(url, params=query_params)
            response.raise_for_status()
            
            data = response.json()
            self.cache.set(cache_key, data)
            return response_model.model_validate(data)
            
        except httpx.HTTPStatusError as e:
            # Try to parse the standard error response
            try:
                error_data = e.response.json()
                err = ErrorResponse.model_validate(error_data)
                raise DivisasException(f"API Error: {e.response.status_code} - {err.error}", status_code=e.response.status_code)
            except Exception:
                raise DivisasException(f"API Error: {e.response.status_code} - {e.response.text}", status_code=e.response.status_code)
        except Exception as e:
            raise DivisasException(f"Request failed: {str(e)}")
            
    def close(self):
        """Closes the underlying HTTP connection pool."""
        self._http.close()

    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
