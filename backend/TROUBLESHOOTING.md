# Deployment Troubleshooting Guide

This guide helps diagnose and resolve common deployment issues.

## Common Issues and Solutions

### 1. Missing Dependencies

**Error**: `ModuleNotFoundError` or similar import errors

**Solution**: 
- Check that all required packages are listed in [requirements.txt](file:///c%3A/Users/prani/Downloads/AI%20DPR%20Evaluation%20System/backend/requirements.txt)
- Ensure special dependencies like `pydantic[email]` are properly specified
- Check build logs for specific missing modules

### 2. Port Binding Issues

**Error**: `No open ports detected` or application fails to start

**Solution**:
- Ensure the application listens on `0.0.0.0` (not `localhost` or `127.0.0.1`)
- Use the `$PORT` environment variable provided by Render
- Correct start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### 3. MongoDB Connection Issues

**Error**: `The DNS query name does not exist` or similar MongoDB connection errors

**Solution**:
- Verify your MongoDB connection string format:
  - Should start with `mongodb+srv://` for Atlas clusters
  - Should include username and password: `mongodb+srv://username:password@cluster.mongodb.net/database`
- Check that your MongoDB Atlas cluster allows connections from Render's IP addresses
- Ensure your MongoDB Atlas username and password are correct
- Test your connection string locally before deploying

### 4. Missing Environment Variables

**Error**: Application fails to start or functions incorrectly

**Solution**:
- Set required environment variables in Render dashboard:
  - `MONGODB_URL`: MongoDB connection string
  - `SECRET_KEY`: JWT secret key
  - `ALGORITHM`: JWT algorithm (typically HS256)
  - `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time
- Never commit actual [.env](file:///c%3A/Users/prani/Downloads/AI%20DPR%20Evaluation%20System/.env) files to Git repositories
- Use [.env.example](file:///c%3A/Users/prani/Downloads/AI%20DPR%20Evaluation%20System/backend/.env.example) as a template for local development

### 5. Build Script Failures

**Error**: Build process fails or exits with non-zero status

**Solution**:
- Check [build.sh](file:///c%3A/Users/prani/Downloads/AI%20DPR%20Evaluation%20System/backend/build.sh) for proper error handling
- Ensure all commands have proper exit codes
- Add logging to identify where failures occur

### 6. Python Version Compatibility

**Error**: Compilation errors or runtime issues

**Solution**:
- Specify Python version in [.python-version](file:///c%3A/Users/prani/Downloads/AI%20DPR%20Evaluation%20System/backend/.python-version) file
- Use compatible package versions in [requirements.txt](file:///c%3A/Users/prani/Downloads/AI%20DPR%20Evaluation%20System/backend/requirements.txt)

## Debugging Steps

1. **Check Build Logs**: Look for specific error messages
2. **Verify Environment Variables**: Ensure all required variables are set
3. **Test Locally**: Run the same commands locally to reproduce issues
4. **Simplify Dependencies**: Temporarily remove complex packages to isolate issues

## Health Check Endpoints

- `/health`: Basic health check
- `/healthz`: Deployment verification endpoint

## Environment Variables Required

- `SECRET_KEY`: JWT secret key
- `ALGORITHM`: JWT algorithm (typically HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time
- `MONGODB_URL`: MongoDB connection string (format: `mongodb+srv://username:password@cluster.mongodb.net/database`)

## MongoDB Atlas Setup

1. Create a cluster at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a database user with read/write permissions
3. Add your connection IP to the whitelist (or allow access from anywhere: 0.0.0.0/0)
4. Get your connection string from the "Connect" button
5. Replace `<password>` with your actual password
6. Set as `MONGODB_URL` environment variable in Render

## Testing MongoDB Connection Locally

```bash
# Test your MongoDB connection string locally
mongosh "mongodb+srv://username:password@cluster.mongodb.net/test"
```

## Setting Environment Variables in Render

1. Go to your Render dashboard
2. Select your service
3. Click "Environment" in the left sidebar
4. Add each required environment variable
5. Click "Save Changes"
6. Redeploy your service

## Debugging MongoDB Connection Issues

If you're seeing "The DNS query name does not exist" errors:

1. **Verify Connection String Format**:
   - Correct format: `mongodb+srv://username:password@cluster.mongodb.net/database`
   - Incorrect format: `mongodb://username:password@cluster.mongodb.net/database` (missing srv)

2. **Check Cluster Name**:
   - Ensure your cluster name is correct
   - The error shows `cluster0.xxxxx.mongodb.net` - make sure this matches your actual cluster

3. **Verify Credentials**:
   - Double-check your username and password
   - Special characters in passwords need to be URL-encoded

4. **Network Access**:
   - In MongoDB Atlas, go to "Network Access"
   - Add `0.0.0.0/0` to allow connections from any IP (for testing)
   - For production, add Render's IP addresses

5. **Test Connection String**:
   ```bash
   # Test locally with mongosh
   mongosh "mongodb+srv://username:password@cluster.mongodb.net/test"
   ```

## Common MongoDB Connection String Issues

1. **Missing SRV**: Using `mongodb://` instead of `mongodb+srv://`
2. **Wrong Cluster Name**: Typo in the cluster name
3. **Incorrect Credentials**: Wrong username or password
4. **Special Characters**: Passwords with special characters not URL-encoded
5. **Network Restrictions**: IP whitelist not configured correctly

## Verifying Your MongoDB Setup

1. Log into MongoDB Atlas
2. Go to your cluster
3. Click "Connect"
4. Select "Connect your application"
5. Copy the connection string
6. Replace `<password>` with your actual password
7. Test locally before deploying

## Testing MongoDB Connection with Python Script

You can test your MongoDB connection using the provided test script:

```bash
# Navigate to the backend directory
cd backend

# Run the test script
python test_mongodb_connection.py
```

This script will:
1. Test the connection to your MongoDB instance
2. Verify database access
3. Test document insertion and deletion
4. Provide detailed logging of each step

## Using dpr_user as MongoDB Username

If you're using `dpr_user` as your MongoDB username, make sure:

1. The user exists in your MongoDB Atlas cluster
2. The user has read/write permissions to the `dpr_evaluation_system` database
3. Your connection string looks like:
   ```
   mongodb+srv://dpr_user:your_password@cluster.mongodb.net/dpr_evaluation_system
   ```
4. Special characters in your password are URL-encoded

## URL Encoding for MongoDB Credentials

If your password contains special characters, they need to be URL-encoded:

| Character | URL Encoded |
|-----------|-------------|
| @         | %40         |
| :         | %3A         |
| /         | %2F         |
| ?         | %3F         |
| #         | %23         |
| [         | %5B         |
| ]         | %5D         |
| %         | %25         |

Example:
- Original password: `my@pass:123`
- URL-encoded password: `my%40pass%3A123`
- Connection string: `mongodb+srv://dpr_user:my%40pass%3A123@cluster.mongodb.net/database`