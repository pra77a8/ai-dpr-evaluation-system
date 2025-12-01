# MongoDB Connection Fix Instructions

## Problem
Your Render deployment is failing with the error:
```
pymongo.errors.ServerSelectionTimeoutError: localhost:27017: [Errno 111] Connection refused
```

This means your backend is trying to connect to a local MongoDB instance instead of your MongoDB Atlas cluster.

## Root Cause
The backend is falling back to `mongodb://localhost:27017` because the `MONGODB_URL` environment variable is not set in your Render deployment.

## Solution

### Step 1: Get Your MongoDB Atlas Connection String

1. Go to MongoDB Atlas: https://cloud.mongodb.com/
2. Select your cluster
3. Click "Connect" button
4. Choose "Connect your application"
5. Copy the SRV connection string (it should start with `mongodb+srv://`)

Example format:
```
mongodb+srv://username:password@cluster-name.mongodb.net/database-name
```

### Step 2: Set Environment Variable in Render

1. Go to your Render dashboard: https://dashboard.render.com/
2. Find your `ai-dpr-backend-2` service
3. Click on "Environment" in the left sidebar
4. Add a new environment variable:
   - **Name**: `MONGODB_URL`
   - **Value**: Your MongoDB Atlas SRV connection string
   - Example: `mongodb+srv://myuser:mypassword@mycluster.mongodb.net/dpr_system`

### Step 3: Verify MongoDB Atlas Configuration

Make sure your MongoDB Atlas is properly configured:

1. **Database User**:
   - Go to "Database Access" in MongoDB Atlas
   - Ensure the user exists with read/write permissions
   - Make sure the username and password match your connection string

2. **Network Access**:
   - Go to "Network Access" in MongoDB Atlas
   - Add your Render service IP to the whitelist
   - For testing, you can temporarily add `0.0.0.0/0` (less secure)
   - For production, use specific IP ranges

### Step 4: Redeploy Your Service

1. After setting the environment variable, redeploy your service
2. Go to your service page in Render
3. Click "Manual Deploy" or push a new commit to trigger deployment

## Verification

### Test Locally (Optional)
You can test your connection string locally:

1. Create a `.env` file in your backend directory:
   ```
   MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/database_name
   ```

2. Run the verification script:
   ```bash
   python verify_mongodb_connection.py
   ```

## Common Issues and Solutions

### 1. Authentication Failed
- **Cause**: Wrong username or password
- **Solution**: Verify credentials in MongoDB Atlas

### 2. Network Access Denied
- **Cause**: IP not whitelisted in MongoDB Atlas
- **Solution**: Add Render's IP to whitelist (0.0.0.0/0 for testing)

### 3. Wrong Connection String Format
- **Cause**: Using `mongodb://` instead of `mongodb+srv://`
- **Solution**: Use the SRV format from MongoDB Atlas

### 4. Database User Permissions
- **Cause**: User doesn't have access to the database
- **Solution**: Grant read/write permissions in MongoDB Atlas

## Environment Variables Required

Make sure these environment variables are set in Render:

| Variable Name | Required | Description |
|---------------|----------|-------------|
| `MONGODB_URL` | ✅ Yes | MongoDB Atlas SRV connection string |
| `SECRET_KEY` | ✅ Yes | Secret key for JWT tokens |
| `ALGORITHM` | ✅ Yes | JWT algorithm (usually HS256) |

## After Fixing

1. Wait for deployment to complete
2. Test the application by uploading a DPR file
3. Check Render logs for any remaining errors

If you continue to have issues, check the Render logs for specific error messages and compare them with the troubleshooting guide above.