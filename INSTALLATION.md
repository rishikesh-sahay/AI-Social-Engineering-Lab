Simple Installation Guide

Step 1: Clone the Repository

git clone https://github.com/rishikesh-sahay/AI-Social-Engineering-Lab
cd AI-Social-Engineering-Lab


Step 2: Choose Installation Method
Option A: Automated Installation (Recommended for Beginners)
chmod +x setup.sh
./setup.sh


The automated script will:

Update system packages

Install Python dependencies

Install and configure Ollama AI engine

Download AI model (phi:2.7b)

Download and configure GoPhish

Create necessary configuration files



Manual Installation

1. Install Dependencies

sudo apt update && sudo apt install -y python3 python3-pip curl wget unzip
pip3 install requests urllib3

2. Install AI Engine

curl -fsSL https://ollama.ai/install.sh | sh
sudo systemctl start ollama
ollama pull phi:2.7b

3. Install GoPhish

wget https://github.com/gophish/gophish/releases/download/v0.12.1/gophish-v0.12.1-linux-64bit.zip
unzip gophish-v0.12.1-linux-64bit.zip
cd gophish-v0.12.1-linux-64bit
chmod +x gophish

4. Setup Steps

Start GoPhish: ./gophish

Get API Key: Go to https://localhost:3333 → Settings → API

Update Script: Edit gophish_integrator.py with your API key

Test Installation

# Test AI
ollama run phi:2.7b "Hello"

# Test PhishGPT  
python3 fixed_phishgpt.py

# Test GoPhish
python3 gophish_integrator.py


Usage
# Generate phishing emails
python3 fixed_phishgpt.py

# Create GoPhish campaigns
python3 gophish_integrator.py


Note: Educational use only. Always get proper authorization.


Option B: Manual Installation (For Advanced Users)
1. Install System Dependencies

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and tools
sudo apt install -y python3 python3-pip curl wget unzip

2. Install Python Dependencies

pip3 install requests urllib3

3. Install Ollama AI Engine

# Download and install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
sudo systemctl start ollama
sudo systemctl enable ollama

# Verify service is running
sudo systemctl status ollama


4. Download AI Model

# Download a lightweight model (recommended for CPU)
ollama pull phi:2.7b

# Alternative models (optional):
# ollama pull llama2:7b-chat        # 3.8GB - Good balance
# ollama pull mistral:7b-instruct   # 4.1GB - More capable


5. Install and Configure GoPhish

# Download GoPhish
wget https://github.com/gophish/gophish/releases/download/v0.12.1/gophish-v0.12.1-linux-64bit.zip

# Extract and prepare
unzip gophish-v0.12.1-linux-64bit.zip
cd gophish-v0.12.1-linux-64bit
chmod +x gophish



Step 3: Initial Setup and Configuration
1. Start GoPhish

# Navigate to GoPhish directory
cd gophish-v0.12.1-linux-64bit

# Start GoPhish with configuration
./gophish --config config.json

2. Get GoPhish API Key
Open web browser and go to: https://localhost:3333

Login with default credentials (check terminal output for password)

Navigate to: Settings → API

Copy the API Key - you'll need this for integration


3. Configure Integration Script
Edit gophish_integrator.py with your API key:


# Back in the main project directory
cd ..
nano gophish_integrator.py
Find this line and replace with your actual API key:


GOPHISH_API_KEY = "your_actual_gophish_api_key_here"

Step 4: Verification Tests
Test 1: Ollama AI Engine
# Test basic AI functionality
ollama run phi:2.7b "Write a one-sentence test email about IT maintenance"

# Expected: AI should respond within 30-60 seconds with a generated sentence



Test 2: PhishGPT

# Test the phishing email generator
python3 fixed_phishgpt.py

# Expected: Should generate sample phishing emails for training


Test 3: GoPhish Integration

# Test connection to GoPhish
python3 gophish_integrator.py

# Expected: Should show "Connected to GoPhish!" and template creation




Step 5: Complete Lab Setup
Configure SMTP for Email Sending (Required for Full Functionality)
In GoPhish UI (https://localhost:3333), go to Sending Profiles

Click New Profile

Configure with your email provider:

Name: Lab SMTP

Interface Type: SMTP

Host: smtp.gmail.com:587 (or your provider)

Username: Your email address

Password: App-specific password (not your regular password)

From Address: security@yourcompany.com



Create Test User Group
In GoPhish UI, go to Users & Groups

Click New Group

Name: Test Targets

Add test email addresses (use your own for testing)







Troubleshooting Common Issues
Issue 1: Ollama Service Not Running

# Check status
sudo systemctl status ollama

# If not running, start it
sudo systemctl start ollama

# If service fails, check logs
journalctl -u ollama.service -f




Issue 2: GoPhish Connection Refused

# Check if GoPhish is running
ps aux | grep gophish

# If not, start it from the correct directory
cd gophish-v0.12.1-linux-64bit
./gophish --config config.json

# Check if port 3333 is listening
netstat -tlnp | grep 3333





Issue 3: API Key Not Working
Verify you copied the entire API key from GoPhish UI

Check there are no extra spaces in the script

Ensure GoPhish is running when testing



Issue 4: Model Download Too Slow

# Cancel current download (Ctrl+C) and try smaller model
ollama pull phi:2.7b

# Or use even smaller model
ollama pull llama2:3b


Issue 5: Permission Errors

# Don't run as root - use regular user permissions
# Fix file permissions if needed
chmod +x *.py
chmod +x *.sh



Usage

# Generate phishing emails
python3 fixed_phishgpt.py

# Create GoPhish campaigns
python3 gophish_integrator.py
