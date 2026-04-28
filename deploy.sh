#!/bin/bash

set -e

echo "Starting deployment of NHL94MCPQuery..."

# Clean up any previous build
echo "Cleaning up previous build..."
rm -rf package
rm -f deployment.zip

# Create package directory
mkdir package

# Install dependencies into package directory
echo "Installing dependencies..."
pip install mcp requests python-dotenv -t package/

# Copy function code into package
echo "Copying function code..."
cp -r agent package/
cp -r mcp_server package/
cp lambda_function.py package/
cp schema/schema.md package/schema.md

# Create the zip file
echo "Creating deployment zip..."
cd package
zip -r ../deployment.zip .
cd ..

# Deploy to Lambda
echo "Deploying to AWS Lambda..."
aws lambda update-function-code \
    --function-name NHL94MCPQuery \
    --zip-file fileb://deployment.zip \
    --profile nhl94-agent

echo "Deployment complete!"