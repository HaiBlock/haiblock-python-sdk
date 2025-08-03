"""
HaiBlock API Client
"""

import os
import requests
from typing import Optional, Dict, Any, List
from .models import Content, Submission, AnalyticsData, TransformationResult
from .exceptions import HaiBlockError, AuthenticationError, APIError, ContentNotFoundError


class HaiBlockClient:
    """
    Main client for interacting with the HaiBlock API
    """
    
    def __init__(self, api_url: str = None, auth_token: str = None):
        """
        Initialize HaiBlock client
        
        Args:
            api_url: Base URL for the HaiBlock API
            auth_token: Authentication token
        """
        self.api_url = api_url or os.getenv("HAIBLOCK_API_URL", "https://api.haiblock.com")
        self.auth_token = auth_token or os.getenv("HAIBLOCK_AUTH_TOKEN")
        
        if not self.auth_token:
            raise AuthenticationError("Auth token is required. Set HAIBLOCK_AUTH_TOKEN environment variable or pass auth_token parameter.")
        
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json",
            "User-Agent": "haiblock-python-sdk/0.1.0"
        })
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request to API"""
        url = f"{self.api_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise AuthenticationError("Invalid or expired authentication token")
            elif e.response.status_code == 404:
                raise ContentNotFoundError("Requested resource not found")
            else:
                raise APIError(f"API request failed: {e}", e.response.status_code, e.response)
        except requests.exceptions.RequestException as e:
            raise APIError(f"Request failed: {e}")
    
    def upload_file(self, file_path: str, metadata: Optional[Dict[str, Any]] = None) -> Content:
        """
        Upload a file for processing
        
        Args:
            file_path: Path to the file to upload
            metadata: Optional metadata for the upload
            
        Returns:
            Content object representing the uploaded content
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        filename = os.path.basename(file_path)
        
        with open(file_path, 'rb') as f:
            files = {'file': (filename, f)}
            data = {'metadata': metadata} if metadata else {}
            
            # Note: For file uploads, we don't use JSON content-type
            headers = {k: v for k, v in self.session.headers.items() if k != "Content-Type"}
            
            response = requests.post(
                f"{self.api_url}/upload",
                files=files,
                data=data,
                headers=headers
            )
            
            if response.status_code != 200:
                raise APIError(f"Upload failed: {response.text}", response.status_code, response)
            
            return Content(**response.json())
    
    def get_content(self, content_id: str) -> Content:
        """
        Get content by ID
        
        Args:
            content_id: ID of the content to retrieve
            
        Returns:
            Content object
        """
        data = self._make_request("GET", f"/content/{content_id}")
        return Content(**data)
    
    def list_content(self, limit: int = 50, offset: int = 0) -> List[Content]:
        """
        List uploaded content
        
        Args:
            limit: Maximum number of items to return
            offset: Number of items to skip
            
        Returns:
            List of Content objects
        """
        params = {"limit": limit, "offset": offset}
        data = self._make_request("GET", "/content", params=params)
        return [Content(**item) for item in data.get("items", [])]
    
    def transform_content(self, content_id: str) -> TransformationResult:
        """
        Transform content for AI consumption
        
        Args:
            content_id: ID of the content to transform
            
        Returns:
            TransformationResult object
        """
        data = self._make_request("POST", f"/content/{content_id}/transform")
        return TransformationResult(**data)
    
    def submit_to_model(self, content_id: str, provider: str = "bedrock") -> Submission:
        """
        Submit content to AI model provider
        
        Args:
            content_id: ID of the content to submit
            provider: AI provider name (default: "bedrock")
            
        Returns:
            Submission object
        """
        data = self._make_request("POST", f"/content/{content_id}/submit/{provider}")
        return Submission(**data)
    
    def get_submission(self, submission_id: str) -> Submission:
        """
        Get submission by ID
        
        Args:
            submission_id: ID of the submission to retrieve
            
        Returns:
            Submission object
        """
        data = self._make_request("GET", f"/submissions/{submission_id}")
        return Submission(**data)
    
    def list_submissions(self, content_id: str = None, limit: int = 50, offset: int = 0) -> List[Submission]:
        """
        List submissions
        
        Args:
            content_id: Optional content ID to filter by
            limit: Maximum number of items to return
            offset: Number of items to skip
            
        Returns:
            List of Submission objects
        """
        params = {"limit": limit, "offset": offset}
        if content_id:
            params["content_id"] = content_id
            
        data = self._make_request("GET", "/submissions", params=params)
        return [Submission(**item) for item in data.get("items", [])]
    
    def get_analytics(self) -> AnalyticsData:
        """
        Get analytics data
        
        Returns:
            AnalyticsData object
        """
        data = self._make_request("GET", "/analytics")
        return AnalyticsData(**data)
    
    def delete_content(self, content_id: str) -> bool:
        """
        Delete content
        
        Args:
            content_id: ID of the content to delete
            
        Returns:
            True if deletion was successful
        """
        self._make_request("DELETE", f"/content/{content_id}")
        return True