#!/usr/bin/env python3
"""
GoPhish + PhishGPT Integration with Fallback
"""

import requests
import json
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class GoPhishIntegrator:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
    def test_connection(self):
        """Test connection to GoPhish API"""
        try:
            response = requests.get(
                f"{self.base_url}/api/campaigns/",
                headers=self.headers,
                verify=False
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Connection failed: {e}")
            return False
    
    def create_email_template(self, name, subject, html_content):
        """Create an email template in GoPhish"""
        template = {
            "name": name,
            "subject": subject,
            "html": html_content,
            "text": subject
        }
        
        response = requests.post(
            f"{self.base_url}/api/templates/",
            headers=self.headers,
            json=template,
            verify=False
        )
        
        if response.status_code == 201:
            template_id = response.json()['id']
            print(f"✅ Template created: {name} (ID: {template_id})")
            return template_id
        else:
            print(f"❌ Failed to create template: {response.text}")
            return None
    
    def create_landing_page(self, name):
        """Create a simple landing page in GoPhish"""
        landing_page = {
            "name": name,
            "html": """
<!DOCTYPE html>
<html>
<head>
    <title>Verify Your Account</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f2f2f2; }
        .login-box { background: white; padding: 30px; border-radius: 4px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); max-width: 400px; margin: 0 auto; }
        input[type="text"], input[type="password"] { width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
        button { background: #0078d4; color: white; padding: 14px 20px; margin: 8px 0; border: none; border-radius: 4px; cursor: pointer; width: 100%; }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>Verify Your Account</h2>
        <form>
            <input type="text" name="username" placeholder="Email" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Verify</button>
        </form>
    </div>
</body>
</html>
            """,
            "capture_credentials": True,
            "capture_passwords": True,
            "redirect_url": "https://example.com"
        }
        
        response = requests.post(
            f"{self.base_url}/api/pages/",
            headers=self.headers,
            json=landing_page,
            verify=False
        )
        
        if response.status_code == 201:
            page_id = response.json()['id']
            print(f"✅ Landing page created: {name} (ID: {page_id})")
            return page_id
        else:
            print(f"❌ Failed to create landing page: {response.text}")
            return None

def generate_ai_email():
    """Try to generate AI email, fallback to template if fails"""
    try:
        from fixed_phishgpt import PhishGPT
        phishgpt = PhishGPT()
        target = {
            "name": "Sarah Johnson",
            "position": "Senior Accountant", 
            "company": "Global Finance Inc",
            "department": "Finance"
        }
        print("Generating AI-powered phishing email...")
        email_content = phishgpt.generate_email(target, "urgent")
        return email_content
    except Exception as e:
        print(f"AI generation failed, using template: {e}")
        return """
Subject: Urgent Security Update Required

Dear Employee,

Our security systems have detected unusual activity on your account. To maintain access and protect company data, you must verify your credentials immediately.

Please click the link below to complete the verification process within the next 24 hours.

IT Security Team
Global Finance Inc
"""

def htmlize_email(text_email):
    """Convert plain text email to HTML format"""
    html = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; max-width: 600px; margin: 0 auto; padding: 20px;">
    <div style="background: #f9f9f9; padding: 20px; border-radius: 5px;">
        {text_email.replace(chr(10), '<br>')}
        <br><br>
        <a href="{{{{.URL}}}}" style="background: #0078d4; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block;">
            Verify Your Account
        </a>
    </div>
</body>
</html>
    """
    return html

def main():
    print("🚀 GoPhish + PhishGPT Integration")
    print("==================================")
    
    # GoPhish configuration
    GOPHISH_URL = "https://localhost:3333"
    GOPHISH_API_KEY = "Replace with your key"
    
    # Initialize integrator
    integrator = GoPhishIntegrator(GOPHISH_URL, GOPHISH_API_KEY)
    
    # Test connection
    print("Testing GoPhish connection...")
    if not integrator.test_connection():
        print("❌ Cannot connect to GoPhish.")
        return
    
    print("✅ Connected to GoPhish!")
    
    # Generate email (with fallback)
    email_content = generate_ai_email()
    
    print("\n📧 Email Content:")
    print("=" * 50)
    print(email_content)
    print("=" * 50)
    
    # Extract subject
    subject = "Urgent Security Update Required"
    for line in email_content.split('\n'):
        if line.startswith('Subject:'):
            subject = line.replace('Subject:', '').strip()
            break
    
    # Convert to HTML
    html_content = htmlize_email(email_content)
    
    print(f"\n📝 Email Subject: {subject}")
    
    # Create GoPhish components
    campaign_name = f"AI_Campaign_{int(time.time())}"
    
    print(f"\nCreating GoPhish campaign: {campaign_name}")
    
    # Create email template
    template_id = integrator.create_email_template(
        name=f"AI_Template_{campaign_name}",
        subject=subject,
        html_content=html_content
    )
    
    if not template_id:
        print("❌ Failed to create template.")
        return
    
    # Create landing page
    page_id = integrator.create_landing_page(
        name=f"AI_Landing_{campaign_name}"
    )
    
    if not page_id:
        print("❌ Failed to create landing page.")
        return
    
    print(f"\n🎉 Success! Created:")
    print(f"   - Email Template ID: {template_id}")
    print(f"   - Landing Page ID: {page_id}")
    print(f"\n📋 Next steps for your class:")
    print(f"1. Go to GoPhish → Campaigns")
    print(f"2. Create new campaign")
    print(f"3. Use Template ID: {template_id}")
    print(f"4. Use Landing Page ID: {page_id}")
    print(f"5. Add test targets and launch!")

if __name__ == "__main__":
    main()
