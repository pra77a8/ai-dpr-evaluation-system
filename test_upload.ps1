# Test PDF upload using PowerShell
try {
    $uri = "http://localhost:3000/api/dpr/upload"
    $filePath = "backend\test_dpr_document.pdf"
    
    # Create a multipart form data content
    $multipartContent = [System.Net.Http.MultipartFormDataContent]::new()
    
    # Add file content
    $fileBytes = [System.IO.File]::ReadAllBytes($filePath)
    $fileContent = [System.Net.Http.ByteArrayContent]::new($fileBytes)
    $fileContent.Headers.ContentDisposition = [System.Net.Http.Headers.ContentDispositionHeaderValue]::new("form-data")
    $fileContent.Headers.ContentDisposition.Name = "file"
    $fileContent.Headers.ContentDisposition.FileName = "test_dpr_document.pdf"
    $multipartContent.Add($fileContent)
    
    # Add uploaded_by field
    $stringContent = [System.Net.Http.StringContent]::new("test_user")
    $stringContent.Headers.ContentDisposition = [System.Net.Http.Headers.ContentDispositionHeaderValue]::new("form-data")
    $stringContent.Headers.ContentDisposition.Name = "uploaded_by"
    $multipartContent.Add($stringContent)
    
    # Create HTTP client and send request
    $httpClient = [System.Net.Http.HttpClient]::new()
    $response = $httpClient.PostAsync($uri, $multipartContent).Result
    
    Write-Host "Status Code: $($response.StatusCode)"
    $responseContent = $response.Content.ReadAsStringAsync().Result
    Write-Host "Response: $responseContent"
}
catch {
    Write-Host "Error: $($_.Exception.Message)"
}