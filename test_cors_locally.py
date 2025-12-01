#!/usr/bin/env python3
"""
Script to test CORS configuration locally
"""

import asyncio
import httpx
from backend.main import app

async def test_cors():
    """Test CORS configuration"""
    print("Testing CORS configuration...")
    
    # Create a test client
    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
        # Test a preflight OPTIONS request
        headers = {
            "Origin": "https://ai-dpr-evaluation-system-qrtg.vercel.app",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        }
        
        print("Sending OPTIONS request...")
        response = await client.options("/api/dpr/upload_with_ai", headers=headers)
        
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        # Check for CORS headers
        cors_headers = [
            "access-control-allow-origin",
            "access-control-allow-credentials",
            "access-control-allow-methods",
            "access-control-allow-headers"
        ]
        
        for header in cors_headers:
            if header in response.headers:
                print(f"{header}: {response.headers[header]}")
            else:
                print(f"MISSING {header}")
        
        # Test a simple GET request
        print("\nSending GET request...")
        response = await client.get("/", headers={"Origin": "https://ai-dpr-evaluation-system-qrtg.vercel.app"})
        
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        # Check for CORS headers
        for header in cors_headers:
            if header in response.headers:
                print(f"{header}: {response.headers[header]}")
            else:
                print(f"MISSING {header}")

if __name__ == "__main__":
    asyncio.run(test_cors())