#!/bin/bash
echo "🔐 AI Social Engineering Lab Setup"
echo "==================================="
echo "Educational Purpose - Use Responsibly"
echo

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "❌ Please don't run as root. Use regular user permissions."
    exit 1
fi

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip3 install requests urllib3

# Install Ollama
echo "🤖 Installing Ollama AI engine..."
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
echo "🚀 Starting Ollama service..."
sudo systemctl start ollama
sudo systemctl enable ollama

# Download AI model
echo "📥 Downloading AI model (this may take 10-30 minutes)..."
ollama pull phi:2.7b

# Download GoPhish
echo "🎣 Downloading GoPhish..."
wget -q https://github.com/gophish/gophish/releases/download/v0.12.1/gophish-v0.12.1-linux-64bit.zip
unzip -q gophish-v0.12.1-linux-64bit.zip
cd gophish-v0.12.1-linux-64bit
chmod +x gophish

# Create GoPhish config
echo "⚙️ Creating GoPhish configuration..."
cat > config.json << 'EOF'
{
	"admin_server": {
		"listen_url": "127.0.0.1:3333",
		"use_tls": true
	},
	"phish_server": {
		"listen_url": "0.0.0.0:8080",
		"use_tls": false
	},
	"db_name": "gophish.db",
	"migrations_prefix": "db/db_"
}
EOF

echo
echo "✅ Setup complete!"
echo
echo "📋 Next steps:"
echo "1. Start GoPhish: cd gophish-v0.12.1-linux-64bit && ./gophish --config config.json"
echo "2. Get API key from https://localhost:3333 → Settings → API"
echo "3. Update gophish_integrator.py with your API key"
echo "4. Run: python3 fixed_phishgpt.py"
echo
echo "⚠️  Remember: Educational use only in controlled environments!"
