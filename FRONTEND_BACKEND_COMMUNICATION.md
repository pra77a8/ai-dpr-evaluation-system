# Frontend-Backend Communication Setup

This document explains how the frontend communicates with the backend in different environments.

## Environment Configuration

### Development Environment
- Frontend runs on: `http://localhost:3001`
- Backend runs on: `http://localhost:8000`
- Communication: Uses Vite proxy to forward `/api` requests to the backend

### Production Environment
- Frontend hosted on: Vercel (URL varies)
- Backend hosted on: Render at `https://ai-dpr-backend-2.onrender.com`
- Communication: Direct API calls to the Render backend

## Configuration Files

### 1. vite.config.ts
```javascript
server: {
  proxy: {
    '/api': {
      target: process.env.VITE_BACKEND_URL || 'https://ai-dpr-backend-2.onrender.com',
      changeOrigin: true,
      secure: false,
    }
  }
}
```

### 2. src/utils/api.js
```javascript
const getBaseURL = () => {
  // In production, use the environment variable or default to Render URL
  if (process.env.NODE_ENV === 'production') {
    return import.meta.env.VITE_BACKEND_URL || 'https://ai-dpr-backend-2.onrender.com';
  }
  // In development, use the proxy
  return '';
};
```

## Environment Variables

### Development (.env file)
```
VITE_BACKEND_URL=http://localhost:8000
```

### Production (.env.production file)
```
VITE_BACKEND_URL=https://ai-dpr-backend-2.onrender.com
```

## Testing Communication

### 1. Health Check Endpoint
- Endpoint: `/api/health`
- Expected Response: `{"status": "healthy"}`

### 2. Manual Testing
You can test the connection by:
1. Starting the frontend: `npm run dev`
2. Visiting `http://localhost:3001/api/health` in your browser
3. You should see the health check response from the backend

### 3. Using the Test Component
The `BackendTest.tsx` component automatically tests the connection when loaded.

## Troubleshooting

### Common Issues

1. **CORS Errors**
   - Ensure the backend has proper CORS configuration
   - Check that the frontend URL is in the allowed origins list

2. **404 Errors**
   - Verify the backend is running
   - Check that the API endpoints exist
   - Confirm the proxy configuration is correct

3. **Connection Refused**
   - Ensure the backend server is accessible
   - Check firewall settings
   - Verify the backend URL is correct

### Debugging Steps

1. **Check Network Tab**
   - Open browser dev tools
   - Look at the Network tab when making API calls
   - Check request URLs and response codes

2. **Verify Environment Variables**
   - Ensure `VITE_BACKEND_URL` is set correctly
   - Check that variables are loaded properly

3. **Test Backend Directly**
   - Visit the backend URL directly in browser
   - Test API endpoints without the frontend

## Deployment

### Vercel Deployment
1. Set `VITE_BACKEND_URL` in Vercel project settings
2. Ensure the build command is `npm run build`
3. Set output directory to `dist`

### Render Backend
1. Ensure the backend is deployed and running
2. Verify the URL is accessible
3. Check that environment variables are set correctly

## Security Considerations

1. **Environment Variables**
   - Never commit actual environment files to Git
   - Use `.env.example` as a template only

2. **API Keys**
   - Keep sensitive keys on the backend
   - Never expose backend secrets to the frontend

3. **CORS Configuration**
   - Restrict allowed origins in production
   - Don't use wildcard (*) in production