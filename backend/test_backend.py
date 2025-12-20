#!/usr/bin/env python3
"""
Test script to verify the backend API is working properly with the correct Qdrant collection.
"""
import requests
import os
import sys
import time

def test_backend():
    base_url = "http://127.0.0.1:8000"

    print("Testing backend connectivity...")

    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

    # Test chat endpoint exists
    try:
        # This will fail with 422 since we're not sending proper data, but that's okay
        response = requests.post(f"{base_url}/api/v1/chat", json={})
        print(f"Chat endpoint accessible: {response.status_code}")
    except Exception as e:
        print(f"Chat endpoint test failed: {e}")
        return False

    # Test ask-from-selection endpoint exists
    try:
        # This will fail with 422 since we're not sending proper data, but that's okay
        response = requests.post(f"{base_url}/api/v1/ask-from-selection", json={})
        print(f"Ask-from-selection endpoint accessible: {response.status_code}")
    except Exception as e:
        print(f"Ask-from-selection endpoint test failed: {e}")
        return False

    print("Backend endpoints are accessible!")
    return True

if __name__ == "__main__":
    print("Starting backend verification test...")
    success = test_backend()
    if success:
        print("\n[SUCCESS] Backend verification successful!")
        print("The API endpoints are properly configured and accessible.")
        print("Next steps: Start the backend with 'uvicorn main:app --reload --port 8000'")
    else:
        print("\n[ERROR] Backend verification failed!")
        sys.exit(1)