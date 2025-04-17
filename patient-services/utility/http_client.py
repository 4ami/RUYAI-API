import httpx
from enum import Enum
from typing import Optional, Dict, Any


class HttpMethods(str, Enum):
    GET='GET'
    POST='POST'
    PUT='PUT'
    DELETE='DELETE'

class HTTPClient:
    def __init__(self, base_url:str):
        self.base_url:str=base_url
        self.client:httpx.AsyncClient=httpx.AsyncClient(base_url=self.base_url)
    
    async def request(
        self,
        method:str,
        endpoint:str,
        params: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> httpx.Response:
        response:httpx.Response=await self.client.request(
            method=method,
            url=endpoint,
            params=params,
            json=body,
            headers=headers
        )
        # response.raise_for_status()
        return response