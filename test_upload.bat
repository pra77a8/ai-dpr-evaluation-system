@echo off
echo Testing DPR upload...
curl -X POST "http://127.0.0.1:8000/api/dpr/upload_with_ai" -F "file=@Model_DPR_Final 2.0.pdf" -F "uploaded_by=test_user"
echo.
echo Upload test completed.