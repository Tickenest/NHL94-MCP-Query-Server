Write-Host "Starting deployment of NHL94MCPQuery..."

# Clean up any previous build
Write-Host "Cleaning up previous build..."
if (Test-Path package) { Remove-Item -Recurse -Force package }
if (Test-Path deployment.zip) { Remove-Item deployment.zip }

# Create package directory
New-Item -ItemType Directory -Path package | Out-Null

# Install dependencies using Docker to ensure Linux compatibility
Write-Host "Installing dependencies using Docker..."
docker run --name lambda_build python:3.12 `
    pip install mcp requests python-dotenv -t /package
docker cp lambda_build:/package/. ./package/
docker rm lambda_build

# Copy function code into package
Write-Host "Copying function code..."
Copy-Item -Recurse agent package/
Copy-Item -Recurse mcp_server package/
Copy-Item lambda_function.py package/
New-Item -ItemType Directory -Path package/schema -Force | Out-Null
Copy-Item schema/schema.md package/schema/schema.md

# Create the zip file
Write-Host "Creating deployment zip..."
Compress-Archive -Path package/* -DestinationPath deployment.zip

# Deploy to Lambda
Write-Host "Deploying to AWS Lambda..."
aws lambda update-function-code `
    --function-name NHL94MCPQuery `
    --zip-file fileb://deployment.zip `
    --profile nhl94-agent

Write-Host "Deployment complete!"