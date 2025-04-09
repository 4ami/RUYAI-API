from utility import HTTPClient, HttpMethods
from typing import Optional, Any, Dict
from views import BaseRequest

class BaseService:
    def __init__(self, service:str):
        self.client:HTTPClient = HTTPClient(base_url=service)

    async def post(self, endpoint:str, data:BaseRequest, headers:Optional[Dict[str, str]]=None): 
        return await self.client.request(
            method=HttpMethods.POST.value, 
            endpoint=endpoint,
            body=data.model_dump(),
            headers=headers
        )
    
    async def get(self, endpoint:str, params:Optional[Dict[str, Any]]=None, headers:Optional[Dict[str, str]]=None):
        return await self.client.request(
            method=HttpMethods.GET.value, 
            endpoint=endpoint,
            params=params,
            headers=headers
        )

    async def put(self, endpoint:str, data:BaseRequest, headers:Optional[Dict[str, str]]=None):
        return await self.client.request(
            method=HttpMethods.PUT.value, 
            endpoint=endpoint,
            body=data.model_dump_json(exclude=None),
            headers=headers
        )

    async def delete(self, endpoint:str, data:BaseRequest, headers:Optional[Dict[str, str]]=None):
        return await self.client.request(
            method=HttpMethods.DELETE.value, 
            endpoint=endpoint,
            body=data.model_dump_json(),
            headers=headers
        )
    