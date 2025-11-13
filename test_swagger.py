import requests
import json

def test_swagger():
    base_url = "http://localhost:8000"
    
    print("Testing Swagger Documentation...")
    
    # Test Swagger JSON
    try:
        response = requests.get(f"{base_url}/swagger.json")
        if response.status_code == 200:
            print("✓ Swagger JSON is accessible")
            data = response.json()
            print(f"  - API Title: {data.get('info', {}).get('title')}")
            print(f"  - API Version: {data.get('info', {}).get('version')}")
            print(f"  - Number of paths: {len(data.get('paths', {}))}")
        else:
            print(f"✗ Swagger JSON failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Swagger JSON error: {e}")
    
    # Test Swagger UI
    try:
        response = requests.get(f"{base_url}/swagger/")
        if response.status_code == 200:
            print("✓ Swagger UI is accessible")
        else:
            print(f"✗ Swagger UI failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Swagger UI error: {e}")
    
    # Test ReDoc
    try:
        response = requests.get(f"{base_url}/redoc/")
        if response.status_code == 200:
            print("✓ ReDoc is accessible")
        else:
            print(f"✗ ReDoc failed: {response.status_code}")
    except Exception as e:
        print(f"✗ ReDoc error: {e}")
    
    print("\nVisit these URLs in your browser:")
    print(f"Swagger UI: {base_url}/swagger/")
    print(f"ReDoc: {base_url}/redoc/")

if __name__ == "__main__":
    test_swagger()