"""
Basic usage example for HaiBlock Python SDK
"""

import os
from haiblock import HaiBlockClient

def main():
    # Initialize client with your auth token
    client = HaiBlockClient(
        api_url="https://mvp.sandbox.haiblock.com/api",  # Replace with actual API URL
        auth_token=os.getenv("HAIBLOCK_AUTH_TOKEN")  # Set this environment variable
    )
    
    try:
        # Upload a file
        print("Uploading file...")
        content = client.upload_file("sample-company-info.txt", metadata={
            "description": "Company information for AI optimization",
            "category": "company-data"
        })
        print(f"✅ File uploaded successfully! Content ID: {content.id}")
        
        # Transform content for AI consumption
        print("\nTransforming content...")
        transformation = client.transform_content(content.id)
        if transformation.success:
            print("✅ Content transformed successfully!")
            print(f"Chunks created: {len(transformation.chunks or [])}")
        else:
            print(f"❌ Transformation failed: {transformation.error}")
        
        # Submit to Amazon Bedrock
        print("\nSubmitting to Amazon Bedrock...")
        submission = client.submit_to_bedrock(content.id)
        print(f"✅ Submitted to Bedrock! Submission ID: {submission.id}")
        print(f"Status: {submission.status}")
        
        # Get analytics
        print("\nFetching analytics...")
        analytics = client.get_analytics()
        print(f"📊 Analytics Summary:")
        print(f"  Total Content: {analytics.total_content}")
        print(f"  Total Submissions: {analytics.total_submissions}")
        print(f"  Success Rate: {analytics.success_rate:.1%}")
        print(f"  Total Costs: ${analytics.total_costs:.2f}")
        
        # List all content
        print("\nListing all content...")
        content_list = client.list_content(limit=10)
        print(f"📋 Found {len(content_list)} content items:")
        for item in content_list:
            print(f"  - {item.filename} (Status: {item.status})")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()