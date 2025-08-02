"""
Data models for HaiBlock SDK
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel


class Content(BaseModel):
    """Content model representing uploaded content"""
    id: str
    user_id: str
    filename: str
    original_text: str
    transformed_text: Optional[str] = None
    upload_date: str
    last_updated: str
    status: str  # 'uploaded' | 'processing' | 'transformed' | 'submitted' | 'error'
    file_size: int
    file_type: str
    s3_key: str
    upload_metadata: Optional[Dict[str, Any]] = None
    validation_checks: Optional[Dict[str, bool]] = None
    upload_completed: Optional[str] = None
    actual_file_size: Optional[int] = None


class Submission(BaseModel):
    """Submission model for AI provider submissions"""
    id: str
    content_id: str
    provider: str  # 'bedrock'
    status: str  # 'pending' | 'submitted' | 'success' | 'error'
    submitted_at: str
    response_data: Optional[Dict[str, Any]] = None
    cost_estimate: Optional[float] = None
    error_message: Optional[str] = None


class TransformationResult(BaseModel):
    """Result of content transformation"""
    success: bool
    transformed_text: Optional[str] = None
    chunks: Optional[List[str]] = None
    company_info: Optional[Dict[str, Any]] = None
    faqs: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None


class AnalyticsData(BaseModel):
    """Analytics data model"""
    total_content: int
    total_submissions: int
    successful_submissions: int
    failed_submissions: int
    total_costs: float
    recent_activity: List[Dict[str, Any]]
    content_status_breakdown: Dict[str, int]
    submission_provider_breakdown: Dict[str, int]
    monthly_trends: Dict[str, Any]
    average_cost_per_submission: float
    success_rate: float


class User(BaseModel):
    """User model"""
    id: str
    email: str
    api_keys: Optional[Dict[str, str]] = None
    created_at: str
    last_login: str