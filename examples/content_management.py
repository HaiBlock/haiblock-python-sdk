"""
Content management example for HaiBlock Python SDK
"""

import os
import time
from haiblock import HaiBlockClient, ContentNotFoundError

def main():
    # Initialize client
    client = HaiBlockClient(
        api_url="https://mvp.sandbox.haiblock.com/api",
        auth_token=os.getenv("HAIBLOCK_AUTH_TOKEN")
    )
    
    print("🚀 HaiBlock Content Management Demo")
    print("=" * 50)
    
    try:
        # 1. Upload multiple files
        files_to_upload = [
            "company-overview.txt",
            "product-catalog.pdf",
            "faq-document.md"
        ]
        
        uploaded_content = []
        
        for filename in files_to_upload:
            print(f"\n📤 Uploading {filename}...")
            try:
                # Create a sample file if it doesn't exist
                if not os.path.exists(filename):
                    with open(filename, 'w') as f:
                        f.write(f"Sample content for {filename}\n\nThis is demo content for HaiBlock optimization.")
                
                content = client.upload_file(filename, metadata={
                    "source": "content_management_demo",
                    "category": "company-info"
                })
                uploaded_content.append(content)
                print(f"✅ {filename} uploaded - ID: {content.id}")
                
            except Exception as e:
                print(f"❌ Failed to upload {filename}: {e}")
        
        # 2. Check upload status
        print(f"\n📋 Checking status of {len(uploaded_content)} uploaded files...")
        for content in uploaded_content:
            updated_content = client.get_content(content.id)
            print(f"  📄 {updated_content.filename}: {updated_content.status}")
        
        # 3. Transform content
        print(f"\n🔄 Transforming content...")
        for content in uploaded_content:
            print(f"  Processing {content.filename}...")
            try:
                result = client.transform_content(content.id)
                if result.success:
                    print(f"    ✅ Transformed successfully")
                    if result.chunks:
                        print(f"    📦 Created {len(result.chunks)} chunks")
                else:
                    print(f"    ❌ Transformation failed: {result.error}")
            except Exception as e:
                print(f"    ❌ Error: {e}")
        
        # 4. Submit to AI providers
        print(f"\n🚀 Submitting to AI providers...")
        submissions = []
        for content in uploaded_content:
            try:
                submission = client.submit_to_model(content.id, "bedrock")
                submissions.append(submission)
                print(f"  ✅ {content.filename} submitted to Bedrock - ID: {submission.id}")
            except Exception as e:
                print(f"  ❌ Failed to submit {content.filename}: {e}")
        
        # 5. Monitor submissions
        print(f"\n👀 Monitoring submission status...")
        time.sleep(2)  # Wait a bit for processing
        
        for submission in submissions:
            try:
                updated_submission = client.get_submission(submission.id)
                print(f"  📊 Submission {submission.id}: {updated_submission.status}")
                if updated_submission.cost_estimate:
                    print(f"      💰 Estimated cost: ${updated_submission.cost_estimate:.4f}")
            except Exception as e:
                print(f"  ❌ Error checking submission {submission.id}: {e}")
        
        # 6. Get comprehensive analytics
        print(f"\n📈 Analytics Summary")
        print("-" * 30)
        analytics = client.get_analytics()
        
        print(f"📊 Total Content Items: {analytics.total_content}")
        print(f"🚀 Total Submissions: {analytics.total_submissions}")
        print(f"✅ Successful: {analytics.successful_submissions}")
        print(f"❌ Failed: {analytics.failed_submissions}")
        print(f"📈 Success Rate: {analytics.success_rate:.1%}")
        print(f"💰 Total Costs: ${analytics.total_costs:.4f}")
        print(f"💵 Avg Cost/Submission: ${analytics.average_cost_per_submission:.4f}")
        
        # 7. Show recent activity
        if analytics.recent_activity:
            print(f"\n📅 Recent Activity:")
            for activity in analytics.recent_activity[:5]:  # Show last 5 activities
                print(f"  • {activity.get('timestamp', 'N/A')}: {activity.get('action', 'Unknown action')}")
        
        # 8. Content status breakdown
        print(f"\n📋 Content Status Breakdown:")
        for status, count in analytics.content_status_breakdown.items():
            print(f"  {status}: {count}")
        
        # 9. Clean up (optional)
        cleanup = input("\n🗑️  Delete uploaded demo files? (y/N): ").lower().strip()
        if cleanup == 'y':
            print("🗑️  Cleaning up...")
            for content in uploaded_content:
                try:
                    client.delete_content(content.id)
                    print(f"  ✅ Deleted {content.filename}")
                    # Also delete local file
                    if os.path.exists(content.filename):
                        os.remove(content.filename)
                except Exception as e:
                    print(f"  ❌ Failed to delete {content.filename}: {e}")
        
        print(f"\n✨ Demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")

if __name__ == "__main__":
    main()