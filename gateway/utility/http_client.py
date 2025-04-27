import httpx
from enum import Enum
from typing import Optional, Dict, Any
from fastapi import UploadFile

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
        return response
    
    async def multipart(
        self,
        method:str,
        endpoint:str,
        fields:Dict[str, Any],
        files:list[tuple[str, UploadFile]],
        headers: Optional[Dict[str, str]] = None
    )-> httpx.Response:
        prep_files: list[tuple[str, tuple[str, bytes, str]]]=[]

        for field_name, upload_file in files:
            content=await upload_file.read()
            prep_files.append(
                (field_name,
                (upload_file.filename, content, upload_file.content_type))
            )
        
        return await self.client.request(
            method=method,
            url=endpoint,
            data=fields,
            files=prep_files,
            headers=headers,
            timeout=httpx.Timeout(60)
        )