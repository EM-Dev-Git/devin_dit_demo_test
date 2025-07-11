import os
from typing import List, Dict, Any, Optional
from azure.identity import ClientSecretCredential
from msgraph_core import GraphRequestAdapter
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.request_information import RequestInformation
from kiota_abstractions.serialization import Parsable
import httpx
import json
from modules.logger import get_logger
from dotenv import load_dotenv

load_dotenv()

logger = get_logger(__name__)

class MicrosoftGraphClient:
    def __init__(self):
        self.tenant_id = os.getenv("MICROSOFT_TENANT_ID")
        self.client_id = os.getenv("MICROSOFT_CLIENT_ID") 
        self.client_secret = os.getenv("MICROSOFT_CLIENT_SECRET")
        self.graph_endpoint = "https://graph.microsoft.com/v1.0"
        
        if not all([self.tenant_id, self.client_id, self.client_secret]):
            logger.warning("Microsoft Graph credentials not configured")
            self._client = None
        else:
            self._initialize_client()
    
    def _initialize_client(self):
        try:
            credential = ClientSecretCredential(
                tenant_id=self.tenant_id,
                client_id=self.client_id,
                client_secret=self.client_secret
            )
            
            self._credential = credential
            logger.info("Microsoft Graph client initialized successfully")
            
        except Exception as e:
            logger.error("Failed to initialize Microsoft Graph client", extra={"error": str(e)})
            self._client = None
    
    async def get_access_token(self) -> Optional[str]:
        if not self._credential:
            return None
            
        try:
            token = self._credential.get_token("https://graph.microsoft.com/.default")
            return token.token
        except Exception as e:
            logger.error("Failed to get access token", extra={"error": str(e)})
            return None
    
    async def get_online_meetings(self, user_id: str = "me") -> List[Dict[str, Any]]:
        access_token = await self.get_access_token()
        if not access_token:
            raise Exception("Unable to authenticate with Microsoft Graph")
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        url = f"{self.graph_endpoint}/users/{user_id}/onlineMeetings"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                
                data = response.json()
                meetings = data.get("value", [])
                
                logger.info("Retrieved online meetings", extra={
                    "user_id": user_id,
                    "meeting_count": len(meetings)
                })
                
                return meetings
                
        except Exception as e:
            logger.error("Failed to retrieve online meetings", extra={
                "user_id": user_id,
                "error": str(e)
            })
            raise
    
    async def get_meeting_transcripts(self, meeting_id: str) -> List[Dict[str, Any]]:
        access_token = await self.get_access_token()
        if not access_token:
            raise Exception("Unable to authenticate with Microsoft Graph")
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        url = f"{self.graph_endpoint}/communications/onlineMeetings/{meeting_id}/transcripts"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                
                data = response.json()
                transcripts = data.get("value", [])
                
                logger.info("Retrieved meeting transcripts", extra={
                    "meeting_id": meeting_id,
                    "transcript_count": len(transcripts)
                })
                
                return transcripts
                
        except Exception as e:
            logger.error("Failed to retrieve meeting transcripts", extra={
                "meeting_id": meeting_id,
                "error": str(e)
            })
            raise
    
    async def get_transcript_content(self, meeting_id: str, transcript_id: str) -> str:
        access_token = await self.get_access_token()
        if not access_token:
            raise Exception("Unable to authenticate with Microsoft Graph")
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        url = f"{self.graph_endpoint}/communications/onlineMeetings/{meeting_id}/transcripts/{transcript_id}/content"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                
                content = response.text
                
                logger.info("Retrieved transcript content", extra={
                    "meeting_id": meeting_id,
                    "transcript_id": transcript_id,
                    "content_length": len(content)
                })
                
                return content
                
        except Exception as e:
            logger.error("Failed to retrieve transcript content", extra={
                "meeting_id": meeting_id,
                "transcript_id": transcript_id,
                "error": str(e)
            })
            raise
    
    async def search_meetings_by_date_range(self, start_date: str, end_date: str, user_id: str = "me") -> List[Dict[str, Any]]:
        meetings = await self.get_online_meetings(user_id)
        
        filtered_meetings = []
        for meeting in meetings:
            meeting_start = meeting.get("startDateTime")
            if meeting_start and start_date <= meeting_start <= end_date:
                filtered_meetings.append(meeting)
        
        logger.info("Filtered meetings by date range", extra={
            "user_id": user_id,
            "start_date": start_date,
            "end_date": end_date,
            "filtered_count": len(filtered_meetings)
        })
        
        return filtered_meetings

graph_client = MicrosoftGraphClient()
