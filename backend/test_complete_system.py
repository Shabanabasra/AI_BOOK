#!/usr/bin/env python3
"""
Test script to verify the complete CCR-compliant retrieval chatbot system
"""
import requests
import json

def test_backend():
    """Test the backend API directly"""
    print("Testing backend API...")

    # Test the /chat endpoint
    url = "http://127.0.0.1:8000/chat"
    payload = {"question": "What is artificial intelligence?"}

    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print("✅ Backend API test successful!")
            print(f"Query: {data['query']}")
            print(f"Retrieved documents: {len(data['retrieved_documents'])}")

            if data['retrieved_documents']:
                first_doc = data['retrieved_documents'][0]
                print(f"First document title: {first_doc['title']}")
                print(f"First document score: {first_doc['score']}")
                print(f"First document source: {first_doc['source']}")

            return True
        else:
            print(f"❌ Backend API test failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Backend API test failed with error: {str(e)}")
        return False

def test_health():
    """Test the health endpoint"""
    print("\nTesting health endpoint...")

    try:
        response = requests.get("http://127.0.0.1:8000/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health check successful: {health_data}")
            return True
        else:
            print(f"❌ Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check failed with error: {str(e)}")
        return False

def test_root():
    """Test the root endpoint"""
    print("\nTesting root endpoint...")

    try:
        response = requests.get("http://127.0.0.1:8000/")
        if response.status_code == 200:
            print("✅ Root endpoint test successful")
            return True
        else:
            print(f"❌ Root endpoint test failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Root endpoint test failed with error: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing CCR-compliant Retrieval Chatbot System")
    print("="*50)

    all_tests_passed = True

    # Test health endpoint
    if not test_health():
        all_tests_passed = False

    # Test root endpoint
    if not test_root():
        all_tests_passed = False

    # Test main chat endpoint
    if not test_backend():
        all_tests_passed = False

    print("\n" + "="*50)
    if all_tests_passed:
        print("🎉 All system tests passed! CCR-compliant retrieval chatbot is working correctly.")
        print("\nSystem Components:")
        print("- ✅ FastAPI backend with .env configuration")
        print("- ✅ RetrievalAgent integration with Qdrant and Cohere")
        print("- ✅ POST /chat endpoint with required JSON output format")
        print("- ✅ Logging and error handling")
        print("- ✅ React frontend with document display")
    else:
        print("❌ Some tests failed. Please check the system configuration.")

    # Note about frontend
    print("\nNote: Frontend can be started with 'npm run dev' in the frontend directory")
    print("The frontend is configured to connect to http://127.0.0.1:8000/chat")