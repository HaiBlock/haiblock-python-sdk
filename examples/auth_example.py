"""
Authentication example for HaiBlock Python SDK
"""

import os
import boto3
from botocore.exceptions import ClientError
from haiblock import HaiBlockClient, AuthenticationError

class HaiBlockAuth:
    """Helper class for HaiBlock authentication using AWS Cognito"""
    
    def __init__(self, user_pool_id=None, client_id=None, region='us-east-1'):
        self.user_pool_id = user_pool_id or os.getenv('HAIBLOCK_USER_POOL_ID')
        self.client_id = client_id or os.getenv('HAIBLOCK_CLIENT_ID')
        self.region = region
        
        if not self.user_pool_id or not self.client_id:
            raise ValueError("User Pool ID and Client ID are required")
        
        self.cognito_client = boto3.client('cognito-idp', region_name=self.region)
    
    def authenticate(self, email: str, password: str) -> str:
        """
        Authenticate with Cognito and return JWT token
        
        Args:
            email: User email
            password: User password
            
        Returns:
            JWT authentication token
        """
        try:
            response = self.cognito_client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': email,
                    'PASSWORD': password
                }
            )
            
            # Extract access token
            access_token = response['AuthenticationResult']['AccessToken']
            return access_token
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NotAuthorizedException':
                raise AuthenticationError("Invalid email or password")
            elif error_code == 'UserNotConfirmedException':
                raise AuthenticationError("Email not verified. Please check your email and confirm your account.")
            else:
                raise AuthenticationError(f"Authentication failed: {e}")
    
    def signup(self, email: str, password: str, name: str) -> bool:
        """
        Sign up a new user
        
        Args:
            email: User email
            password: User password
            name: User's full name
            
        Returns:
            True if signup successful
        """
        try:
            response = self.cognito_client.sign_up(
                ClientId=self.client_id,
                Username=email,
                Password=password,
                UserAttributes=[
                    {'Name': 'email', 'Value': email},
                    {'Name': 'name', 'Value': name}
                ]
            )
            return True
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'UsernameExistsException':
                raise AuthenticationError("User already exists")
            elif error_code == 'InvalidPasswordException':
                raise AuthenticationError("Password does not meet requirements")
            else:
                raise AuthenticationError(f"Signup failed: {e}")
    
    def confirm_signup(self, email: str, confirmation_code: str) -> bool:
        """
        Confirm user signup with verification code
        
        Args:
            email: User email
            confirmation_code: Verification code from email
            
        Returns:
            True if confirmation successful
        """
        try:
            self.cognito_client.confirm_sign_up(
                ClientId=self.client_id,
                Username=email,
                ConfirmationCode=confirmation_code
            )
            return True
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'CodeMismatchException':
                raise AuthenticationError("Invalid verification code")
            elif error_code == 'ExpiredCodeException':
                raise AuthenticationError("Verification code expired")
            else:
                raise AuthenticationError(f"Confirmation failed: {e}")

def demo_authentication():
    """Demonstrate authentication flow"""
    
    print("🔐 HaiBlock Authentication Demo")
    print("=" * 50)
    
    # Option 1: Using environment variables (recommended)
    print("\n1️⃣ Authentication using environment variables:")
    
    auth_token = os.getenv('HAIBLOCK_AUTH_TOKEN')
    if auth_token:
        try:
            client = HaiBlockClient(auth_token=auth_token)
            # Test the connection
            analytics = client.get_analytics()
            print("✅ Successfully authenticated using environment variable!")
            print(f"📊 Your account has {analytics.total_content} content items")
        except AuthenticationError as e:
            print(f"❌ Authentication failed: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print("❌ HAIBLOCK_AUTH_TOKEN environment variable not set")
    
    # Option 2: Using AWS Cognito (if configured)
    print("\n2️⃣ Authentication using AWS Cognito:")
    
    user_pool_id = os.getenv('HAIBLOCK_USER_POOL_ID')
    client_id = os.getenv('HAIBLOCK_CLIENT_ID')
    
    if user_pool_id and client_id:
        auth = HaiBlockAuth(user_pool_id, client_id)
        
        # Demo login (don't use real credentials in production!)
        email = os.getenv('DEMO_EMAIL', 'demo@example.com')
        password = os.getenv('DEMO_PASSWORD', 'demo-password')
        
        try:
            print(f"🔑 Attempting to authenticate {email}...")
            token = auth.authenticate(email, password)
            
            # Use the token with HaiBlock client
            client = HaiBlockClient(auth_token=token)
            analytics = client.get_analytics()
            
            print("✅ Successfully authenticated using Cognito!")
            print(f"📊 Your account has {analytics.total_content} content items")
            
        except AuthenticationError as e:
            print(f"❌ Cognito authentication failed: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print("❌ Cognito configuration not available (USER_POOL_ID and CLIENT_ID required)")
    
    # Option 3: Manual token input
    print("\n3️⃣ Manual token input:")
    
    manual_token = input("Enter your HaiBlock auth token (or press Enter to skip): ").strip()
    if manual_token:
        try:
            client = HaiBlockClient(auth_token=manual_token)
            analytics = client.get_analytics()
            print("✅ Successfully authenticated using manual token!")
            print(f"📊 Your account has {analytics.total_content} content items")
        except AuthenticationError as e:
            print(f"❌ Authentication failed: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print("⏭️  Skipped manual token input")
    
    # Authentication best practices
    print("\n" + "=" * 50)
    print("🛡️  AUTHENTICATION BEST PRACTICES")
    print("=" * 50)
    
    practices = [
        "✅ Store auth tokens in environment variables",
        "✅ Use AWS Cognito for production authentication",
        "✅ Implement token refresh logic for long-running applications",
        "✅ Never hardcode credentials in source code",
        "✅ Use IAM roles in AWS environments when possible",
        "✅ Implement proper error handling for authentication failures",
        "✅ Log authentication events for security monitoring"
    ]
    
    for practice in practices:
        print(f"  {practice}")
    
    print("\n📝 Setup Instructions:")
    print("  1. Set HAIBLOCK_AUTH_TOKEN environment variable")
    print("  2. For Cognito: Set HAIBLOCK_USER_POOL_ID and HAIBLOCK_CLIENT_ID")
    print("  3. For development: Set DEMO_EMAIL and DEMO_PASSWORD")
    print("  4. Test authentication before using other SDK features")

def demo_signup_flow():
    """Demonstrate user signup flow"""
    
    print("\n👤 User Signup Demo")
    print("-" * 30)
    
    user_pool_id = os.getenv('HAIBLOCK_USER_POOL_ID')
    client_id = os.getenv('HAIBLOCK_CLIENT_ID')
    
    if not (user_pool_id and client_id):
        print("❌ Cognito configuration required for signup demo")
        return
    
    auth = HaiBlockAuth(user_pool_id, client_id)
    
    # Demo signup (use fake data)
    test_email = "test@example.com"
    test_password = "TempPassword123!"
    test_name = "Test User"
    
    try:
        print(f"📝 Attempting to sign up {test_email}...")
        auth.signup(test_email, test_password, test_name)
        print("✅ Signup successful! Check email for verification code.")
        
        # Note: In production, you would get the code from the user
        confirmation_code = input("Enter verification code from email: ").strip()
        if confirmation_code:
            auth.confirm_signup(test_email, confirmation_code)
            print("✅ Email verified! You can now login.")
        
    except AuthenticationError as e:
        print(f"❌ Signup failed: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    demo_authentication()
    
    # Uncomment to demo signup flow
    # demo_signup_flow()