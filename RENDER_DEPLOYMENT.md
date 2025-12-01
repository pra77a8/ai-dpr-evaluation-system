# Deploying to Render

This guide explains how to deploy the AI DPR Evaluation System backend to Render.

## Prerequisites

1. A Render account (sign up at [render.com](https://render.com))
2. This repository connected to your GitHub account

## Deployment Steps

### 1. Create a New Web Service

1. Log in to your Render account
2. Click the "New" button in the top right corner
3. Select "Web Service"

### 2. Connect Your Repository

1. Search for `pra77a8/ai-dpr-evaluation-system`
2. Select the repository

### 3. Configure Your Web Service

Set the following configuration:

- **Name**: `ai-dpr-backend`
- **Region**: Choose your preferred region
- **Branch**: [main](file://c:\Users\prani\Downloads\AI%20DPR%20Evaluation%20System\main.py#L0-L54)
- **Root Directory**: `backend`
- **Runtime**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

**Important**: Make sure to set the Root Directory to `backend` so Render knows this is a Python application, not a Node.js application.

### 4. Add Environment Variables

In the "Advanced" section, add these environment variables:

- `SECRET_KEY`: A random string for JWT token generation
- `ALGORITHM`: HS256
- `ACCESS_TOKEN_EXPIRE_MINUTES`: 30
- `MONGODB_URL`: Your MongoDB Atlas connection string (see below)

### 5. Set Up MongoDB Database

Since Render doesn't provide managed MongoDB instances, you need to use MongoDB Atlas:

1. **Create MongoDB Atlas Account**:
   - Go to [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
   - Sign up for a free account
   - Create a new cluster (free tier M0 Sandbox)

2. **Configure Database Access**:
   - In Atlas dashboard, go to "Database Access"
   - Click "Add New Database User"
   - Create a new user with "Read and write to any database" permissions

3. **Configure Network Access**:
   - Go to "Network Access"
   - Click "Add IP Address"
   - Select "Allow Access from Anywhere" (0.0.0.0/0) for testing

4. **Get Connection String**:
   - Go back to "Clusters"
   - Click "Connect" on your cluster
   - Select "Connect your application"
   - Copy the connection string and replace `<password>` with the actual password

### 6. Deploy

Click "Create Web Service" and wait for the deployment to complete.

## Alternative: Using render.yaml

This repository includes a [render.yaml](file://c:\Users\prani\Downloads\AI%20DPR%20Evaluation%20System\render.yaml) file that automatically configures the service for Render. If you link your repository correctly, Render should automatically detect and use this configuration.

## Connecting to Frontend

Once deployed, Render will provide a URL for your backend (e.g., `https://ai-dpr-backend.onrender.com`).

Update your frontend to use this URL by setting the `VITE_BACKEND_URL` environment variable in your Vercel project settings.

## Troubleshooting

### Build Failures

If you encounter build failures:

1. Make sure the Root Directory is set to `backend`
2. Check that all dependencies in [requirements.txt](file:///c%3A/Users/prani/Downloads/AI%20DPR%20Evaluation%20System/backend/requirements.txt) are compatible with Render's build environment
3. Ensure you're using Python 3.9.x (specified in [.python-version](file:///c%3A/Users/prani/Downloads/AI%20DPR%20Evaluation%20System/backend/.python-version))

### Common Issues

1. **Node.js vs Python Detection**: Render might try to build this as a Node.js app because there's a [package.json](file:///c%3A/Users/prani/Downloads/AI%20DPR%20Evaluation%20System/package.json) in the root. Setting the Root Directory to `backend` fixes this.

2. **Compilation Errors**: Some packages like `blis` and `spacy` might have compilation issues. We've simplified [requirements.txt](file:///c%3A/Users/prani/Downloads/AI%20DPR%20Evaluation%20System/backend/requirements.txt) to avoid these problematic dependencies.

3. **Memory Issues**: If you encounter memory issues during deployment, consider upgrading to a paid plan on Render.

## Notes

- The first deployment might take a few minutes as Render installs dependencies
- Render automatically handles HTTPS for your application
- Your application will automatically scale based on traffic
- Make sure to replace `<password>` in your MongoDB connection string with the actual password

## Recent Updates

- **Simplified Dependencies**: Removed problematic packages that caused compilation issues
- **Improved Configuration**: Updated [render.yaml](file://c:\Users\prani\Downloads\AI%20DPR%20Evaluation%20System\render.yaml) with explicit root directory