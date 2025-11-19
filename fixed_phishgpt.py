#!/usr/bin/env python3
"""
Improved PhishGPT - Working Version
"""

import subprocess
import time
import requests
import json

class PhishGPT:
    def __init__(self, model="phi:2.7b"):
        self.model = model
        self.base_url = "http://localhost:11434"
        
    def is_ollama_ready(self):
        """Check if Ollama API is responsive"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def generate_with_api(self, prompt):
        """Use Ollama API instead of command line"""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=120  # 2 minute timeout
            )
            if response.status_code == 200:
                return response.json()['response']
            else:
                return f"API Error: {response.status_code}"
        except Exception as e:
            return f"API Call Error: {str(e)}"
    
    def generate_email(self, target_info, email_type="urgent"):
        """Generate email using API"""
        
        prompt = f"""Create a short security notification email for training. 
        To: {target_info['name']} ({target_info['position']})
        Company: {target_info['company']}
        Scenario: {email_type} security update
        Keep it very short - 2-3 sentences maximum."""
        
        print("Sending request to Ollama API...")
        return self.generate_with_api(prompt)

def main():
    print("🔐 Improved PhishGPT - Using Ollama API")
    print("=" * 50)
    
    phishgpt = PhishGPT()
    
    # Check if Ollama is ready
    if not phishgpt.is_ollama_ready():
        print("❌ Ollama is not responding. Please check: sudo systemctl status ollama")
        return
    
    print("✅ Ollama is running")
    
    # Test targets
    targets = [
        {
            "name": "Sarah Johnson",
            "position": "Senior Accountant", 
            "company": "Global Finance Inc",
            "department": "Finance"
        },
        {
            "name": "Mike Chen",
            "position": "Marketing Manager",
            "company": "Tech Innovations LLC", 
            "department": "Marketing"
        }
    ]
    
    for i, target in enumerate(targets, 1):
        print(f"\n🎯 Generating email for {target['name']}...")
        print("Please be patient - CPU mode is slow...")
        
        start_time = time.time()
        email = phishgpt.generate_email(target, "urgent")
        end_time = time.time()
        
        print(f"Generated in {end_time - start_time:.1f} seconds")
        print(f"\n📧 Email {i}:")
        print("=" * 50)
        print(email)
        print("=" * 50)
        
        if i < len(targets):
            input("\nPress Enter for next example...")

if __name__ == "__main__":
    main()
