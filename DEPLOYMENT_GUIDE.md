# Deployment Guide for AI DPR Evaluation System

This guide provides detailed instructions for deploying the AI DPR Evaluation System to production using Vercel for the frontend and Railway for the backend.

## Overview

The AI DPR Evaluation System consists of:
1. **Frontend**: React application built with Vite
2. **Backend**: Python API built with FastAPI

Since Vercel only supports Node.js backends, we'll deploy:
- Frontend to Vercel
- Backend to Railway (or Render/Heroku)

## Prerequisites

1. GitHub account
2. Vercel account
3. Railway account (or Render/Heroku)
4. MongoDB database (Railway offers a free MongoDB plugin)

## Step-by-Step Deployment

### 1. Prepare the Repository

1. Push your code to a GitHub repository
2. Ensure the following files exist in your repository:
   - `vercel.json` (for frontend routing)
   - `backend/Procfile` (for backend deployment)
   - `backend/requirements.txt` (for Python dependencies)
   - `package.json` (for frontend dependencies)

### 2. Deploy the Backend to Railway

1. Go to [railway.app](https://railway.app) and sign up/sign in
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. In the "Root Directory" setting, set it to `backend`
5. Railway will automatically detect it's a Python project
6. Go to the "Variables" tab and add:
   - `MONGODB_URL`: Your MongoDB connection string
   - Any other environment variables from `backend/.env.example`
7. Add MongoDB database:
   - Click "New" → "Database" → "Add MongoDB"
   - Railway will automatically set the `MONGODB_URL` variable
8. Click "Deploy" to deploy your backend

After deployment, note the generated URL for your backend (e.g., `https://your-project.up.railway.app`)

### 3. Update Frontend Configuration

1. Update [vite.config.ts](file:///c%3A/Users/prani/Downloads/AI%20DPR%20Evaluation%20System/vite.config.ts) to use the production backend URL:
   ```javascript
   server: {
     port: 3001,
     open: true,
     proxy: {
       '/api': {
         target: 'https://your-backend-url.up.railway.app',  // Your Railway URL
         changeOrigin: true,
         secure: false,
       }
     }
   }
   ```

Note: For production, you'll want to use environment variables instead of hardcoding the URL.

### 4. Deploy Frontend to Vercel

1. Go to [vercel.com](https://vercel.com) and sign up/sign in
2. Click "New Project"
3. Import your GitHub repository
4. Vercel will automatically detect it's a Vite project
5. Set the following configuration:
   - Framework Preset: Vite
   - Root Directory: `/` (project root)
   - Build Command: `npm run build`
   - Output Directory: `dist`
6. Add environment variables if needed
7. Click "Deploy"

### 5. Configure Environment Variables

#### For Backend (Railway):
In Railway, go to your project → Settings → Variables and add:
- `MONGODB_URL`: (automatically set if using Railway MongoDB)
- `SECRET_KEY`: A random string for JWT tokens
- `FRONTEND_URL`: Your Vercel frontend URL (e.g., `https://your-frontend.vercel.app`)

#### For Frontend (Vercel):
In Vercel, go to your project → Settings → Environment Variables and add:
- `VITE_BACKEND_URL`: Your Railway backend URL

Then update your frontend code to use this environment variable when making API calls.

## Alternative Backend Deployment Options

### Deploying to Render

1. Go to [render.com](https://render.com) and sign up/sign in
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Set the following configuration:
   - Name: Your service name
   - Region: Choose your region
   - Branch: main (or your preferred branch)
   - Root Directory: `backend`
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables
6. Click "Create Web Service"

### Deploying to Heroku

1. Install Heroku CLI
2. In your backend directory, create a `runtime.txt` file:
   ```
   python-3.9.15
   ```
3. Login to Heroku: `heroku login`
4. Create app: `heroku create your-app-name`
5. Set buildpack: `heroku buildpacks:set heroku/python`
6. Deploy: `git subtree push --prefix backend heroku main`

## Post-Deployment Steps

1. Test the frontend and backend connectivity
2. Create initial user accounts if needed
3. Verify that PDF processing works correctly
4. Test the AI features if enabled

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure your backend CORS settings include your frontend URL
2. **API Connection Issues**: Verify environment variables are set correctly
3. **Database Connection Issues**: Check MongoDB connection string
4. **Build Failures**: Ensure all dependencies are in requirements.txt

### Monitoring

- Railway provides built-in logging and monitoring
- Vercel provides performance insights and logs
- Check application logs for error messages

## Scaling Considerations

1. **Database**: Upgrade MongoDB plan as data grows
2. **Backend**: Railway automatically scales based on demand
3. **Frontend**: Vercel automatically handles traffic scaling
4. **File Storage**: For large file uploads, consider integrating with cloud storage services

## Maintenance

1. Regularly update dependencies
2. Monitor application logs
3. Backup database regularly
4. Update AI models as needed