"""
Tests for HaiBlock client
"""

import pytest
import requests_mock
from haiblock import HaiBlockClient, AuthenticationError, APIError
from haiblock.models import Content, Submission, AnalyticsData


class TestHaiBlockClient:
    """Test cases for HaiBlockClient"""
    
    def setup_method(self):
        """Setup test client"""
        self.client = HaiBlockClient(
            api_url="https://api.test.haiblock.com",
            auth_token="test-token"
        )
    
    def test_init_without_token_raises_error(self):
        """Test that client raises error without auth token"""
        with pytest.raises(AuthenticationError):
            HaiBlockClient(api_url="https://api.test.com")
    
    @requests_mock.Mocker()
    def test_get_analytics_success(self, m):
        """Test successful analytics retrieval"""
        mock_response = {
            "total_content": 5,
            "total_submissions": 10,
            "successful_submissions": 8,
            "failed_submissions": 2,
            "total_costs": 1.25,
            "recent_activity": [],
            "content_status_breakdown": {"uploaded": 3, "processed": 2},
            "submission_provider_breakdown": {"bedrock": 10},
            "monthly_trends": {},
            "average_cost_per_submission": 0.125,
            "success_rate": 0.8
        }
        
        m.get("https://api.test.haiblock.com/analytics", json=mock_response)
        
        analytics = self.client.get_analytics()
        
        assert isinstance(analytics, AnalyticsData)
        assert analytics.total_content == 5
        assert analytics.success_rate == 0.8
    
    @requests_mock.Mocker()
    def test_get_content_success(self, m):
        """Test successful content retrieval"""
        content_id = "test-content-id"
        mock_response = {
            "id": content_id,
            "user_id": "user-123",
            "filename": "test.txt",
            "original_text": "test content",
            "upload_date": "2025-01-01T00:00:00Z",
            "last_updated": "2025-01-01T00:00:00Z",
            "status": "uploaded",
            "file_size": 1000,
            "file_type": "text/plain",
            "s3_key": "uploads/test.txt"
        }
        
        m.get(f"https://api.test.haiblock.com/content/{content_id}", json=mock_response)
        
        content = self.client.get_content(content_id)
        
        assert isinstance(content, Content)
        assert content.id == content_id
        assert content.filename == "test.txt"
    
    @requests_mock.Mocker()
    def test_list_content_success(self, m):
        """Test successful content listing"""
        mock_response = {
            "items": [
                {
                    "id": "content-1",
                    "user_id": "user-123",
                    "filename": "test1.txt",
                    "original_text": "content 1",
                    "upload_date": "2025-01-01T00:00:00Z",
                    "last_updated": "2025-01-01T00:00:00Z",
                    "status": "uploaded",
                    "file_size": 1000,
                    "file_type": "text/plain",
                    "s3_key": "uploads/test1.txt"
                },
                {
                    "id": "content-2",
                    "user_id": "user-123",
                    "filename": "test2.txt", 
                    "original_text": "content 2",
                    "upload_date": "2025-01-01T00:00:00Z",
                    "last_updated": "2025-01-01T00:00:00Z",
                    "status": "processed",
                    "file_size": 2000,
                    "file_type": "text/plain",
                    "s3_key": "uploads/test2.txt"
                }
            ]
        }
        
        m.get("https://api.test.haiblock.com/content", json=mock_response)
        
        content_list = self.client.list_content()
        
        assert len(content_list) == 2
        assert all(isinstance(item, Content) for item in content_list)
        assert content_list[0].filename == "test1.txt"
        assert content_list[1].status == "processed"
    
    @requests_mock.Mocker()
    def test_api_error_handling(self, m):
        """Test API error handling"""
        m.get("https://api.test.haiblock.com/analytics", status_code=500, text="Internal Server Error")
        
        with pytest.raises(APIError) as exc_info:
            self.client.get_analytics()
        
        assert exc_info.value.status_code == 500
    
    @requests_mock.Mocker()
    def test_authentication_error_handling(self, m):
        """Test authentication error handling"""
        m.get("https://api.test.haiblock.com/analytics", status_code=401, text="Unauthorized")
        
        with pytest.raises(AuthenticationError):
            self.client.get_analytics()
    
    @requests_mock.Mocker()
    def test_submit_to_bedrock_success(self, m):
        """Test successful Bedrock submission"""
        content_id = "test-content-id"
        mock_response = {
            "id": "submission-123",
            "content_id": content_id,
            "provider": "bedrock",
            "status": "pending",
            "submitted_at": "2025-01-01T00:00:00Z"
        }
        
        m.post(f"https://api.test.haiblock.com/content/{content_id}/submit/bedrock", json=mock_response)
        
        submission = self.client.submit_to_bedrock(content_id)
        
        assert isinstance(submission, Submission)
        assert submission.provider == "bedrock"
        assert submission.status == "pending"