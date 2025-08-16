import requests
import json
import time

def test_register():
    url = "https://notesia.vercel.app/api/auth/register"
    timestamp = int(time.time())
    data = {
        "email": f"test_{timestamp}@example.com",
        "password": "TestPassword123!",
        "full_name": "Test User",
        "username": f"testuser_{timestamp}"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 201:
            print("✅ Registro exitoso")
        else:
            print("❌ Error en el registro")
            
    except Exception as e:
        print(f"Error de conexión: {e}")

if __name__ == "__main__":
    test_register()