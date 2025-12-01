# AI DPR Evaluation System

This is an AI-powered system for evaluating Daily Progress Reports (DPRs) with risk assessment capabilities.

## Deployment Instructions

### Frontend Deployment (Vercel)

1. **Prepare for Vercel Deployment**:
   - This project includes a `vercel.json` configuration file for proper routing
   - The frontend is built with Vite and React

2. **Deploy to Vercel**:
   - Push your code to a GitHub repository
   - Go to [Vercel](https://vercel.com) and sign up/sign in
   - Click "New Project"
   - Import your GitHub repository
   - Vercel will automatically detect the Vite project
   - Keep the default settings and click "Deploy"

3. **Environment Variables** (if needed):
   - Add any required environment variables in the Vercel project settings

### Backend Deployment

Since Vercel doesn't support Python backends, you'll need to deploy the backend separately:

#### Option 1: Render (Currently Being Deployed)
1. Create an account at [render.com](https://render.com)
2. Create a new Web Service
3. Connect your GitHub repository
4. Set the root directory to `/backend`
5. Set the build command to `pip install -r requirements.txt`
6. Set the start command to `uvicorn main:app --host 0.0.0.0 --port $PORT`
7. Add environment variables:
   - `MONGODB_URL`: Your MongoDB connection string

#### Option 2: Railway (Recommended)
1. Create an account at [railway.app](https://railway.app)
2. Create a new project
3. Connect your GitHub repository
4. Set the root directory to `/backend`
5. Add a `Procfile` in the backend directory with:
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
6. Deploy the project

#### Option 3: Heroku
1. Create an account at [heroku.com](https://heroku.com)
2. Install the Heroku CLI
3. Create a new app: `heroku create your-app-name`
4. Set the stack to container: `heroku stack:set container`
5. Deploy: `git push heroku main`

### Connecting Frontend to Backend

After deploying your backend:
1. Update the proxy settings in `vite.config.ts` to point to your deployed backend URL
2. Or set environment variables in Vercel for the backend URL
3. Modify the frontend code to use the production backend URL

### Local Development

To run the application locally:
1. Install frontend dependencies: `npm install`
2. Start frontend: `npm run dev`
3. In a separate terminal, navigate to the backend directory
4. Install backend dependencies: `pip install -r requirements.txt`
5. Start backend: `uvicorn main:app --reload`

The frontend will be available at http://localhost:3001
The backend API will be available at http://localhost:8000

## Recent Updates

- **Vercel Deployment Fix**: Updated configuration files to resolve build issues (2025-10-09)
- **Render Deployment Configuration**: Added [render.yaml](file://c:\Users\prani\Downloads\AI%20DPR%20Evaluation%20System\render.yaml) and updated dependencies for Render deployment (2025-10-09)