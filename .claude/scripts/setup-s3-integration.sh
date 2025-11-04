#!/bin/bash
# Setup S3 Integration for Backups and Archival
# Installs AWS CLI and configures S3 buckets

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║              S3 Integration Setup                              ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "📦 Installing AWS CLI..."

    # Install via Homebrew
    if command -v brew &> /dev/null; then
        brew install awscli
    else
        echo "❌ Homebrew not found. Installing AWS CLI manually..."
        curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "/tmp/AWSCLIV2.pkg"
        sudo installer -pkg /tmp/AWSCLIV2.pkg -target /
        rm /tmp/AWSCLIV2.pkg
    fi

    echo "✅ AWS CLI installed"
else
    echo "✅ AWS CLI already installed: $(aws --version)"
fi

echo ""
echo "🔐 Configuring AWS credentials..."
echo ""

# Check if credentials exist
if [ -f ~/.aws/credentials ]; then
    echo "✅ AWS credentials already configured"
    echo ""
    echo "Current profiles:"
    aws configure list-profiles
else
    echo "Choose credential source:"
    echo "1. Enter manually"
    echo "2. Retrieve from 1Password"
    echo ""
    read -p "Enter choice (1 or 2): " cred_choice

    if [ "$cred_choice" = "1" ]; then
        echo ""
        echo "Enter AWS credentials:"
        read -p "AWS Access Key ID: " aws_access_key
        read -sp "AWS Secret Access Key: " aws_secret_key
        echo ""
        read -p "Default region (e.g., us-east-1): " aws_region

        mkdir -p ~/.aws
        cat > ~/.aws/credentials <<EOF
[default]
aws_access_key_id = $aws_access_key
aws_secret_access_key = $aws_secret_key
EOF

        cat > ~/.aws/config <<EOF
[default]
region = $aws_region
output = json
EOF

        echo "✅ Credentials saved"

    elif [ "$cred_choice" = "2" ]; then
        echo ""
        echo "Looking for AWS credentials in 1Password..."

        # Check if 1Password CLI is available
        if ! command -v op &> /dev/null; then
            echo "❌ 1Password CLI not found"
            echo "   Install: brew install --cask 1password-cli"
            exit 1
        fi

        # Search for AWS credentials
        echo "Searching for AWS items in 1Password..."
        aws_items=$(op item list --categories "Login,Password,API Credential" --format json 2>/dev/null | jq -r '.[] | select(.title | test("AWS|S3|Amazon"; "i")) | .id + " | " + .title')

        if [ -z "$aws_items" ]; then
            echo "⚠️  No AWS items found in 1Password"
            echo "   Please run option 1 to enter manually"
            exit 1
        fi

        echo ""
        echo "Found AWS items:"
        echo "$aws_items"
        echo ""
        read -p "Enter item ID to use: " item_id

        # Extract credentials
        aws_access_key=$(op item get "$item_id" --fields "access key id,username" 2>/dev/null | head -1)
        aws_secret_key=$(op item get "$item_id" --fields "secret access key,password" 2>/dev/null | head -1)

        if [ -z "$aws_access_key" ] || [ -z "$aws_secret_key" ]; then
            echo "❌ Could not extract credentials from 1Password item"
            exit 1
        fi

        read -p "Default region (e.g., us-east-1): " aws_region

        mkdir -p ~/.aws
        cat > ~/.aws/credentials <<EOF
[default]
aws_access_key_id = $aws_access_key
aws_secret_access_key = $aws_secret_key
EOF

        cat > ~/.aws/config <<EOF
[default]
region = $aws_region
output = json
EOF

        echo "✅ Credentials retrieved from 1Password and saved"
    else
        echo "❌ Invalid choice"
        exit 1
    fi
fi

echo ""
echo "📊 Testing S3 connection..."
if aws s3 ls &> /dev/null; then
    echo "✅ S3 connection successful"
    echo ""
    echo "Available buckets:"
    aws s3 ls
else
    echo "⚠️  Could not list buckets (may need to create one)"
fi

echo ""
echo "🪣 S3 Bucket Setup"
echo ""
read -p "Do you want to create a new bucket for backups? (y/N): " create_bucket

if [[ "$create_bucket" =~ ^[Yy]$ ]]; then
    read -p "Enter bucket name (e.g., mike-finneran-backups): " bucket_name
    read -p "Enter region (e.g., us-east-1): " bucket_region

    echo "Creating bucket: $bucket_name in $bucket_region..."

    if [ "$bucket_region" = "us-east-1" ]; then
        aws s3api create-bucket --bucket "$bucket_name" --region "$bucket_region"
    else
        aws s3api create-bucket --bucket "$bucket_name" --region "$bucket_region" \
            --create-bucket-configuration LocationConstraint="$bucket_region"
    fi

    # Enable versioning
    aws s3api put-bucket-versioning --bucket "$bucket_name" \
        --versioning-configuration Status=Enabled

    # Enable encryption
    aws s3api put-bucket-encryption --bucket "$bucket_name" \
        --server-side-encryption-configuration '{
            "Rules": [{
                "ApplyServerSideEncryptionByDefault": {
                    "SSEAlgorithm": "AES256"
                }
            }]
        }'

    echo "✅ Bucket created with versioning and encryption enabled"

    # Save bucket name to environment
    echo "" >> ~/.zshrc
    echo "# S3 Backup Configuration" >> ~/.zshrc
    echo "export S3_BACKUP_BUCKET='$bucket_name'" >> ~/.zshrc

    echo "✅ Bucket name saved to ~/.zshrc"
else
    echo ""
    echo "Using existing bucket. Set it in your environment:"
    echo "   export S3_BACKUP_BUCKET='your-bucket-name'"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                   S3 Setup Complete!                           ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo "1. Reload shell: source ~/.zshrc"
echo "2. Test backup: ~/.claude/scripts/backup-to-s3.sh"
echo ""
