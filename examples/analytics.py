"""
Analytics dashboard example for HaiBlock Python SDK
"""

import os
from datetime import datetime
from haiblock import HaiBlockClient

def format_currency(amount):
    """Format currency for display"""
    return f"${amount:.4f}"

def format_percentage(value):
    """Format percentage for display"""
    return f"{value:.1%}"

def print_section_header(title):
    """Print a formatted section header"""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")

def print_subsection(title):
    """Print a formatted subsection header"""
    print(f"\n{'-' * 40}")
    print(f"  {title}")
    print(f"{'-' * 40}")

def main():
    # Initialize client
    client = HaiBlockClient(
        api_url="https://mvp.sandbox.haiblock.com/api",
        auth_token=os.getenv("HAIBLOCK_AUTH_TOKEN")
    )
    
    print("📊 HaiBlock Analytics Dashboard")
    print_section_header("ANALYTICS OVERVIEW")
    
    try:
        # Get analytics data
        analytics = client.get_analytics()
        
        # Overview metrics
        print_subsection("Key Metrics")
        print(f"📄 Total Content Items:     {analytics.total_content:,}")
        print(f"🚀 Total Submissions:       {analytics.total_submissions:,}")
        print(f"✅ Successful Submissions:  {analytics.successful_submissions:,}")
        print(f"❌ Failed Submissions:      {analytics.failed_submissions:,}")
        print(f"📈 Success Rate:            {format_percentage(analytics.success_rate)}")
        
        # Cost metrics
        print_subsection("Cost Analysis")
        print(f"💰 Total Costs:             {format_currency(analytics.total_costs)}")
        print(f"💵 Average Cost/Submission: {format_currency(analytics.average_cost_per_submission)}")
        
        # Efficiency metrics
        if analytics.total_submissions > 0:
            cost_per_success = analytics.total_costs / analytics.successful_submissions if analytics.successful_submissions > 0 else 0
            print(f"💎 Cost per Success:        {format_currency(cost_per_success)}")
        
        # Content status breakdown
        print_subsection("Content Status Distribution")
        total_content = sum(analytics.content_status_breakdown.values())
        for status, count in analytics.content_status_breakdown.items():
            percentage = count / total_content if total_content > 0 else 0
            bar_length = int(percentage * 30)  # 30 character bar
            bar = "█" * bar_length + "░" * (30 - bar_length)
            print(f"{status.upper():12} │{bar}│ {count:3} ({format_percentage(percentage)})")
        
        # Provider breakdown
        if analytics.submission_provider_breakdown:
            print_subsection("AI Provider Distribution")
            total_submissions = sum(analytics.submission_provider_breakdown.values())
            for provider, count in analytics.submission_provider_breakdown.items():
                percentage = count / total_submissions if total_submissions > 0 else 0
                bar_length = int(percentage * 30)
                bar = "█" * bar_length + "░" * (30 - bar_length)
                print(f"{provider.upper():12} │{bar}│ {count:3} ({format_percentage(percentage)})")
        
        # Recent activity
        if analytics.recent_activity:
            print_subsection("Recent Activity")
            print("📅 Latest 10 Activities:")
            for i, activity in enumerate(analytics.recent_activity[:10], 1):
                timestamp = activity.get('timestamp', 'N/A')
                action = activity.get('action', 'Unknown action')
                content_id = activity.get('content_id', '')
                status = activity.get('status', '')
                
                # Format timestamp if it's a proper datetime string
                try:
                    if timestamp != 'N/A':
                        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        timestamp = dt.strftime('%Y-%m-%d %H:%M')
                except:
                    pass
                
                status_emoji = {
                    'success': '✅',
                    'error': '❌',
                    'pending': '⏳',
                    'processing': '🔄'
                }.get(status.lower(), '📝')
                
                print(f"{i:2}. {status_emoji} {timestamp} - {action}")
                if content_id:
                    print(f"     Content: {content_id[:8]}...")
        
        # Monthly trends (if available)
        if analytics.monthly_trends:
            print_subsection("Monthly Trends")
            for month, data in analytics.monthly_trends.items():
                submissions = data.get('submissions', 0)
                costs = data.get('costs', 0)
                print(f"{month}: {submissions:3} submissions, {format_currency(costs)} costs")
        
        # Performance insights
        print_section_header("PERFORMANCE INSIGHTS")
        
        # Success rate analysis
        if analytics.success_rate >= 0.9:
            print("🎉 Excellent success rate! Your content optimization is working great.")
        elif analytics.success_rate >= 0.7:
            print("👍 Good success rate. Consider reviewing failed submissions for improvement opportunities.")
        elif analytics.success_rate >= 0.5:
            print("⚠️  Moderate success rate. Review content transformation and submission processes.")
        else:
            print("🚨 Low success rate. Immediate attention needed for content optimization workflow.")
        
        # Cost analysis
        avg_cost = analytics.average_cost_per_submission
        if avg_cost < 0.01:
            print("💰 Very cost-effective processing!")
        elif avg_cost < 0.05:
            print("💰 Cost-effective processing.")
        elif avg_cost < 0.10:
            print("💸 Moderate processing costs. Monitor for optimization opportunities.")
        else:
            print("💸 High processing costs. Consider optimizing content size and transformation logic.")
        
        # Activity level
        if analytics.total_submissions > 100:
            print("🚀 High activity level - platform is being actively used!")
        elif analytics.total_submissions > 20:
            print("📈 Moderate activity level - good engagement.")
        else:
            print("📊 Getting started - consider uploading more content for better insights.")
        
        # Get detailed content list for additional analysis
        print_section_header("CONTENT ANALYSIS")
        
        content_list = client.list_content(limit=50)
        if content_list:
            print_subsection("Content Summary")
            
            # File type analysis
            file_types = {}
            total_size = 0
            status_counts = {}
            
            for content in content_list:
                file_type = content.file_type
                file_types[file_type] = file_types.get(file_type, 0) + 1
                total_size += content.file_size
                status_counts[content.status] = status_counts.get(content.status, 0) + 1
            
            print(f"📁 Total Files: {len(content_list)}")
            print(f"💾 Total Size: {total_size / (1024*1024):.2f} MB")
            
            print("\n📋 File Types:")
            for file_type, count in sorted(file_types.items()):
                print(f"  {file_type}: {count}")
            
            print("\n📊 Content Status:")
            for status, count in sorted(status_counts.items()):
                print(f"  {status}: {count}")
            
            # Recent uploads
            recent_content = sorted(content_list, key=lambda x: x.upload_date, reverse=True)[:5]
            print(f"\n📅 Recent Uploads:")
            for content in recent_content:
                size_mb = content.file_size / (1024*1024)
                print(f"  📄 {content.filename} ({size_mb:.2f}MB) - {content.status}")
        
        print_section_header("DASHBOARD COMPLETE")
        print("✨ Analytics dashboard generated successfully!")
        
    except Exception as e:
        print(f"❌ Failed to generate analytics dashboard: {e}")

if __name__ == "__main__":
    main()