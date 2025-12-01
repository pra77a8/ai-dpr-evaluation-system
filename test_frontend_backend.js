// Simple test to verify frontend can communicate with backend
async function testBackendConnection() {
  const backendUrl = import.meta.env.VITE_BACKEND_URL || 'https://ai-dpr-backend-2.onrender.com';
  
  console.log('Testing connection to backend at:', backendUrl);
  
  try {
    // Test the root endpoint
    const response = await fetch(`${backendUrl}/`);
    const data = await response.json();
    
    console.log('✅ Backend connection successful!');
    console.log('Response:', data);
    
    // Test the health endpoint
    const healthResponse = await fetch(`${backendUrl}/health`);
    const healthData = await healthResponse.json();
    
    console.log('✅ Health check successful!');
    console.log('Health response:', healthData);
    
    return true;
  } catch (error) {
    console.error('❌ Backend connection failed:', error);
    return false;
  }
}

// Run the test
testBackendConnection().then(success => {
  if (success) {
    console.log('🎉 All tests passed! Your frontend should be able to communicate with your backend.');
  } else {
    console.log('💥 Tests failed. Please check your backend URL and network configuration.');
  }
});